'''
Module for creating a world cloud of data in the HeritageScrape/modified folder.

Created on Jun 28, 2020

@author: mark
'''
import os
import sys
import csv
from os import listdir
import datetime

import numpy as np
import pandas as pd
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

import matplotlib.pyplot as plt

class Wordcloud():

    def loadData(self, start, end):
        pn=os.path.abspath(__file__)
        pn=pn.split("src")[0]  
        directory=os.path.join(pn,'modified')
      

       
        try:
            for f in listdir(directory):
                
                texts=''
                if '.csv' not in f:
                    continue
                
             
                
                with open(os.path.join(directory,f),'r') as csvfile:
                    reader = csv.DictReader(csvfile)
            
                    for row in reader:
                        text=row['Text']
                        date_time=row['Datetime'].split(" ")[0]
                        
                        date_time_obj = datetime.datetime.strptime(date_time, '%Y-%m-%d')
                        
                        st = datetime.datetime.strptime(start, '%Y-%m-%d')
                        ed = datetime.datetime.strptime(end, '%Y-%m-%d')
                        
                        row['Datetime']=date_time_obj.date()
                        
                        if st<=date_time_obj:
                            if  ed>date_time_obj:
                                texts+=" "+text
                       
                self.wordCloud(texts)
        except IOError:
            print ("Could not read file:", csvfile)
    
       
    def wordCloud(self,text):
       
        # Create and generate a word cloud image:
        wordcloud = WordCloud().generate(text)

        #   Display the generated image:
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()
        
    def run(self, argv):
        self.loadData(argv[1],argv[2])
        print('Finished')

if __name__ == '__main__':
    wc=Wordcloud()
    wc.run(sys.argv)