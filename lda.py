import pickle

import gensim
from gensim import corpora
from gensim import models

import os.path
from os import path

import recorder
from recorder import Splitter, LemmatizationWithPOSTagger

from gensim.similarities import Similarity
from gensim.test.utils import get_tmpfile

import multiprocessing
workers = multiprocessing.cpu_count() - 1

def dictionary_corpus():
    try:    

        with open('./pkl/main/combined_list.pickle', 'rb') as handle:
            combined_list = pickle.load(handle)
            handle.close()

        with open('./pkl/main/flag1.pickle', 'rb') as handle:
            flag1 = pickle.load(handle)
            handle.close()        
        
        try:
            with open('./pkl/lda/flag2.pickle', 'rb') as handle1, open('./text/corpus.pickle', 'rb') as handle2:
                flag2 = pickle.load(handle1)
                if(combined_list[flag2: ]):
                    corpus = pickle.load(handle2)
                    handle2.close()

                    dictionary = corpora.Dictionary.load('./text/combined.dict')
                    dictionary.add_documents(combined_list[flag2:])
                    
                    corpus.extend([dictionary.doc2bow(text) for text in combined_list[flag2:]])                    
                    tfidf = models.TfidfModel(corpus)  # step 1 -- initialize a model
                    corpus_tfidf = tfidf[corpus]
                    
                    print('Corpus updated successfully')
                    dictionary.save('./text/combined.dict')
                    handle1.close()
                    
                    with open('./text/corpus.pickle', 'wb') as handle:
                        pickle.dump(corpus, handle, pickle.HIGHEST_PROTOCOL)
                        handle.close()
                    
                    with open('./text/corpus_tfidf.pickle', 'wb') as handle:
                        pickle.dump(corpus_tfidf, handle, pickle.HIGHEST_PROTOCOL)
                        handle.close()

                    with open('./pkl/lda/flag2.pickle', 'wb') as handle:
                        pickle.dump(len(combined_list), handle, pickle.HIGHEST_PROTOCOL)
                        handle.close()
                    
                    with open('./pkl/lda/updated.pickle', 'wb') as handle:
                        pickle.dump(1, handle, pickle.HIGHEST_PROTOCOL)
                        handle.close()
                    
                else:
                    print('Corpus and dictionary already updated!')
                    handle1.close()
                    handle2.close()
        
        except:
            
            dictionary = corpora.Dictionary(combined_list)
            dictionary.save('./text/combined.dict')
            
            corpus = [dictionary.doc2bow(text) for text in combined_list]
            tfidf = models.TfidfModel(corpus)  # step 1 -- initialize a model
            corpus_tfidf = tfidf[corpus]
            
            print('Dictionary and corpus created!')

            with open('./text/corpus.pickle', 'wb') as handle:
                pickle.dump(corpus, handle, pickle.HIGHEST_PROTOCOL)
                handle.close()
                
            with open('./text/corpus_tfidf.pickle', 'wb') as handle:
                pickle.dump(corpus_tfidf, handle, pickle.HIGHEST_PROTOCOL)
                handle.close()

            with open('./pkl/lda/flag2.pickle', 'wb') as handle:
                pickle.dump(len(combined_list), handle, pickle.HIGHEST_PROTOCOL)
                handle.close()

            with open('./pkl/lda/updated.pickle', 'wb') as handle:
                        pickle.dump(0, handle, pickle.HIGHEST_PROTOCOL)
                        handle.close()
                        
    except FileNotFoundError:
        print('One or more of the required files missing')
        


def train_lda():
        
    try:
        with open('./text/corpus_tfidf.pickle', 'rb') as handle:
            corpus_tfidf = pickle.load(handle)
            handle.close()

        dictionary = corpora.Dictionary.load('./text/combined.dict')
        normal_train(corpus_tfidf, dictionary)                

    except:
        print('No corpus present to train the model on!')
        return
            
    
def online_train(lda, extended_corpus):
    
    print('Updating the existing model!')
    
    lda.update(extended_corpus)
    os.remove('./text/extended_corpus.pickle')
    
    with open('./models/lda.pickle', 'wb') as handle:
        pickle.dump(lda, handle, pickle.HIGHEST_PROTOCOL)
    

def normal_train(corpus_tfidf, dictionary):
    
    with open('./pkl/lda/updated.pickle', 'rb') as handle:
        updated = pickle.load(handle)
        handle.close()

    if((updated == 0) & path.exists('./models/lda.pickle')):
        print('The model is already trained')
        return

    elif(updated ==1):

        print('The corpus was updated! Retraining the LDA model!')

    else:
        print('Training the model now!')
        
    lda = models.LdaMulticore(corpus = corpus_tfidf, num_topics = 30, id2word = dictionary, workers = workers, chunksize = 1000, passes = 4)

    with open('./models/lda.pickle', 'wb') as handle:
        pickle.dump(lda, handle, pickle.HIGHEST_PROTOCOL)
        handle.close()

    with open('./pkl/lda/updated.pickle', 'wb') as handle:
        pickle.dump(0, handle, pickle.HIGHEST_PROTOCOL)

def query(text):

    try:
        with open('./text/corpus.pickle', 'rb') as handle:
            corpus = pickle.load(handle)
            dictionary = corpora.Dictionary.load('./text/combined.dict')
            handle.close()
            
        try:
            with open('./models/lda.pickle', 'rb') as handle:
                lda = pickle.load(handle)
                handle.close()
                
            text = recorder.preprocess_dict(text)
            vec_text = dictionary.doc2bow(text.lower().split())
            
            tfidf = models.TfidfModel(corpus)
            vec_tfidf = tfidf[vec_text]
        
            return lda[vec_tfidf]
        except FileNotFoundError:
            print('lda.pickle is not found. ')

    
    except:
        print('Corpus is not present!')
    
