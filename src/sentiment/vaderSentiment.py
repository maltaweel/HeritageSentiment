'''
Created on Jan 28, 2021

@author: maltaweel
'''
import re
import os
from os import listdir

import csv
import flair, torch

from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk import word_tokenize

from textblob import TextBlob

from flair.models import TextClassifier
from flair.data import Sentence
from segtok.segmenter import split_single
import spacy
nlp = spacy.load("en_core_web_sm")

#spacy.prefer_gpu()
analyser = SentimentIntensityAnalyzer()

pn=os.path.abspath(__file__)
pn=pn.split("src")[0] 
data=os.path.join(pn,'models','best-model.pt')
classifier = TextClassifier.load('sentiment')

#English stop words
stop_words = set(stopwords.words('english')) 
flair.device = torch.device('cuda')

def sentiment_analyzer_scores(sentence):
    
    score = analyser.polarity_scores(sentence)
    return score

def tokenizer(text: str) -> str:
    "Tokenize input string using a spacy pipeline"
#    nlp = spacy.blank('en')
    
    tokenized_text = word_tokenize(text)
    tokenized_text = [w for w in tokenized_text  if not w in stop_words]
    tokenized_text = [w.strip() for w in tokenized_text]
    tokenized_text = [w for w in tokenized_text if not w==''] 
    tokenized_text = ' '.join(token for token in tokenized_text)
    
    text=text.replace(',','')
    text=text.replace('"','')
    text=text.replace('``','')
    text=text.replace(';','')
    text=text.replace(':', '')
    text=text.replace('&amp;', '')
    text=text.replace('.', '')
    text=text.replace('/', '')
    text=text.replace('[', '')
    text=text.replace('!', '')
    text=text.replace(']', '')
    text = text.replace('(', '') 
    text = text.replace(')', '')
    text = text.replace('?', '')
    text = text.replace("'", '')
 
    
    #nlp.add_pipe('sentencizer')  # Very basic NLP pipeline in spaCy
    #doc = nlp(text)
    
    #tokenized_text = ' '.join(token.text for token in doc)
    #tokenized_text = [w for w in tokenized_text if len(w) > 2]
    
    return text

def scoreFlair(text, model):
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
    model.eval()
    model.predict(sentence)
    
    return sentence.labels

def textAspect(aspects):
    asps=[]
    for aspect in aspects:
        text=aspect['description']
        if text=='':
            continue
        aspect['blob_sentiment'] = TextBlob(text).sentiment
        aspect['flair_sentiment']=scoreFlair(text, classifier)
        asps.append(aspect)
   #    print(aspect)
    aspectOut=output_aspect(asps)
    return aspectOut

def output_aspect(asps):
    result={}
    text=''
    blob_subj=0.0
    blob_polar=0.0
    flair_sent=0.0
    
    n=0
    for i in asps:
        text+=i['description']+'/'
        sentiment=i['blob_sentiment']
        blob_polar+=sentiment.polarity
        blob_subj+=sentiment.subjectivity
        flair=i['flair_sentiment']
        
        dd=flair[0]._value.split(',')[0]
        sd=flair[0].score
        if dd=='NEGATIVE':
            sd=-sd
        flair_sent+=sd
        n+=1
    
    if n>0:
        blob_subj=blob_subj/float(n)
        blob_polar=blob_polar/float(n)
        flair_sent=flair_sent/float(n)
    
    result['description']=text
    result['blob_subjective']=blob_subj
    result['blob_polarity']=blob_polar
    result['flair_sentiment']=flair_sent
    
    return result
    
def aspectMine(sentence):
    aspect = []
    doc = nlp(sentence)
    descriptive_term = ''
    target = ''
    for token in doc:
        if token.dep_ == 'nsubj' and token.pos_ == 'NOUN':
            target = token.text
        if token.pos_ == 'ADJ':
            prepend = ''
            for child in token.children:
                if child.pos_ != 'ADV':
                    continue
                prepend += child.text + ' '
            descriptive_term = prepend + token.text
        if descriptive_term=='':
            continue
        aspect.append({'aspect': target,
            'description': descriptive_term})
    
    return aspect

def make_sentences(text):
    """ Break apart text into a list of sentences """
    sentences = [sent for sent in split_single(text)]
    return sentences

def main() -> None:
   
    pn=os.path.abspath(__file__)
    pn=pn.split("src")[0]
    
    file_read=os.path.join(pn,'modified')
        
    fieldnames = ['created_time','_id','positive','negative','neutral',
                  'compound','subjectivity','flair','flair score','aspect terms','aspect tb polarity',
                  'aspect tb subjectivity','aspect flair','sentence']
    
 
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
                    text=row['sentence']
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
                            flair=scoreFlair(te,classifier)
                            te=te.replace('\n',' ')
                            aspect=aspectMine(te)
                            asps=textAspect(aspect)
                            printData['aspect']=asps
                            
#                           exp = explainer.explainer('fasttext', data, text, 1000)
                            #p=exp.score
                            
                            printData['positive']=score['pos']
                            printData['negative']=score['neg']
                            printData['neutral']=score['neu']
                            printData['subjectivity']=scoreS
                            
                            if flair is None or len(flair)<0:
                                continue
                            
                            try:
                                dd=flair[0]._value.split(',')[0]
                                sd=flair[0].score
                                if dd=='NEGATIVE':
                                    sd=-sd
                                
                            
                            except IndexError:
                                print(flair)
                                continue
                                
                            printData['flair']=dd
                            printData['flair_score']=sd
                            printData['compound']=score['compound']
                            printData['created_time']=row['created_time']
                            try:
                                printData['_id']=row['_id']
                            except:
                                printData['_id']=row['from_id']
                            
                            printData['sentence']=te
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
    result=f['aspect']
    
    asptext=result['description']
    blob_subj=result['blob_subjective']
    blob_polar=result['blob_polarity']
    flair_sent=result['flair_sentiment']
    
        #write out row data        
    writer.writerow({'created_time': str(f['created_time']),
            '_id':str(f['_id']),'positive':str(f['positive']),
            'negative':str(f['negative']),'neutral':str(f['neutral']),'compound':str(f['compound']),
            'subjectivity':str(f['subjectivity']),'flair':str(f['flair']),'flair score':str(f['flair_score']),
            'aspect terms':asptext,'aspect tb polarity':str(blob_polar),'aspect tb subjectivity':str(blob_subj),
            'aspect flair':str(flair_sent),'sentence':str(f['sentence'])})
        
if __name__ == "__main__":
    # Evaluation text
    
    main()
    
    print("Finished") 
