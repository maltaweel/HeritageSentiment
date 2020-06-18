'''
Created on Jun 18, 2020

@author: mark
'''
import os
from os import listdir

import csv
import re
import nltk
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
from nltk.tokenize import RegexpTokenizer
import fileinput




stop_words = set(stopwords.words('english')) 

def cleanData():
    pn=os.path.abspath(__file__)
    pn=pn.split("src")[0]  
    directory=os.path.join(pn,'results')
    output_directory=os.path.join(pn,'modified')
    
    files={}
    try:
        for f in listdir(directory):
            rows=[]
            with open(os.path.join(directory,f),'r') as csvfile:
                reader = csv.DictReader(csvfile)
            
                for row in reader:
                    text=row['Text']
                    
                    
                    row['Text']=text
                    
                    text=text.lower()
                    text=re.sub('(\\b[A-Za-z] \\b|\\b [A-Za-z]\\b)', '', text)
                    
                    word_tokens = word_tokenize(text) 
  
                    filtered_sentence = [w for w in word_tokens if not w in stop_words] 
                    tokenizer = RegexpTokenizer(r'\w+')
                    
                    tokens=[]
                    for f in filtered_sentence:
                        if '#' in f:
                            continue
                        if 'https:' in f:
                            continue
                        f=tokenizer.tokenize(f)[0]
                        tokens.append(f+" ")
                    
                    text=""
                    text=text.join(tokens)
                    
                    row['Text']=text
                    rows.append(row)
                
                fle=os.path.join(output_directory,'modified'+"_"+f)   
                output(rows,fle)  
                  
            files[f]=rows      
    
    except IOError:
        print ("Could not read file:", csvfile)

def output(data,fileOutput):
    fieldnames = ['Datetime','ID','Link','Text','Username','Retweets','Hashtags','Geolocation']
    with open(fileOutput, 'wt') as csvf:
        writer = csv.DictWriter(csvf, fieldnames=fieldnames)

        writer.writeheader()  
        
        for f in data:
            writer.writerow({'Datetime': str(f['Datetime']),
                             'ID':str(f['ID']),'Link':str(f['Link']),
                             'Text':str(f['Text']),'Username':str(f['Retweets']),'':str(f['Hashtags']),
                              'Geolocation':str(f['Geolocation'])})
    
        
def run():
    cleanData()
    print('Finished')

if __name__ == '__main__':
    run()