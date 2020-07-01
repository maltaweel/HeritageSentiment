'''
Created on Jul 1, 2020

@author: mark
'''
import sys
import csv
import os
from os import listdir

import datetime

from nltk.tokenize import RegexpTokenizer as word_tokenize
from gensim.models import CoherenceModel, LdaModel, HdpModel

import re
import pyLDAvis.gensim
import gensim
from gensim.utils import lemmatize
from gensim.corpora import Dictionary

pn=os.path.abspath(__file__)
pn=pn.split("src")[0]

class TopicModel():
    
    def process_texts(self, texts):
        bigram = gensim.models.Phrases(texts) 
 
        
    
        texts = [bigram[line] for line in texts]
        texts = [[word.split('/')[0] for word in lemmatize(' '.join(line), allowed_tags=re.compile('(NN)'), min_length=3)] for line in texts]

        dictionary = Dictionary(texts)
        corpus = [dictionary.doc2bow(text) for text in texts]
        
        return corpus, dictionary
        
        
    def loadData(self,start,end):
        pn=os.path.abspath(__file__)
        pn=pn.split("src")[0]  
        directory=os.path.join(pn,'modified')
        
        rows=[]
        try:
            for f in listdir(directory):
                
                
                if '.csv' not in f:
                    continue
                
                with open(os.path.join(directory,f),'r') as csvfile:
                    reader = csv.DictReader(csvfile)
            
                    for row in reader:
                        text=row['Text']
                        date=row['Datetime'].split(" ")[0]
                        
                        date_time_obj = datetime.datetime.strptime(date, '%Y-%m-%d')
                        start_d=datetime.datetime.strptime(start, '%Y-%m-%d')
                        end_d=datetime.datetime.strptime(end, '%Y-%m-%d')
                        
                        date=date_time_obj.date()
                        startD=start_d.date()
                        endD=end_d.date()
                        
                        if date>=startD:
                            if date<endD:
                                text_t = word_tokenize(text)
                                rows.append(text_t)       
                        
                        
        except IOError:
            print ("Could not read file:", csvfile)               
        
        return rows
    
    '''Output results of the analysis
        i-- the topic number
        model-- the model used (e.g., lda, hdp)
    '''
    def printResults(self,i,results,model):
        
        
        #os.chdir('../')
        
        filename=os.path.join(pn,'topic_model_results','analysis_results_'+model+str(i)+".csv")
        
        fieldnames = ['Topic','Term','Value']
        
        
        with open(filename, 'wb') as csvf:
            writer = csv.DictWriter(csvf, fieldnames=fieldnames)

            writer.writeheader()
            
            for key in results:
                v=results[key]
                tn=key.split(":")[0]
                kt=key.split(":")[1]
                writer.writerow({'Topic':str(tn),'Term': str(kt.encode("utf-8")),'Value':str(v)})
    
    def runModels(self,number_of_topics, corpus, dictionary):
        
        #hdp model
        hdpmodel = HdpModel(corpus=corpus, id2word=dictionary)

        hdpmodel.show_topics()

        hdptopics = hdpmodel.show_topics(num_topics=number_of_topics)

    #   result_dict=addTotalTermResults(hdptopics)
            
        #add results to total kept in a list     
    #   addToResults(result_dict)
    
        self.printResults(number_of_topics,hdptopics,'hdp')
        
     
        #lda model
        ldamodel = LdaModel(corpus=corpus, num_topics=number_of_topics, id2word=dictionary)
       
        ldamodel.save('lda'+number_of_topics+'.model')
        ldatopics = ldamodel.show_topics(num_topics=number_of_topics)
    
    #    result_dict=addTotalTermResults(ldatopics)    
    #   addToResults(result_dict)
        self.printResults(number_of_topics,ldatopics,'lda')
    
    
        visualisation2 = pyLDAvis.gensim.prepare(ldamodel, corpus, dictionary)
   
        location=os.path.join(pn,'results')
     
        #visualize outputs
        pyLDAvis.save_html(visualisation2, os.path.join(location,'LDA_Visualization'+str(number_of_topics)+'.html')) 
'''
Method to run the module
'''           
def run(argv):
    tm=TopicModel()
    number_of_topics = argv[1]
    start=argv[2]
    end=argv[3]
    texts=tm.loadData(start,end)
    corpus, dictionary=tm.process_text(texts)
    tm.runModels(number_of_topics,corpus, dictionary)
    
    
    print('Finished')
   
if __name__ == '__main__':
    run(sys.argv)