'''
Module to scrape twitter data. User provide inputer parameters that include:

1) a text query to search in twitter, 2) the maximum number of tweets to scrape,
3) the date to start a search, 4) the date to end a search


Created on Jun 13, 2020

@author: mark
'''
import os
import sys
import GetOldTweets3 as got
import pandas as pd

'''
 Method that pulls tweets from a specific username and turns to csv file.

@param username- the username 
@param count- maximum number of most recent tweets to pull from
'''
def username_tweets_to_csv(username, count):
    # Creation of query object
    tweetCriteria = got.manager.TweetCriteria().setUsername(username)\
                                            .setMaxTweets(count)
    # Creation of list that contains all tweets
    tweets = got.manager.TweetManager.getTweets(tweetCriteria)

    # Creating list of chosen tweet data
    user_tweets = [[tweet.date, tweet.text] for tweet in tweets]

    # Creation of dataframe from tweets list
    tweets_df = pd.DataFrame(user_tweets, columns = ['Datetime', 'Text'])

    # Converting dataframe to CSV
    tweets_df.to_csv('{}-{}k-tweets.csv'.format(username, int(count/1000)), sep=',')
    
# Function that pulls tweets based on a general search query and turns to csv file

'''
Method to apply a text querty based on start and end date and maximum amount.

@param text_query- the query being searched
@param since_date- the date to begin a search
@param util_date- the date to end a search (but not including)
@param count- maximum number of most recent tweets to pull from
'''
def text_query_to_csv(text_query, since_date, until_date, count):
    
    pn=os.path.abspath(__file__)
    pn=pn.split("src")[0]  
    
    path=os.path.join(pn,'output')

    # Creation of query object
    tweetCriteria = got.manager.TweetCriteria().setQuerySearch(text_query).setSince(since_date).setUntil(until_date).setMaxTweets(count)
    
    # Creation of list that contains all tweets
    tweets = got.manager.TweetManager.getTweets(tweetCriteria)
    
    # Creating list of chosen tweet data
    text_tweets = [[tweet.date, tweet.id,tweet.permalink,tweet.text, tweet.retweets, tweet.hashtags,tweet.username,tweet.geo] for tweet in tweets]
    
    # Creation of dataframe from tweets
    tweets_df = pd.DataFrame(text_tweets, columns = ['Datetime', 'Id','Link','Text','Retweets','Hashtags','Username','Geolocation'])

    # Converting tweets dataframe to csv file
    tweets_df.to_csv(path+'/{}-{}k-tweets.csv'.format(text_query, int(count/1000)), sep=',')
    
'''
Method to run the module

@param argv- the input arguments to execute the run
'''           
def run(argv):

    # Max recent tweets pulls x amount of most recent tweets from user
    text_query = argv[1]
    count = int(argv[2])

    since_date = argv[3]
    until_date = argv[4]

    # Calling function to query X amount of relevant tweets and create a CSV file
    text_query_to_csv(text_query, since_date, until_date, count)

    print('Finished')
   
if __name__ == '__main__':
    run(sys.argv)
       
