'''
Created on 3 Oct 2022

@author: maltaweel
'''

import os
import csv
from os import listdir
from random import randint
from random import seed

#get the patheay to the data
pn=os.path.abspath(__file__)
pn=pn.split("src")[0]

seed(1)
files={}
fieldnames = ['created_time','_id','positive','negative','neutral',
                  'compound','subjectivity','flair','flair score','aspect terms','aspect tb polarity',
                  'aspect tb subjectivity','aspect flair','sentence']

def loadData():
    
    #the data directory
    directory=os.path.join(pn,'results')
    
    outputs=[]          
   
    
    #now go through file(s) and begin cleaning text
    try:
        for f in listdir(directory):
           
            #open files
            with open(os.path.join(directory,f),'r') as csvfile:
                reader = csv.DictReader(csvfile)
            
                #go through the rows
                for row in reader:
                    neut=row['neutral']
                    pos=row['positive']
                    neg=row['negative']
                    sent=row['sentence']
                    tb_polarity=row['aspect tb polarity']
                    tb_sub=row['aspect tb subjectivity']
                    aspect=row['aspect flair']
                    
                    if (float(tb_polarity)==0.0 or float(tb_sub)==0.0 or 
                        float(aspect)==0.0):
                        continue

                    if len(sent)<5:
                        continue
                    
                    if (float(neut)>float(neg) and float(neut)>float(pos)):
                        continue
                    outputs.append(row)
                    
    
        files['sentiment_files_total.csv']=outputs
    #exception handling
    except IOError:
        print ("Could not read file:", csvfile)

def sampleData():
    
    for f in files:
        outputs=files[f]
        l=len(outputs)
        
        fileOutput=os.path.join(pn,'modified','sampled'+"_"+f)   
        with open(fileOutput, 'w') as csvf:
            
            #write the output
            writer = csv.DictWriter(csvf, fieldnames=fieldnames)

            writer.writeheader()  
            outs=[]
            for i in  range(0,500):
                print(i)
                value = randint(0, l)
                while value in outs:
                    value = randint(0, l)
                
                row=outputs[value]
            
                #write out row data        
                writer.writerow({'created_time': str(row['created_time']),
                    '_id':str(row['_id']),'positive':str(row['positive']),
                    'negative':str(row['negative']),'neutral':str(row['neutral']),'compound':str(row['compound']),
                    'subjectivity':str(row['subjectivity']),'flair':str(row['flair']),'flair score':str(row['flair score']),
                    'aspect terms':str(row['aspect terms']),'aspect tb polarity':str(row['aspect tb polarity']),
                    'aspect tb subjectivity':str(row['aspect tb subjectivity']), 'aspect flair':str(row['aspect flair']),'sentence':str(row['sentence'])})
            
                
        
            
        


'''
The main run method to run the cleanup module.
'''        
def run():
    #clean data
    loadData()
    sampleData()
    
    print('Finished')

#calls the run method
if __name__ == '__main__':
    run()