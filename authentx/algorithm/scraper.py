import bs4
import asyncio
import aiohttp
from duckduckgo_search import AsyncDDGS
import logging



class Scraper:
    def __init__(self):
        self.results = []
        self.ddgs = AsyncDDGS(proxy=None)

    async def _aget_urls(self, word):
        results = await self.ddgs.text(word, max_results=5)
        return [result["href"] for result in results]

    async def _scrape_search_text(self, urls):
        async with aiohttp.ClientSession() as session:
            tasks = [self._fetch(session, url) for url in urls]
            pages = await asyncio.gather(*tasks)
            self.results.extend(
                bs4.BeautifulSoup(page, "html.parser").text for page in pages
            )
        return self.results

    async def _fetch(self, session, url):
        try:
            async with session.get(url) as response:
                return await response.text()
        except (
            aiohttp.client_exceptions.ServerDisconnectedError,
            aiohttp.client_exceptions.ClientOSError,
        ) as e:
            logging.error(f"Error occurred: {e}")
            await asyncio.sleep(0.2 )  # Wait for 0.2 second before retrying

    async def aggregate(self, words):
        tasks = [self._aget_urls(w) for w in words]
        urls = await asyncio.gather(*tasks)
        # Flatten the nested list of urls
        urls = [url for sublist in urls for url in sublist]
        self.data = await self._scrape_search_text(urls)
        self.data = " ".join(self.data)
        print(self.data)
        return self.data


if __name__ == "__main__":
    words = ["apple", "banana", "cherry"]
    scraper = Scraper()
    asyncio.run(scraper.aggregate(words))
