'''
The main module used for topic modelling.
Topic models include latent Dirichlet allocation (LDA) and Hierarchical Dirichlet Process (HDP).

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

#use this as the starting pathway (the src folder)
pn=os.path.abspath(__file__)
pn=pn.split("src")[0]

#the world lemmatizer to lemmatize words
lemmatizer = WordNetLemmatizer()

class TopicModel():
    
    '''
    Simple method to prepocess text using gensim
    '''
    def first_process(self,texts):

        for t in texts:
            t=yield gensim.utils.simple_preprocess(t, deacc=True, min_len=3)
    
    
    '''
    Method to process text and lemmatize.
    
    @param fullt_text- the full text to create bigram
    @param texts- texts to analyze for topic models and process using lemmatization.
    
    @return corpus- the corpus of text to analyze
    @return dictionary- the term dictionary to match against
    '''       
    def process_text(self, full_text, texts):
        
        #develop bigram
        bigram = gensim.models.Phrases(full_text, min_count=5, threshold=100) # higher threshold fewer phrases.
        bigram = gensim.models.phrases.Phraser(bigram)
 #      trigram = gensim.tsmodels.phrases.Phraser(full_text, threshold=100)
        
        #get texts from bigram
        texts = [bigram[line] for line in texts]
  #     texts = [[word.split('/')[0] for word in lemmatize(' '.join(line), allowed_tags=re.compile('(NN)'), min_length=3)] for line in texts]
  #      texts_lemma = ' '.join([lemmatizer.lemmatize(w) for w in texts])
        
        #get lemmaztized words
        texts_lemma=[]
        for line in texts:
            for word in line:
                l=lemmatizer.lemmatize(word)
                texts_lemma.append(l)
        
        #create dictionary
        texts_lemma = [d.split() for d in texts_lemma]
        dictionary = Dictionary(texts_lemma)
        
        #create the corpus
        corpus = [dictionary.doc2bow(text) for text in texts_lemma]
        
        return corpus, dictionary
        
    '''
    Method to load text data based on a start and end data.
    
    @param start- the start date to load text
    @param end- the end date to load text
    '''  
    def loadData(self,start,end):
        
        #the pathway to the data to analyze
        directory=os.path.join(pn,'modified')
        
        rows=[]
        
        #get the text file from the directory
        try:
            for f in listdir(directory):
                
                
                if '.csv' not in f:
                    continue
                
                #open the text
                with open(os.path.join(directory,f),'rt') as csvfile:
                    
                    #get the reader
                    reader = csv.DictReader(csvfile)
            
                    #get single reader
                    for row in reader:
                        
                        #get text
                        text=row['Text'] #.decode('utf-8')
                        
                        #get date
                        date=row['Datetime'].split(" ")[0]
                        
                        #get dates (start and end)
                        date_time_obj = datetime.datetime.strptime(date, '%Y-%m-%d')
                        start_d=datetime.datetime.strptime(start, '%Y-%m-%d')
                        end_d=datetime.datetime.strptime(end, '%Y-%m-%d')
                        
                        date=date_time_obj.date()
                        startD=start_d.date()
                        endD=end_d.date()
                        
                        if date>=startD:
                            if date<endD:
                                rows.append(text)       
                        
        # the exception handling           
        except IOError:
            print ("Could not read file:", csvfile)               
        
        return rows
    
    """
    Method for using a coherence model to look at topic coherence for LDA models.
    
    @param dictionary- Gensim dictionary
    @param corpus- Gensim corpus
    @param limit- topic limit
    
    @return lm_list- List of LDA topic models
    @return c_v- Coherence values corresponding to the LDA model with respective number of topics
    """
    def evaluate_graph(self, dictionary, corpus, texts, limit):
    
        c_v = []
        lm_list = []
        
        #topic models made using LDA with the models analyzed using UMASS method coherence test
        for num_topics in range(1, (limit*2)+1):
            lm = LdaModel(corpus=corpus, num_topics=num_topics, id2word=dictionary,alpha="auto")
            lm_list.append(lm)
            cm = CoherenceModel(model=lm, texts=[texts], corpus=corpus, coherence='u_mass')
            c_v.append(cm.get_coherence())
            del cm
            
        return lm_list, c_v

    '''
    Method to print csv output results of the evaluations conducted 
    
    @param modList- the model evaluated
    @param results- the result scores
    @param i- the index output desired
    @param start- the start date
    @param end- the end date
    '''
    def printEvaluation(self,modList,results,i,start,end):
       
        filename=os.path.join(pn,'topic_model_results','evaluationTotal'+str(i)+"_"+start+"_"+end+".csv")   
        
        fieldnames = ['Model','Score']
    
        with open(filename, 'w') as csvf:
                writer = csv.DictWriter(csvf, fieldnames=fieldnames)

                writer.writeheader()
                for t in range(0,len(modList)):
        
                    writer.writerow({'Model':str(modList[t]),'Score': str(results[t])})
                
    '''
    Method to output results of the analysis.
    
    @param i- the topic number
    @param results- the results from the model
    @param model- the model used (e.g., lda, hdp) to output
    @param start- the start date
    @param end- the end date
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
    
    '''
    Method to run the topic models (lda and hdp).
    @param number_of_topics- the number of topics
    @param corpus- the corpus of text
    @param dictionary- the dictionary of terms
    @param start- the start date
    @param end- the end date
    '''
    def runModels(self,number_of_topics, corpus, dictionary,start,end):
        
        #do hdp model
        hdpmodel = HdpModel(corpus=corpus, id2word=dictionary)
        
        hdpmodel.print_topics(num_topics=int(number_of_topics), num_words=10)
        hdptopics = hdpmodel.show_topics(num_topics=int(number_of_topics))

    #   result_dict=addTotalTermResults(hdptopics)
            
        #add results to total kept in a list     
    #   addToResults(result_dict)
    
        #output results
        self.printResults(number_of_topics,hdptopics,'hdp',start,end)
        
        #d lda model
        ldamodel = LdaModel(corpus=corpus, num_topics=number_of_topics, id2word=dictionary,passes=20,iterations=400)
       
        ldamodel.save('lda'+number_of_topics+'.model')
        ldatopics = ldamodel.show_topics(num_topics=int(number_of_topics))
    
    #   result_dict=addTotalTermResults(ldatopics)    
    #   addToResults(result_dict)
        self.printResults(number_of_topics,ldatopics,'lda',start,end)
    
    
        visualisation = pyLDAvis.gensim.prepare(ldamodel, corpus, dictionary)
   
        location=os.path.join(pn,'topic_model_results')
     
        #visualize outputs in html
        pyLDAvis.save_html(visualisation, os.path.join(location,'LDA_Visualization'+str(number_of_topics)+"_"+start+
                                                        "_"+end+'.html')) 
        
        
        
'''
Method to run the module.

@param argv- the runtime argument
'''           
def run(argv):
    
    #get run arguments
    tm=TopicModel()
    number_of_topics = argv[1]
    start=argv[2]
    end=argv[3]
    
    #load and process text
    original_texts=tm.loadData(start,end)
    texts=tm.first_process(original_texts)
    corpus, dictionary=tm.process_text(original_texts,texts)
    
    #run topic models
    tm.runModels(number_of_topics,corpus, dictionary,start,end)
    
    #output coherence model
    lmlist, c_v=tm.evaluate_graph(dictionary, corpus, original_texts, int(number_of_topics))
    tm.printEvaluation(lmlist,c_v,number_of_topics,start,end)
    
    print('Finished')

#run the module
if __name__ == '__main__':
    run(sys.argv)