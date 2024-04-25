import spacy
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem import PorterStemmer
from nltk import ngrams
import asyncio
from gensim.models import KeyedVectors
import numpy as np
from gensim.scripts.glove2word2vec import glove2word2vec
import os
from typing import Set


class Analyser:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        glove_input_file = os.path.join(base_dir, "glove/glove.6B.100d.txt")
        word2vec_output_file = os.path.join(base_dir, "glove/glove.6B.100d.txt.w2v")
        self.nlp = self.load_nlp_model()
        self.stopwords = self.nlp.Defaults.stop_words
        self.stemmer = PorterStemmer()
        self.glove_model = self.load_glove_model(glove_input_file, word2vec_output_file)

    @staticmethod
    def load_nlp_model():
        try:
            return spacy.load("en_core_web_sm")
        except OSError:
            spacy.cli.download("en_core_web_sm")
            return spacy.load("en_core_web_sm")

    @staticmethod
    def load_glove_model(
        glove_input_file: str, word2vec_output_file: str
    ) -> KeyedVectors:
        try:
            return KeyedVectors.load_word2vec_format(word2vec_output_file, binary=False)
        except FileNotFoundError:
            glove2word2vec(glove_input_file, word2vec_output_file)
            return KeyedVectors.load_word2vec_format(
                word2vec_output_file, binary=False, no_header=True
            )

    async def _calculate_glove_similarity(self, text1: str, text2: str) -> float:
        tokens1 = text1.split()
        tokens2 = text2.split()

        vector1 = np.mean(
            [self.glove_model[token] for token in tokens1 if token in self.glove_model],
            axis=0,
        )
        vector2 = np.mean(
            [self.glove_model[token] for token in tokens2 if token in self.glove_model],
            axis=0,
        )

        return cosine_similarity([vector1], [vector2])[0][0]

    async def preprocess(self, text: str) -> str:
        text = re.sub(r"\W|\s+[a-zA-Z]\s+|\^[a-zA-Z]\s+|\d+|\s+|\n", " ", text).strip()
        return " ".join(
            [
                self.stemmer.stem(word)
                for word in text.lower().split()
                if word not in self.stopwords
            ]
        )

    async def _create_shingles(self, text: str, k=3) -> Set[str]:
        return set(["".join(gram) for gram in list(ngrams(text, k))])

    async def check_plagiarism(self, text1: str, text2: str, k=3) -> float:
        text1 = await self.preprocess(text1)
        text2 = await self.preprocess(text2)

        shingles1 = await self._create_shingles(text1, k)
        shingles2 = await self._create_shingles(text2, k)

        intersection = shingles1.intersection(shingles2)
        union = shingles1.union(shingles2)
        jaccard_similarity = len(intersection) / len(union)

        vectorizer = TfidfVectorizer(ngram_range=(1, 3))
        tfidf_matrix = vectorizer.fit_transform([text1, text2])

        cosine_similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix)

        return (jaccard_similarity + cosine_similarities[0][1]) / 2


if __name__ == "__main__":
    analyser = Analyser()
    text = "This is a test sentence. It is used to test the analyser."
    text2 = "This sentence is an exercise. It is used for analyzer testing."
    print(asyncio.run(analyser.check_plagiarism(text, text2)))
