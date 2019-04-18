#Parses the .xml files in ./xml and creates (or updates) the 1) dictionary and 2) lists of data from the data parsed from the .xml file 

import xml.etree.ElementTree as ET
import re
import string

import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

from nltk.corpus import stopwords
nltk.download('wordnet')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')
stopwords = set(stopwords.words('english'))


def dictRecords(xmlfile, flag1, recDict, id_list, combined_list):
    
    #Shorthands
    OAI = '{http://www.openarchives.org/OAI/2.0/}'
    OAI2 = '{http://www.openarchives.org/OAI/2.0/oai_dc/}'
    PURL = '{http://purl.org/dc/elements/1.1/}'
    
    #create element tree object
    tree = ET.parse(xmlfile)
    
    #get root element
    root = tree.getroot()
    
    for item in root.findall('./' + OAI + 'ListRecords/'):
        #print(flag1)
        flag1 = flag1 + 1
        recDict[flag1] = {}
 
        #Storing the ID from the header
        for idfier in item.findall('./'+ OAI + 'header/' + OAI + 'identifier'):
            recDict[flag1]['id'] = re.sub('\\n', '', idfier.text)
            id_list.append(recDict[flag1]['id'])

        for metadata in item.findall('./' + OAI + 'metadata'):

            for dc in metadata.findall('./' + OAI2 + 'dc'):

                #For storing the title of the record
                for title in dc.findall('./' + PURL + 'title'):
                    recDict[flag1]['title'] = title.text
                    ti = preprocess_dict(recDict[flag1]['title']).split() #Preprocessing the title before storing it.

                #For storing the processed_description (abstract) of the record
                i = 0
                for descrip in dc.findall('./' + PURL + 'description'):
                    i += 1
                    if(i == 1):
                        txt = re.sub('\\n', ' ', descrip.text)
                        recDict[flag1]['abstract'] = txt
                        ab = preprocess_dict(recDict[flag1]['abstract']).split() #Preprocessing the abstract before storing it.
                 
                combined_list.append(ab + ti)

    if(len(recDict) != len(combined_list)):
        recDict.pop(flag1, None)
        return recDict, flag1 - 1, id_list, combined_list
    else:
        return recDict, flag1, id_list, combined_list 
    #_ = abstract_list.pop()
    #_ = id_list.pop()
    
def preprocess_dict(text):
    
    text = re.sub(r'\([^)]*\)', '', text)

    '''#Removing instances like (SGD), (ANN) etc
    text = re.sub(r'[A-Z]{2,}', '', text)

    #Removing instances like (SGD), (ANN) etc
    text = re.sub(r'[A-Z]+-[A-Z]+', '', text)
    
    #Removing instances like SGD, ANN etc
    text = re.sub(r'\([A-Z]{2,}\)', '', text)

    #Removing instances like AB-CDE, EF-GHI etc
    text = re.sub(r'\([A-Z]+-[A-Z]+\)', '', text)'''

    '''#Removing instances (i), (ii), (iii)
    text = re.sub(r'\([i]{1,2,3}\)', '', text)

    #Removing instances (1), (2), (3)
    text = re.sub(r'\([\d]+\)', '', text)'''
        
    #Removing Mathemeatical formulaes using Latex like representation
    text = re.sub(r'[$].*[$]', '', text)

    #Removing XML Escape Characters
    text = re.sub(r'&amp;', '', text)
    text = re.sub(r'&lt;', ' ', text)
    text = re.sub(r'&gt;', ' ', text)
    text = re.sub(r'&quot;', '', text)
    text = re.sub(r'&apos;', '', text)
    
    #Lowering case the text
    text = text.lower()
        
    #Removing numbers
    text = re.sub(r'\d+', '', text)
    
    #Removing words of length 1
    text = re.sub(r'\b\w{1, 2}\b', '', text)
    
    #Removing - from pair of words
    text = text.replace('-', " ")
    
    #Removing punctuations
    text = text.translate(str.maketrans('', '', string.punctuation))

    #Removing stop words
    tokens = word_tokenize(text)
    text = ' '.join([ i for i in tokens if not i in stopwords])
    
    #Lemmatizing using POS Tags
    lemmatizer = WordNetLemmatizer()
    splitter = Splitter()
    lemmatization_using_pos_tagger = LemmatizationWithPOSTagger()

    tokens = splitter.split(text)    #step 1 split document into sentence followed by tokenization
    lemma_pos_token = lemmatization_using_pos_tagger.pos_tag(tokens)#step 2 lemmatization using pos tagger 
    try:
        tokens = [lemma_pos_token[0][i][1] for i in range(len(lemma_pos_token[0]))]
        text = ' '.join([token for token in tokens])
    except:
        pass

    #Removing stop words (post lemmatization)

    tokens = word_tokenize(text)
    text = ' '.join([ i for i in tokens if not i in stopwords])
   
    #Removing apostrophes
    text = text.replace('”', "")
    text = text.replace('“', "")
    
    return text

class Splitter(object):
    """
    split the document into sentences and tokenize each sentence
    """
    def __init__(self):
        self.splitter = nltk.data.load('tokenizers/punkt/english.pickle')
        self.tokenizer = nltk.tokenize.TreebankWordTokenizer()

    def split(self,text):
        """
        out : ['What', 'can', 'I', 'say', 'about', 'this', 'place', '.']
        """
        # split into single sentence
        sentences = self.splitter.tokenize(text)
        # tokenization in each sentences
        tokens = [self.tokenizer.tokenize(sent) for sent in sentences]
        return tokens


class LemmatizationWithPOSTagger(object):
    def __init__(self):
        pass
    def get_wordnet_pos(self,treebank_tag):
        """
        return WORDNET POS compliance to WORDENT lemmatization (a,n,r,v) 
        """
        if treebank_tag.startswith('J'):
            return wordnet.ADJ
        elif treebank_tag.startswith('V'):
            return wordnet.VERB
        elif treebank_tag.startswith('N'):
            return wordnet.NOUN
        elif treebank_tag.startswith('R'):
            return wordnet.ADV
        else:
            # As default pos in lemmatization is Noun
            return wordnet.NOUN

    def pos_tag(self,tokens):
        # find the pos tagginf for each tokens [('What', 'WP'), ('can', 'MD'), ('I', 'PRP') ....
        pos_tokens = [nltk.pos_tag(token) for token in tokens]
        lemmatizer = WordNetLemmatizer()
        # lemmatization using pos tagg   
        # convert into feature set of [('What', 'What', ['WP']), ('can', 'can', ['MD']), ... ie [original WORD, Lemmatized word, POS tag]
        pos_tokens = [ [(word, lemmatizer.lemmatize(word,self.get_wordnet_pos(pos_tag)), [pos_tag]) for (word,pos_tag) in pos] for pos in pos_tokens]
        return pos_tokens
    

