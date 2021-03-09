'''
Created on Jan 28, 2021

@author: maltaweel
'''
import re
import os
from os import listdir

import csv
import spacy

from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob

from flair.models import TextClassifier
from flair.data import Sentence

classifier = TextClassifier.load('en-sentiment')
analyser = SentimentIntensityAnalyzer()

pn=os.path.abspath(__file__)
pn=pn.split("src")[0] 
data=os.path.join(pn,'models/fasttext','sst5.ftz')

from segtok.segmenter import split_single

def sentiment_analyzer_scores(sentence):
    
    score = analyser.polarity_scores(sentence)
    return score

def tokenizer(text: str) -> str:
    "Tokenize input string using a spaCy pipeline"
    nlp = spacy.blank('en')
    text=text.replace('.','')
    text=text.replace('"','')
    
    nlp.add_pipe(nlp.create_pipe('sentencizer'))  # Very basic NLP pipeline in spaCy
    doc = nlp(text)
    tokenized_text = ' '.join(token.text for token in doc)
    tokenized_text=tokenized_text+' .'
    return tokenized_text

def scoreFlair(text):
    result = re.sub("<[a][^>]*>(.+?)</[a]>", 'Link.', text)
    result = re.sub('&gt;', "", result)
    result = re.sub('&#x27;', "'", result)
    result = re.sub('&quot;', '"', result)
    result = re.sub('&#x2F;', ' ', result)
    result = re.sub('<p>', ' ', result)
    result = re.sub('</i>', '', result)
    result = re.sub('&#62;', '', result)
    result = re.sub('<i>', ' ', result)
    result = re.sub("\n", '', result)
    
    sentence = Sentence(result)
    classifier.predict(sentence)
    
    return sentence.labels

def make_sentences(text):
    """ Break apart text into a list of sentences """
    sentences = [sent for sent in split_single(text)]
    return sentences

def main() -> None:
   
    pn=os.path.abspath(__file__)
    pn=pn.split("src")[0]
    
    file_read=os.path.join(pn,'results')
        
    fieldnames = ['created_time','_id','positive','negative','neutral',
                  'compound','subjectivity','flair','message']
    
 
    for f in listdir(file_read):
        name=f.split('.csv')[0]
        fileOutput=os.path.join(pn,"sentiment","sentiment_classification"
                                +'_'+name+'.csv')
        
        with open(fileOutput, 'w') as csvf:
            
            #write the output
            writer = csv.DictWriter(csvf, fieldnames=fieldnames)

            writer.writeheader()  
            
            
        #open file to read

            with open(os.path.join(file_read,f),'r',encoding="ISO-8859-1") as csvfile:
                reader = csv.DictReader(csvfile)
            
                
                #read the rows
                for row in reader:
                    
                    #output data
                    printData={}
                
                    #get the tweet text
                    text=row['message']
                    sent=make_sentences(text)
                    i=0
                    
                    for te in sent:
                        try:
                            te = tokenizer(te)  # Tokenize text using spaCy before explaining
                            if te=='':
                                continue
                            #print("Generating LIME explanation for example {}: `{}`".format(i+1, text))
                        
                        
                            score = sentiment_analyzer_scores(te)
                            scoreS=TextBlob(te).sentiment.subjectivity
                            flair=scoreFlair(te)
                            te=te.replace('\n',' ')
#                           exp = explainer.explainer('fasttext', data, text, 1000)
                            #p=exp.score
                            printData['positive']=score['pos']
                            printData['negative']=score['neg']
                            printData['neutral']=score['neu']
                            printData['subjectivity']=scoreS
                            printData['flair']=flair
                            printData['compound']=score['compound']
                            printData['created_time']=row['created_time']
                            try:
                                printData['_id']=row['_id']
                            except:
                                printData['_id']=row['from_id']
                            
                            printData['message']=te
                            output(writer,printData)
                            i+=1
                        
                        except ValueError as err:
                            print(err)
                            continue
                            
                    
                print(f)    
            csvf.close()
            
'''
    Method to output sentiment for individual tweets.
    @param data- the data for given tweets
    @param fileOutput- the file to output data
'''                 
def output(writer,f):
        #write out row data        
        writer.writerow({'created_time': str(f['created_time']),
            '_id':str(f['_id']),'positive':str(f['positive']),
            'negative':str(f['negative']),'neutral':str(f['neutral']),'compound':str(f['compound']),
            'subjectivity':str(f['subjectivity']),'flair':str(f['flair']),'message':str(f['message'])})
        
if __name__ == "__main__":
    # Evaluation text
    
    main()
    
    print("Finished") 