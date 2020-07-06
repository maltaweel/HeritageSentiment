'''
Approach that uses sentiment analysis using the Afinn library.  Sentiment is determined for individual tweets as well as in aggregate based
on days when tweets are available.


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
    
    #the Afinn setiment library
    afinn = Afinn()
    
    '''
    This determines the affinity (sentiment) score from a tweet.
    
    @param tweet- the tweet to score
    @return score- the sentiment score
    '''
    def get_affinity_score(self, tweet):
        
        # the score value
        score=0
        
        #score if the length of the tweet is at least 1
        if len(tweet)>0:
            score=self.afinn.score(tweet) / len(tweet)
            return score
        
        #otherwise no score
        else:
            return score
            
   
    '''
    Method to load csv data from the modified folder
    '''
    def loadData(self):
        
        #get the path for the modified and sentiment directories
        pn=os.path.abspath(__file__)
        pn=pn.split("src")[0]  
        directory=os.path.join(pn,'modified')
        output_directory=os.path.join(pn,'sentiment')

        #now read the files in the modified directory to get relevant files
        try:
            
            #iteratre through the directory
            for f in listdir(directory):
                rows=[]
                
                #skip non-csv files
                if '.csv' not in f:
                    continue
                
             
                #have containers for the data based on the twitter text, 
                texts=[]
                
                #date reference for tweet scores
                time={}
                
                #day-based reference to texts
                day={}
                
                #container for retweets over time
                retwts={}
                
                #open file to read
                with open(os.path.join(directory,f),'r') as csvfile:
                    reader = csv.DictReader(csvfile)
            
                    #read the rows
                    for row in reader:
                        
                        #get the tweet text
                        text=row['Text']
                        
                        #the date of the text
                        date_time=row['Datetime'].split(" ")[0]
                        
                        #covert to a date object (year-month-day)
                        date_time_obj = datetime.datetime.strptime(date_time, '%Y-%m-%d')
                        
                        #put date object in place of datetime in data
                        row['Datetime']=date_time_obj.date()
                        
                        #get retweets
                        retweets=int(row['Retweets'])
                        
                        #get sentiment score of tweet
                        score=self.get_affinity_score(text)
                        
                        #containers for text, sentiment and retweet data
                        inputT=[]
                        dd=[]
                        retweet=[]
                        
                        #see if current date exists in container
                        if  date_time_obj.date() in time:
                            
                            #organize information based on time
                            inputT=time[date_time_obj.date()]
                            dd=day[date_time_obj.date()]
                            
                            #score and text data
                            inputT.append(score)
                            dd.append(text)
                            
                            #retweet data
                            retweet=retwts[date_time_obj.date()]
                            retweet.append(retweets)
        
                        else:
                            
                            #if containers do not exist then add to new lists the sentiment, text, and retweet data
                            inputT.append(score)
                            dd.append(text)
                            retweet.append(retweets)
                        
                        #put data (tweets, sentiment score, and retweets) into dictionaries 
                        time[date_time_obj.date()]=inputT
                        day[date_time_obj.date()]=dd
                        retwts[date_time_obj.date()]=retweet
                        
                        #raw sentiment score for a tweet 
                        row['Score']=score
                        
                        #row data are put back to output to individual tweet data in the sentiment folder
                        rows.append(row)
                        
                        #tokenize words
                        twords=word_tokenize(text)
                        for tt in twords:
                            texts.append(tt)
                            
                #now do word counting to see top words in text
                word_counts = Counter(texts)
                
                #find the 100 most common words for all the data
                t=word_counts.most_common(100)
                
                #most common term output goes to the sentiment output directory
                self.most_common_output(t,os.path.join(output_directory,'common_100'+"_"+f))
                fle=os.path.join(output_directory,'sentiment'+"_"+f)       
                self.output(rows,fle)
                
                #call the date-based sentiment output
                self.doTimeBasedOutput(time,output_directory,day,retwts,f)
                
        except IOError:
            print ("Could not read file:", csvfile)
    '''
    Method to create time-based output for tweets.
    
    @param time- The day of when a given tweet is made
    @paramr- output_directory- the output directory which is the sentiment directory
    @param- day the day reference to associate with twitter data (retweets)
    @param- retwts represents the retweet data used
    @param- the file to output the results to.
    '''
    def doTimeBasedOutput(self,date,output_directory,day,retwts,f):
        
        #fieldnames to output
        fieldnames = ['Date','Mean Score','Median Score','Tweets', 'Retweets','Standard Deviation','Top 15']
        
        #the file output path
        fileOutput=os.path.join(output_directory,'sentiment_over_time'+"_"+f) 
        
        tts=[]
        with open(fileOutput, 'wt') as csvf:
            
            #write the output file
            writer = csv.DictWriter(csvf, fieldnames=fieldnames)
            
            #write the file header
            writer.writeheader() 
            for t in date:
                
                #do output based on date. Get the number of tweets, sentiment score, and number of retweets
                inpt=date[t]
                dd=day[t]
                rtweets=retwts[t]
                texts=[]

                #get the number of tweets
                n=len(dd)
                
                #get the most common terms for a given date
                for tt in dd:
                    twords=word_tokenize(tt)
                    for w in twords:
                        texts.append(w)
                        tts.append(w)
                
                #create a word counter
                word_counts = Counter(texts)
                
                #do word counts (top 15 terms for a date)
                z=word_counts.most_common(15)
                tz=[l for l, t in z]
                
                #get the mean sentiment score
                
                #get the standard deviation
                mean=np.mean(inpt)
                std=np.std(inpt)
                
                #get the median value
                median=np.median(inpt)
                
                #get the sum of retweets
                rts=np.sum(rtweets)
            
                writer.writerow({'Date': str(t),
                             'Mean Score':str(mean),'Median Score':str(median),'Tweets':str(n),
                             'Retweets':str(rts),'Standard Deviation':str(std),'Top 15': str(tz)})
        
       
   
   
        
    '''
    Method to output the most common terms.
    @param t- the term data for most common terms
    @param fileOutput- the file to output the results to
    '''
    def most_common_output(self,t,fileOutput):
        
        #fieldnames for the output file
        fieldnames=[]
        
        #the output data organized by the most common terms
        output={}
        for l, d in t:
            fieldnames.append(l)
            output[l]=d
           
            
        #write the output 
        with open(fileOutput, 'wt') as csvf:
            writer = csv.DictWriter(csvf, fieldnames=fieldnames)

            writer.writeheader()  
            writer.writerow(output)
           
    '''
    Method to output sentiment for individual tweets.
    @param data- the data for given tweets
    @param fileOutput- the file to output data
    '''   
    def output(self,data,fileOutput):
        
        #the fieldnames in the output file
        fieldnames = ['Datetime','ID','Score','Link','Text','Username','Retweets','Hashtags','Geolocation']
        with open(fileOutput, 'wt') as csvf:
            
            #write the output
            writer = csv.DictWriter(csvf, fieldnames=fieldnames)

            writer.writeheader()  
            
            #iterate through data rows and write out
            for f in data:
                writer.writerow({'Datetime': str(f['Datetime']),
                             'ID':str(f['ID']),'Score':str(f['Score']),'Link':str(f['Link']),
                             'Text':str(f['Text']),'Username':str(f['Username']),'Retweets':str(f['Retweets']),'Hashtags':str(f['Hashtags']),
                              'Geolocation':str(f['Geolocation'])})
    
    '''
    Method to run the sentiment analysis.
    '''
    def run(self):
        #load the data and run analysis
        self.loadData()
        
        #finished
        print('Finished')

if __name__ == '__main__':
    s=Sentiment()
    s.run()