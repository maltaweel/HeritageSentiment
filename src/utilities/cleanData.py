'''
Module used to clean Twitter data.

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



#English stop words
stop_words = set(stopwords.words('english')) 

'''
Main method to remove stop words, short (2-letter words or less), and clean text.
'''
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
                    
                    #block of filters to clean sentences
                    #removes stop words, @ symbol, http, and various punctuation listed
                    filtered_sentence = [w for w in word_tokens if not w in stop_words]
                    filtered_sentence = [w for w in filtered_sentence if not w.startswith("@")]
                    filtered_sentence = [w for w in filtered_sentence if not w.startswith("http")]
                    filtered_sentence = [w for w in filtered_sentence if " amp " not in w]
                    
                    #removal of commas, punctuations, brackets, 
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
                    
                    #re-add cleaned words to tweet text    
                    w = " ".join(words)

                    #add text to the dictionary and then the row
                    row['Text']=w
                    rows.append(row)
                
                #call the output of the clean data
                fle=os.path.join(output_directory,'modified'+"_"+f)   
                output(rows,fle)  
                  
            files[f]=rows      
    
    #exception handling
    except IOError:
        print ("Could not read file:", csvfile)

'''
Method to output the cleaned data.
@param fileOutput- the file output directory
'''
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
    
'''
The main run method to run the cleanup module.
'''        
def run():
    #clean data
    cleanData()
    
    print('Finished')

#calls the run method
if __name__ == '__main__':
    run()