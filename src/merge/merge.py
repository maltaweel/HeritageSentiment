'''
Module to merge data from scraped twitter data.

Created on Jun 13, 2020

@author: mark
'''

import os

import csv


'''
Method to load data from input files in the output folder. Method merges files in the folder, keeping all the data columns and removing duplicate values.

@return dates- the date of tweets
@return ids- the user ids
@return links- the links of tweets
@return texts- the texts (or tweets)
@return usernames- the username data
@return retweets- the retweet data
@return hashtags- the hashtag data
@return locations- the location data
'''
def loadData():
    
    #This code changes the current directory so relative paths are used
    pn=os.path.abspath(__file__)
    pn=pn.split("src")[0]
    pathway=os.path.join(pn,'output')
    
    texts=[]
    dates=[]
    usernames=[]
    retweets=[]
    hashtags=[]
    locations=[]
    ids=[]
    links=[]
    
  
    for fil in os.listdir(pathway):
        with open(os.path.join(pathway,fil),'rU') as csvfile:
            reader = csv.DictReader(csvfile)
            print(csvfile)
       
            for row in reader:   
                date=row['Datetime']
                text=row['Text']
                iid=row['Id']
                link=row['Link']
                username=row['Username']
                hashtag=row['Hashtags']
                retweet=row['Retweets']

                location=row['Geolocation']
                

                if text in texts and date in dates:
                    continue
                
                else:
                    dates.append(date)
                    usernames.append(username)
                    locations.append(location)
                    texts.append(text)
                    retweets.append(retweet)
                    hashtags.append(hashtag)
                    ids.append(iid)
                    links.append(link)
                        
          
                
                
    return dates,ids,links,texts,usernames,retweets,hashtags,locations    

'''
Method to print the results of the output
'''                   
def printResults(dates,ids,links,texts,usernames,retweets,hashtags,locations):

    fieldnames = ['Datetime','ID','Link','Text','Username','Retweets','Hashtags','Geolocation']
    pn=os.path.abspath(__file__)
    pn=pn.split("src")[0]
    fileOutput=os.path.join(pn,'results',"totalTweets.csv")
    
    with open(fileOutput, 'w') as csvf:
        writer = csv.DictWriter(csvf, fieldnames=fieldnames)

        writer.writeheader()      
    
        for i in range(0,len(texts)):
   
            writer.writerow({'Datetime':str(dates[i]),'ID':str(ids[i]),'Link':str(links[i]),'Text':str(texts[i]),'Username':str(usernames[i]),'Retweets':str(retweets[i]),
                             'Hashtags':str(hashtags[1]),'Geolocation':str(locations[i])})
                    
'''
Method to run the module
'''           
def run():

    #load data and get different data
    dates,ids,links,texts,usernames,retweets,hashtags,locations=loadData()
    
    #print results
    printResults(dates,ids,links,texts,usernames,retweets,hashtags,locations)
    
    print("Finished")
   
if __name__ == '__main__':
    run()