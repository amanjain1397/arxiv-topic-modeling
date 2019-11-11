import os
from os import path
import glob
import tqdm
import argparse
import sys
from models.Harvester import Harvester
import models.preprocess_text
from models.Lda import LDA

import pyLDAvis.gensim
#pyLDAvis.enable_notebook()

#from gensim import corpora

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)

parser = argparse.ArgumentParser(
    # ... other options ...
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

#Arguments related to harvesting data 

parser.add_argument('--endpoint', type=str, default = 'http://export.arxiv.org/oai2',help='The endpoint of OAI interface')
parser.add_argument('--metadataPrefix', type=str, default = 'oai_dc',help='the prefix identifying the metadata format')
parser.add_argument('--harvestSet', type=str, default = 'cs',help='a set for selective harvesting')
parser.add_argument('--from_when', type=str, default = '2019-11-01', help='the earliest timestamp of the records, format : yyyy/mm/dd')
parser.add_argument('--until_when', type=str, default = '', help='the latest timestamp of the records, format: yyyy/mm/dd, blank means today\'s date')

#Arguments related to topic modeling
parser.add_argument('--num_topics', type=int,  default = 30, help='Number of topics to be found')
parser.add_argument('--chunksize', type=int,  default = 400)
parser.add_argument('--passes', type=int,  default= 4)
parser.add_argument('--visualisation', type = bool, default = True, help = 'Topic visualisation using pyLDAvis')


FLAGS = parser.parse_args()

endpoint = FLAGS.endpoint
metadataPrefix = FLAGS.metadataPrefix
harvestSet = FLAGS.harvestSet
from_when = FLAGS.from_when
until_when = FLAGS.until_when

num_topics = FLAGS.num_topics
chunksize = FLAGS.chunksize
passes = FLAGS.passes
visualisation = FLAGS.visualisation

if __name__ == "__main__":
    
    ###----Harvesting the data----###

    #First we harvest the data from the arXiv e-print repository
    h = Harvester(endpoint, metadataPrefix, harvestSet, from_when, until_when)
    
    #Issues a ListRecords request 
    h.responseCollector()

    #Retreiving the .xml files of the records
    h.recordCollector()
    
    #Making list of tokensied abstracts
    h.createCorpus()


    ###----Topic modeling in the corpus----### 
    
    #descriptions - the list of tokenised documents
    documents = h.descriptions

    #Instantiating the Gensim LDA model
    lda = LDA(documents)
    
    #Generating the corpus
    lda.createCorpus()

    #Training the LDA model
    lda.train_lda(num_topics, chunksize, passes)
    
    if(visualisation):
        #Visualising the found topics using pyLDAvis
        #index.html is stored at ./index.html
        lda.visualiseTopics()