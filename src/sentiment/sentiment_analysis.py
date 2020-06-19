'''
Created on Jun 18, 2020

@author: mark
'''
import os
from os import listdir

import csv

class Sentiment:

    def loadData(self):
        pn=os.path.abspath(__file__)
        pn=pn.split("src")[0]  
        directory=os.path.join(pn,'modified')

        try:
            for f in listdir(directory):
                rows=[]
                with open(os.path.join(directory,f),'r') as csvfile:
                    reader = csv.DictReader(csvfile)
            
                    for row in reader:
                        text=row['Text']
                        
    
        except IOError:
            print ("Could not read file:", csvfile)
    
    def run(self):
        self.loadData()

if __name__ == '__main__':
    s=Sentiment()
    s.run()