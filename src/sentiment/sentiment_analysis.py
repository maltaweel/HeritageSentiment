'''
Created on Jun 18, 2020

@author: mark
'''
import os
import numpy as np
from os import listdir
import collections
from collections import Counter
from nltk.tokenize import word_tokenize 
import datetime

import csv

from afinn import Afinn
from sklearn.metrics.cluster.tests.test_supervised import score_funcs


class Sentiment:
    afinn = Afinn()
    def get_affinity_score(self, tweet):
        
        score=0
        
        if len(tweet)>0:
            score=self.afinn.score(tweet) / len(tweet)
            return score
        else:
            return score
            
   
   
    def loadData(self):
        pn=os.path.abspath(__file__)
        pn=pn.split("src")[0]  
        directory=os.path.join(pn,'modified')
        output_directory=os.path.join(pn,'sentiment')

        try:
            for f in listdir(directory):
                rows=[]
                
                if '.csv' not in f:
                    continue
                
             
                texts=[]
                time={}
                day={}
                with open(os.path.join(directory,f),'r') as csvfile:
                    reader = csv.DictReader(csvfile)
            
                    for row in reader:
                        text=row['Text']
                        date_time=row['Datetime'].split(" ")[0]
                        
                        date_time_obj = datetime.datetime.strptime(date_time, '%Y-%m-%d')
                        row['Datetime']=date_time_obj.date()
                        score=self.get_affinity_score(text)
                        
                        inputT=[]
                        dd=[]
                        if  date_time_obj.date() in time:
                            inputT=time[date_time_obj.date()]
                            dd=day[date_time_obj.date()]
                            inputT.append(score)
                            dd.append(text)
        
                        else:
                            inputT.append(score)
                            dd.append(text)
                        
                        time[date_time_obj.date()]=inputT
                        day[date_time_obj.date()]=dd
                        
                        row['Score']=score
                        
                        rows.append(row)
                        
                        twords=word_tokenize(text)
                        for tt in twords:
                            texts.append(tt)
                
                word_counts = Counter(texts)
                
                t=word_counts.most_common(100)
                
                self.most_common_output(t,os.path.join(output_directory,'common_100'+"_"+f))
                fle=os.path.join(output_directory,'sentiment'+"_"+f)       
                self.output(rows,fle)
                
                self.doTimeBasedOutput(time,output_directory,day,f)
                
        except IOError:
            print ("Could not read file:", csvfile)
    
    def doTimeBasedOutput(self,time,output_directory,day,f):
        fieldnames = ['Date','Mean Score','Median Score','Tweets','Standard Deviation','Top 15']
        fileOutput=os.path.join(output_directory,'sentiment_over_time'+"_"+f) 
        
        with open(fileOutput, 'wt') as csvf:
            writer = csv.DictWriter(csvf, fieldnames=fieldnames)
            writer.writeheader() 
            for t in time:
                inpt=time[t]
                dd=day[t]
                texts=[]

                n=len(dd)
                for tt in dd:
                    twords=word_tokenize(tt)
                    for w in twords:
                        texts.append(w)
                
                word_counts = Counter(texts)
                
                z=word_counts.most_common(15)
                tz=[l for l, t in z]
                mean=np.mean(inpt)
                std=np.std(inpt)
                median=np.median(inpt)
            
                writer.writerow({'Date': str(t),
                             'Mean Score':str(mean),'Median Score':str(median),'Tweets':str(n),
                             'Standard Deviation':str(std),'Top 15': str(tz)})
        
    def most_common_output(self,t,fileOutput):
        
        fieldnames=[]
        
        output={}
        for l, d in t:
            fieldnames.append(l)
            output[l]=d
           
            
        
        with open(fileOutput, 'wt') as csvf:
            writer = csv.DictWriter(csvf, fieldnames=fieldnames)

            writer.writeheader()  
            writer.writerow(output)
           
        
    def output(self,data,fileOutput):
        fieldnames = ['Datetime','ID','Score','Link','Text','Username','Retweets','Hashtags','Geolocation']
        with open(fileOutput, 'wt') as csvf:
            writer = csv.DictWriter(csvf, fieldnames=fieldnames)

            writer.writeheader()  
        
            for f in data:
                writer.writerow({'Datetime': str(f['Datetime']),
                             'ID':str(f['ID']),'Score':str(f['Score']),'Link':str(f['Link']),
                             'Text':str(f['Text']),'Username':str(f['Username']),'Retweets':str(f['Retweets']),'Hashtags':str(f['Hashtags']),
                              'Geolocation':str(f['Geolocation'])})
    
    def run(self):
        self.loadData()
        print('Finished')

if __name__ == '__main__':
    s=Sentiment()
    s.run()