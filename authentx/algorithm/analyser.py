import numpy as np
from gensim import models
from gensim.utils import simple_preprocess
from gensim import corpora

def tfdif(doc: str):
    tokenized = []
    for sentence in doc.read().split(''):
        tokenized.append(simple_preprocess(sentence, deacc= True))

    dictionary = corpora.Dictionary(tokenized)

    BoW_corpus = [dictionary.doc2bow(doc, allow_update=True) for doc in tokenized]

    # Word weight in Bag of Words corpus
    word_weight = []
    for doc in BoW_corpus:
        for id, freq in doc:
            word_weight.append([dictionary[id], freq])


    # create TF-IDF model
    tfIdf = models.TfidfModel(BoW_corpus, smartirs='ntc')

    # TF-IDF Word Weight
    weight_tfidf = []
    for doc in tfIdf[BoW_corpus]:
        for id, freq in doc:
            weight_tfidf.append([dictionary[id], np.around(freq, decimals=3)])
    print(weight_tfidf)

if __name__ == "__main__":
    from authentx.utils import extractor, PDFFile
    file = PDFFile(path="test/EEG_Text_Generation.pdf", text=None, metadata=None)
    text = extractor(file)

    tfdif(text)