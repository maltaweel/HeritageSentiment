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
    pattern = re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
                          
    files={}
    try:
        for f in listdir(directory):
            rows=[]
            with open(os.path.join(directory,f),'r') as csvfile:
                reader = csv.DictReader(csvfile)
            
            
                for row in reader:
                    text=row['Text']
                    
                    
                    
                    text=text.lower()
                    text=re.sub('(\\b[A-Za-z] \\b|\\b [A-Za-z]\\b)', '', text)
                    text=pattern.sub("",text)
                    
                    word_tokens = word_tokenize(text) 
                    
                    
                    filtered_sentence = [w for w in word_tokens if not w in stop_words]
                    filtered_sentence = [w for w in filtered_sentence if not w.startswith("@")]
                    filtered_sentence = [w for w in filtered_sentence if not w.startswith("http")]
                    
                
                                         
                    words = [w.replace('(', '') for w in filtered_sentence]
                    words = [w.replace(')', '') for w in words]
                    words = [w.replace('?', '') for w in words]
                    words = [w.replace(',', '') for w in words]
                    words = [w.replace("'", '') for w in words]
                    words = [w.replace('"', '') for w in words]
                    words = [w.replace('!', '') for w in words]
                    words = [w.replace(':', '') for w in words]
                    words = [w.replace('&amp;', '') for w in words]
                    words = [w.replace('.', '') for w in words]
                    words = [w.replace('/', '') for w in words]
                    words = [w.replace('[', '') for w in words]
                    words = [w.replace(']', '') for w in words] 
                    words = [w for w in words if len(w) > 2]
                        
                    w = " ".join(words)

                    row['Text']=w
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
                             'Text':str(f['Text']),'Username':str(f['Username']),'Retweets':str(f['Retweets']),'Hashtags':str(f['Hashtags']),
                              'Geolocation':str(f['Geolocation'])})
    
        
def run():
    cleanData()
    print('Finished')

if __name__ == '__main__':
    run()