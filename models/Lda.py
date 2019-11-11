import gensim
from gensim import corpora
from gensim import models

import os.path
from os import path

from gensim.similarities import Similarity
from gensim.test.utils import get_tmpfile

import multiprocessing
workers = multiprocessing.cpu_count() - 1

from .preprocess_text import preprocess_text, Splitter, LemmatizationWithPOSTagger
import pyLDAvis.gensim
#pyLDAvis.enable_notebook()


class LDA():

    def __init__(self, documents = [[]]):
        
        #list of tokenised documents
        #e.g. [['Aman', 'is', 'a', 'good', 'boy'],
        #      ['Naman', 'is', 'a', 'bad', 'boy']]
        self.documents =  documents
        self.dictionary = None
        self.corpus = None
        self.corpus_tfidf = None

        self.model = None

    def createCorpus(self):
    
        self.dictionary = corpora.Dictionary(self.documents)
        #dictionary.save('./text/combined.dict')        
        self.corpus = [self.dictionary.doc2bow(text) for text in self.documents]
        tfidf = models.TfidfModel(self.corpus)  # step 1 -- initialize a model
        self.corpus_tfidf = tfidf[self.corpus]

    def train_lda(self, num_topics, chunksize = 1000, passes = 4):
        self.model = models.LdaMulticore(corpus = self.corpus_tfidf, num_topics = num_topics, id2word = self.dictionary,
                                 workers = workers, chunksize = chunksize, passes = passes)

    def query(self, text):
        text = preprocess_text(text)
        vec_text = self.dictionary.doc2bow(text.lower().split())
        tfidf = models.TfidfModel(self.corpus)
        vec_tfidf = tfidf[vec_text]
    
        return self.model[vec_tfidf]

    def showTopics(self, topic_id):
        return self.model.show_topics(topic_id)
    
    def visualiseTopics(self):
        vis = pyLDAvis.gensim.prepare(self.model, self.corpus, self.dictionary)
        pyLDAvis.save_html(vis, 'index.html')
        #return vis

    


