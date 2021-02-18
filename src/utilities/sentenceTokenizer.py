'''
Created on Feb 18, 2021

@author: maltaweel
'''
import os
from os import listdir

import csv
from nltk.tokenize import sent_tokenize


'''
Method to output the cleaned text data.
@param results- the results to output
@param fileOutput- the file output directory
'''
def output(results,fileOutput):
    #the fieldnames or title of columns for the output file
    fieldnames = ['from_id','from_name_id','created_time','sentence']
    
    #output file
    with open(fileOutput, 'wt') as csvf:
        writer = csv.DictWriter(csvf, fieldnames=fieldnames)

        #write the header
        writer.writeheader()  
        
        for f in results:
            sentences=f['sentences']
            for sent in sentences:
                s=str(sent)
                writer.writerow({'from_id': str(f['from_id']),'from_name_id':str(f['from_name_id']),
                         'created_time': str(f['created_time']),'sentence':s})                  
           
           
def tokenize(text):
    texts=sent_tokenize(text)    
    
    return texts  

def openData():
    #get the pathway to the data
    pn=os.path.abspath(__file__)
    pn=pn.split("src")[0]
    
    #the data directory
    directory=os.path.join(pn,'results')
    
    #output directory for cleaned file
    output_directory=os.path.join(pn,'modified')
    
    #now go through file(s) and begin cleaning text
    try:
        for f in listdir(directory):
        
            #open files
            with open(os.path.join(directory,f),'r',encoding="ISO-8859-1") as csvfile:
                
                reader = csv.DictReader(csvfile)
    
                results=[]
                
                print(f)
                
                #go through the rows
                for row in reader:
                    data={}
                    message=row['message']
                    try:
                        from_id=row['from_id']
                    except:
                        from_id=''
                    try:
                        from_name=row['from_name']
                    except:
                        from_name=row['_id']
                        
                    created_time=row['created_time']
                    
                    texts=tokenize(message)
                    
                    data['sentences']=texts
                    data['from_id']=from_id
                    data['from_name_id']=from_name
                    data['created_time']=created_time
                    results.append(data)
                    
                mod_f=f.split('.csv')[0]
                mod_f=mod_f+'_sentences.csv'
                
                fileOutput=os.path.join(output_directory,mod_f)
                    
                output(results,fileOutput)
    
    #exception handling
    except IOError:
        print ("Could not read file:", csvfile)  
                 
'''
The main run method to run the cleanup module.
'''        
def run():
    #clean data
    openData()
    
    print('Finished')

#calls the run method
if __name__ == '__main__':
    run()                                         