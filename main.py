import pickle

import pandas as pd
import numpy as np
import glob

import tqdm

import pyLDAvis.gensim
pyLDAvis.enable_notebook()

import os
from os import path

from gensim import corpora 
import recorder

import _pickle as cPickle

def creator(): 
    files = pd.Series(glob.glob('./xml/*.xml'))
    file_nums = files.str.findall(r'response(\d+)\.xml').apply(np.squeeze).astype('uint16').sort_values().reset_index(drop = True)


    try:
        with open('./pkl/main/fileDumpCounter.pickle', 'rb') as handle:
            fileDumpCounter = pickle.load(handle)
            handle.close()
            
            nums = file_nums[file_nums > fileDumpCounter]
            #print(nums)        

            if(len(nums) != 0):
                with open('./pkl/main/recDict.pickle', 'rb') as handle1, open('./pkl/main/flag1.pickle', 'rb') as handle2, open('./pkl/main/combined_list.pickle', 'rb') as handle3, open('./pkl/main/id_list.pickle', 'rb') as handle4:
                    recDict = cPickle.load(handle1)
                    flag1 = cPickle.load(handle2)
                    combined_list = cPickle.load(handle3)
                    id_list = cPickle.load(handle4)

                handle1.close()
                handle2.close()
                handle3.close()
                handle4.close()

                for num in tqdm.tqdm(nums):
                    #fileDumpCounter += 1
                    recDict, flag1, id_list, combined_list = recorder.dictRecords('./xml/response' + str(num) + '.xml', flag1, recDict, id_list, combined_list)            
            
            try:
                fileDumpCounter = max(nums)
                
                #flag1 is the actual record number in the dictionary. Record nums : [0, inf]
                #flag1 is equal to  len(recDict - 1)

                with open('./pkl/main/recDict.pickle', 'wb') as handle1:
                    cPickle.dump(recDict, handle1, protocol = pickle.HIGHEST_PROTOCOL)

                with open('./pkl/main/flag1.pickle', 'wb') as handle2:
                    cPickle.dump(flag1, handle2, protocol=pickle.HIGHEST_PROTOCOL)

                '''with open('./pkl/main/abstract_list.pickle', 'wb') as handle3:
                    cPickle.dump(abstract_list, handle3, protocol = pickle.HIGHEST_PROTOCOL)'''
                
                with open('./pkl/main/combined_list.pickle', 'wb') as handle3:
                    cPickle.dump(combined_list, handle3, protocol = pickle.HIGHEST_PROTOCOL)
                    
                with open('./pkl/main/id_list.pickle', 'wb') as handle4:
                    cPickle.dump(id_list, handle4, protocol=pickle.HIGHEST_PROTOCOL)

                with open('./pkl/main/fileDumpCounter.pickle', 'wb') as handle5:
                        pickle.dump(fileDumpCounter, handle5, protocol=pickle.HIGHEST_PROTOCOL)

                '''with open('./pkl/main/title_list.pickle', 'wb') as handle6:
                        pickle.dump(title_list, handle6, protocol=pickle.HIGHEST_PROTOCOL)'''    
                handle1.close()
                handle2.close()
                handle3.close()
                handle4.close()
                handle5.close()
                #handle6.close()
                            
            except ValueError:
                print('Dumping file counter!')
                with open('./pkl/main/fileDumpCounter.pickle', 'wb') as handle:
                        pickle.dump(fileDumpCounter, handle, protocol=pickle.HIGHEST_PROTOCOL)
                handle.close()

    except:
            #fileDumpCounter = -1
            print('No prev dict found. Creating a new one!')
            recDict = {}
            flag1 = -1
            combined_list = []
            id_list = []
            
            for num in tqdm.tqdm(file_nums):
                recDict, flag1, id_list, combined_list = recorder.dictRecords('./xml/response' + str(num) + '.xml', flag1, recDict, id_list, combined_list)

            try:
                fileDumpCounter = max(file_nums)
                
                with open('./pkl/main/recDict.pickle', 'wb') as handle1:
                    cPickle.dump(recDict, handle1, protocol = pickle.HIGHEST_PROTOCOL)

                with open('./pkl/main/flag1.pickle', 'wb') as handle2:
                    cPickle.dump(flag1, handle2, protocol=pickle.HIGHEST_PROTOCOL)

                '''with open('./pkl/main/abstract_list.pickle', 'wb') as handle3:
                    cPickle.dump(abstract_list, handle3, protocol = pickle.HIGHEST_PROTOCOL)'''

                with open('./pkl/main/combined_list.pickle', 'wb') as handle3:
                    cPickle.dump(combined_list, handle3, protocol = pickle.HIGHEST_PROTOCOL)

                with open('./pkl/main/id_list.pickle', 'wb') as handle4:
                    cPickle.dump(id_list, handle4, protocol=pickle.HIGHEST_PROTOCOL)

                with open('./pkl/main/fileDumpCounter.pickle', 'wb') as handle5:
                        pickle.dump(fileDumpCounter, handle5, protocol=pickle.HIGHEST_PROTOCOL)

                '''with open('./pkl/main/title_list.pickle', 'wb') as handle6:
                        pickle.dump(title_list, handle6, protocol=pickle.HIGHEST_PROTOCOL)'''    
                
                handle1.close()
                handle2.close()
                handle3.close()
                handle4.close()
                handle5.close()
                #handle6.close()
                
            except ValueError:
                print('No .xml files to write into dictionary!')

