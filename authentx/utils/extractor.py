from typing import Dict, Any, Optional
from dataclasses import dataclass
import pdfplumber
import re
import spacy

@dataclass
class PDFFile:
    path: str
    text: Optional[str]
    metadata: Optional[Dict[str, Any]]


def extractor(file: PDFFile) -> str:
    with pdfplumber.open(file.path) as pdf:
        text = "".join(page.extract_text() for page in pdf.pages)
    return text

async def web_source_processor(data: str):
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        spacy.cli.download("en_core_web_sm")
        nlp = spacy.load("en_core_web_sm")

    stopwords = nlp.Defaults.stop_words

    text = re.sub(r"\W|\s+[a-zA-Z]\s+|\^[a-zA-Z]\s+|\d+|\s+|\n", " ", data).strip()
    words = text.lower().split()
    return [word for word in words if word not in stopwords]
    

if __name__ == "__main__":
    file = PDFFile(path="test/EEG_Text_Generation.pdf", text=None, metadata=None)
    text = extractor(file)
    print(text)