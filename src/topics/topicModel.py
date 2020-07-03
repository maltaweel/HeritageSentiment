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
from nltk.stem import WordNetLemmatizer
from gensim.models import CoherenceModel, LdaModel, HdpModel

import re
import pyLDAvis.gensim
import gensim
from gensim.utils import lemmatize
from gensim.corpora import Dictionary

pn=os.path.abspath(__file__)
pn=pn.split("src")[0]
lemmatizer = WordNetLemmatizer()

class TopicModel():
    
    def first_process(self,texts):

        for t in texts:
            t=yield gensim.utils.simple_preprocess(t, deacc=True, min_len=3)
            
    def process_text(self, full_text, texts):
            
        bigram = gensim.models.Phrases(full_text, min_count=5, threshold=100) # higher threshold fewer phrases.
        bigram = gensim.models.phrases.Phraser(bigram)
 #      trigram = gensim.tsmodels.phrases.Phraser(full_text, threshold=100)
         
        texts = [bigram[line] for line in texts]
  #     texts = [[word.split('/')[0] for word in lemmatize(' '.join(line), allowed_tags=re.compile('(NN)'), min_length=3)] for line in texts]
  #      texts_lemma = ' '.join([lemmatizer.lemmatize(w) for w in texts])
        
        texts_lemma=[]
        for line in texts:
            for word in line:
                l=lemmatizer.lemmatize(word)
                texts_lemma.append(l)
        
        texts_lemma = [d.split() for d in texts_lemma]
        dictionary = Dictionary(texts_lemma)
        
        corpus = [dictionary.doc2bow(text) for text in texts_lemma]
        
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
                
                with open(os.path.join(directory,f),'rt') as csvfile:
                    reader = csv.DictReader(csvfile)
            
                    for row in reader:
                        text=row['Text'] #.decode('utf-8')
                        date=row['Datetime'].split(" ")[0]
                        
                        date_time_obj = datetime.datetime.strptime(date, '%Y-%m-%d')
                        start_d=datetime.datetime.strptime(start, '%Y-%m-%d')
                        end_d=datetime.datetime.strptime(end, '%Y-%m-%d')
                        
                        date=date_time_obj.date()
                        startD=start_d.date()
                        endD=end_d.date()
                        
                        if date>=startD:
                            if date<endD:
                                rows.append(text)       
                        
                        
        except IOError:
            print ("Could not read file:", csvfile)               
        
        return rows
    
    """
    Method for using a coherence model to look at topic coherence for LDA models.
    
    Parameters:
    ----------
    dictionary-- Gensim dictionary
    corpus-- Gensim corpus
    limit-- topic limit
    
    Returns:
    -------
    lm_list : List of LDA topic models
    c_v : Coherence values corresponding to the LDA model with respective number of topics
    """
    def evaluate_graph(self, dictionary, corpus, texts, limit):
    
        c_v = []
        lm_list = []
        for num_topics in range(1, limit*2):
            lm = LdaModel(corpus=corpus, num_topics=num_topics, id2word=dictionary)
            lm_list.append(lm)
            cm = CoherenceModel(model=lm, texts=texts, dictionary=dictionary, coherence='c_v')
            c_v.append(cm.get_coherence())
            del cm
            
        return lm_list, c_v

    '''
    Method to print csv output results of the evaluations conducted 
    modList-- the model evaluated
    results-- the result scores
    i-- the index output desired
    '''
    def printEvaluation(self,modList,results,i,start,end):
       
        filename=os.path.join(pn,'topic_model_results','evaluationTotal'+str(i)+"_"+start+"_"+end+".csv")   
        
        fieldnames = ['Model','Score']
    
        with open(filename, 'w') as csvf:
                writer = csv.DictWriter(csvf, fieldnames=fieldnames)

                writer.writeheader()
                for i in range(0,len(modList)):
        
                    writer.writerow({'Model':str(modList[i]),'Score': str(results[i])})
                
    '''
    Output results of the analysis
    i-- the topic number
    model-- the model used (e.g., lda, hdp)
    '''
    def printResults(self,i,results,model,start,end):

        filename=os.path.join(pn,'topic_model_results','analysis_results_'+model+str(i)+"_"+start+"_"+
                              end+".csv")
        
        fieldnames = ['Topic','Term','Value']

        with open(filename, 'w') as csvf:
            writer = csv.DictWriter(csvf, fieldnames=fieldnames)

            writer.writeheader()
            
            for l in results:
                n=l[0]
                v=l[1]
                vvs=v.split("+")
                for vv in vvs:
                    vvt=vv.split("*")
                    if len(vvt)<2:
                        continue
                    t=vvt[1]
                    val=vvt[0]
                    writer.writerow({'Topic':str(n),'Term': str(t.encode("utf-8")),'Value':str(val)})
    
    
    def runModels(self,number_of_topics, corpus, dictionary,start,end):
        
        #hdp model
        hdpmodel = HdpModel(corpus=corpus, id2word=dictionary)
        
        hdpmodel.print_topics(num_topics=int(number_of_topics), num_words=10)
        hdptopics = hdpmodel.show_topics(num_topics=int(number_of_topics))

    #   result_dict=addTotalTermResults(hdptopics)
            
        #add results to total kept in a list     
    #   addToResults(result_dict)
    
        #output results
        self.printResults(number_of_topics,hdptopics,'hdp',start,end)
        
        #lda model
        ldamodel = LdaModel(corpus=corpus, num_topics=number_of_topics, id2word=dictionary,passes=20,iterations=400)
       
        ldamodel.save('lda'+number_of_topics+'.model')
        ldatopics = ldamodel.show_topics(num_topics=int(number_of_topics))
    
    #   result_dict=addTotalTermResults(ldatopics)    
    #   addToResults(result_dict)
        self.printResults(number_of_topics,ldatopics,'lda',start,end)
    
    
        visualisation2 = pyLDAvis.gensim.prepare(ldamodel, corpus, dictionary)
   
        location=os.path.join(pn,'topic_model_results')
     
        #visualize outputs
        pyLDAvis.save_html(visualisation2, os.path.join(location,'LDA_Visualization'+str(number_of_topics)+"_"+start+
                                                        "_"+end+'.html')) 
        
        
        
'''
Method to run the module
'''           
def run(argv):
    
    #get run arguments
    tm=TopicModel()
    number_of_topics = argv[1]
    start=argv[2]
    end=argv[3]
    
    #load and process text
    texts=tm.loadData(start,end)
    full_text=texts
    texts=tm.first_process(texts)
    corpus, dictionary=tm.process_text(full_text,texts)
    
    #run topic models
    tm.runModels(number_of_topics,corpus, dictionary,start,end)
    
    #output coherence model
    lmlist, c_v=tm.evaluate_graph(dictionary, corpus, texts, int(number_of_topics))
    tm.printEvaluation(lmlist,c_v,number_of_topics,start,end)
    
    print('Finished')
   
if __name__ == '__main__':
    run(sys.argv)