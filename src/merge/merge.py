import os

import csv


'''
Method to load data from input files in the totalData folder.
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

    dates,ids,links,texts,usernames,retweets,hashtags,locations=loadData()
    printResults(dates,ids,links,texts,usernames,retweets,hashtags,locations)
    print("Finished")
   
if __name__ == '__main__':
    run()