import numpy as np
from sickle import Sickle
from sickle.iterator import OAIResponseIterator
import pickle

from datetime import date
from dateutil.relativedelta import relativedelta

import os
import re
from .preprocess_text import preprocess_text, Splitter, LemmatizationWithPOSTagger 

#shorthands
OAI = '{http://www.openarchives.org/OAI/2.0/}'
OAI2 = '{http://www.openarchives.org/OAI/2.0/oai_dc/}'
PURL = '{http://purl.org/dc/elements/1.1/}'

class Harvester():

    def __init__(self, endpoint = 'http://export.arxiv.org/oai2',
                 metadataPrefix = 'oai_dc', harvest_set = 'cs',
                 recsFrom = str(date.today() - relativedelta(days = 1)),
                 recsUntil = ''):
        
        self.endpoint = endpoint
        self.metadataPrefix = metadataPrefix
        self.harvest_set = harvest_set
        self.recsFrom = recsFrom
        if not recsUntil:
            self.recsUntil = date.today()
        else: 
            self.recsUntil = recsUntil    
        #self.recsUntil = recsUntil
        
        self.responses = None
        self.recs = []
        
        self.idfiers = []
        self.descriptions = []

        self.sickle = Sickle(endpoint, iterator = OAIResponseIterator)

    def responseCollector(self):
        try:
            responses = self.sickle.ListRecords(**{'metadataPrefix' : self.metadataPrefix, 
                                            'set' : self.harvest_set,
                                            'from': self.recsFrom,
                                            'until': self.recsUntil})
        except Exception as err:
            
            if(type(err).__name__ == 'NoRecordsMatch'):
                print('NoRecordsMatch : No records match the paramaters specified for this selective harvesting request.')
                responses = None
                
            if (type(err).__name__ == 'BadResumptionToken'):
                print('BadResumptionToken : Bad date values, must have from<=until')
                responses = None
            
        self.responses = responses
        
    def recordCollector(self):
        
        if(self.responses):
            recs = []
            try:
                while True:
                    raw = self.responses.next()
                    if raw:
                        recs.append(raw)
            except StopIteration:
                pass
            
            self.recs = recs
            
    def createCorpus(self):
        
        #Each rec is a .xml file
        for rec in self.recs:

            #each item denotes a research paper
            items = [item for item in rec.xml.findall('./' + OAI + 'ListRecords/')]            
            
            #Get id of each paper
            self.idfiers.extend([self.returnIds(item) for item in items][:-1])
            
            #Get description each paper
            self.descriptions.extend([self.returnDescrip(item) for item in items][:-1])
        
        assert(len(self.idfiers) == len(self.descriptions))

    @staticmethod
    def returnIds(item):
        try:
            idfier = item.findall('./'+ OAI + 'header/' + OAI + 'identifier')[0].text
        except:
            idfier = ''
        #print(idfier)
        return idfier
    
    @staticmethod
    def returnDescrip(item):
    
        description = ''

        for metadata in item.findall('./' + OAI + 'metadata'):
            for dc in metadata.findall('./' + OAI2 + 'dc'):

                i = 0
                for descrip in dc.findall('./' + PURL + 'description'):
                    i += 1
                    if(i == 1):
                        description = re.sub('\\n', ' ', descrip.text)
                        description = preprocess_text(description).split()

        return description
            
if __name__ == "__main__":
    h = Harvester(recsFrom = '2019-11-05')
    h.responseCollector()
    h.recordCollector()
    h.createCorpus()
    print(len(h.idfiers))



            
            

