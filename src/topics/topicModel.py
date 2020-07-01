'''
Created on Jul 1, 2020

@author: mark
'''
import sys
import csv
import os
from os import listdir

def loadData(self):
        pn=os.path.abspath(__file__)
        pn=pn.split("src")[0]  
        directory=os.path.join(pn,'modified')
        
        try:
            for f in listdir(directory):
                rows=[]
                
                if '.csv' not in f:
                    continue
                
                with open(os.path.join(directory,f),'r') as csvfile:
                    reader = csv.DictReader(csvfile)
            
                    for row in reader:
                        text=row['Text']
                        
        except IOError:
            print ("Could not read file:", csvfile)               
                        
'''
Method to run the module
'''           
def run(argv):

    since_date = argv[1]
    until_date = argv[2]

   
 

    print('Finished')
   
if __name__ == '__main__':
    run(sys.argv)