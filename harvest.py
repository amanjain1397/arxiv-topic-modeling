from sickle import Sickle
from sickle.iterator import OAIResponseIterator
import pickle

from datetime import date
from dateutil.relativedelta import relativedelta

import os


def oai_harvester_response(metadataPrefix = 'oai_dc', harvest_set = 'cs'):    
    
    sickle = Sickle('http://export.arxiv.org/oai2', iterator = OAIResponseIterator)
            
    try:
        with open('./pkl/harvest/today.pickle', 'rb') as handle:
            today = pickle.load(handle)
            
            if(today!= str(date.today())):
                responses = sickle.ListRecords(**{'metadataPrefix' : metadataPrefix, 'set' : harvest_set,
                                          'from': today, 'until' : str(date.today() - relativedelta(days = 1))})
                handle.close()
                
            else:
                print('The records are already present till yesterday!')
                responses = None
    
    except FileNotFoundError:
            responses = sickle.ListRecords(**{'metadataPrefix' : metadataPrefix, 'set' : harvest_set})
                                             #,'from' : str(date.today)})
                
    except NoRecordsMatchError:
        responses = None
        print('There are no more records to be updated!')
        
    return responses

def oai_harvester_dumper(responses):   
    try:
        with open('./pkl/harvest/flag.pickle', 'rb') as handle1, open('./pkl/harvest/today.pickle', 'rb') as handle2:
            flag = pickle.load(handle1)
            today = pickle.load(handle2)
            handle1.close()
            handle2.close()
            
            if((today!= str(date.today())) & (responses!= None)):
                try:
                    while(True):
                        flag = flag + 1
                        with open('./xml/response' + str(flag) + '.xml', 'w') as fp:
                            raw = responses.next().raw
                            if(raw != None):
                                fp.write(raw)
                                print('Wrote #', flag)
                            else:
                                continue

                except StopIteration:
                    # if StopIteration is raised, break from loop
                    with open('./pkl/harvest/today.pickle', 'wb') as handle:
                        pickle.dump(str(date.today()), handle, protocol=pickle.HIGHEST_PROTOCOL)
                        handle.close()
                    with open('./pkl/harvest/flag.pickle', 'wb') as handle:
                        pickle.dump(flag-1, handle, protocol=pickle.HIGHEST_PROTOCOL)
                        handle.close()
                    os.remove('./xml/response' + str(flag) + '.xml')
                    return
            else:
                print('No responses exists to dump!' )
                
                
    except:
        flag = -1
        print('Here')
        
        if(responses!= None):
            try:
                while(True):
                    flag = flag + 1
                    with open('./xml/response' + str(flag) + '.xml', 'w') as fp:

                        raw = responses.next().raw
                        #print(raw)

                        if(raw != None):
                            fp.write(raw)
                            print('Wrote ', flag, '.xml')

            except StopIteration:
                    # if StopIteration is raised, break from loop
                if(flag > -1):
                    os.remove('./xml/response' + str(flag) + '.xml')

                with open('./pkl/harvest/today.pickle', 'wb') as handle:
                    pickle.dump(str(date.today()), handle, protocol=pickle.HIGHEST_PROTOCOL)
                    handle.close()

                with open('./pkl/harvest/flag.pickle', 'wb') as handle:
                    pickle.dump(flag-1, handle, protocol=pickle.HIGHEST_PROTOCOL)
                    handle.close()
                return
        else:
                 print('No responses exists to dump!' )