def show_topics():
    if(path.exists('./models/lda.pickle')):
        with open('./models/lda.pickle', 'rb') as handle:
                lda = pickle.load(handle)
                handle.close()
        return lda.show_topics(-1)
    else:
        print('No model present to show topics for!')
    

def visualise_topics():
    if(path.exists('./models/lda.pickle')):
        with open('./models/lda.pickle', 'rb') as handle:
            lda = pickle.load(handle)
            handle.close()
                
        try:
            with open('./text/corpus.pickle', 'rb') as handle:

                corpus = pickle.load(handle)
                dictionary = corpora.Dictionary.load('./text/combined.dict')
                handle.close()

                vis = pyLDAvis.gensim.prepare(lda, corpus, dictionary)
                return vis
        except:
            print('Either corpus or dictionary not present.')
            return
    else:
        print('No model present to visulaise topics of.')
    


def pklInfo():
    
    with open('./pkl/harvest/flag.pickle', 'rb') as handle:
        flag = pickle.load(handle)
        print('flag : ', flag)
        handle.close()
        
    with open('./pkl/harvest/today.pickle', 'rb') as handle:
        today = pickle.load(handle)
        print('today : ', today)
        handle.close()

    with open('./pkl/main/flag1.pickle', 'rb') as handle:
        flag1 = pickle.load(handle)
        print('flag1 : ', flag1)
        handle.close()
    
    with open('./pkl/main/recDict.pickle', 'rb') as handle:
        recDict = pickle.load(handle)
        print('Length of recDict : ', len(recDict))
        handle.close()

    '''with open('./pkl/main/abstract_list.pickle', 'rb') as handle:
        abstract_list = pickle.load(handle)
        print('Length of abstract_list : ', len(abstract_list))
        handle.close()'''

    with open('./pkl/main/id_list.pickle', 'rb') as handle:
        id_list = pickle.load(handle)
        print('Length of id_list : ', len(id_list))
        handle.close()

    with open('./pkl/main/fileDumpCounter.pickle', 'rb') as handle:
        fileDumpCounter = pickle.load(handle)
        print('fileDumpCounter : ', fileDumpCounter)
        handle.close()    
    
    with open('./pkl/main/combined_list.pickle', 'rb') as handle:
        combined_list = pickle.load(handle)
        print('Length of combined_list : ', len(combined_list))
        handle.close()
    
    with open('./pkl/lda/flag2.pickle', 'rb') as handle:
        flag2 = pickle.load(handle)
        print('flag2 : ', flag2)
        handle.close()
