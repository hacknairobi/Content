#!/usr/bin/env python
# encoding: utf-8

import tweepy #https://github.com/tweepy/tweepy
import csv # Write csv files
import argparse # Use this to pass username arguments from teh commandline
import config # Save our credentials in a separate file for security
 
# Twitter only allows access to a users most recent 3240 tweets with this method

def get_all_tweets(screen_name):
    
    #authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
    auth.set_access_token(config.access_key, config.access_secret)
    api = tweepy.API(auth)
     
    #initialize a list to hold all the tweepy Tweets
    alltweets = []  
     
    #make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name = screen_name,count=200)
     
    #save most recent tweets
    alltweets.extend(new_tweets)
     
    #save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1
     
    #keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print("\tGetting tweets before %s" % (oldest))
         
        #all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)

         
        #save most recent tweets
        alltweets.extend(new_tweets)
         
        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1
         
        print("\t...%s tweets downloaded so far" % (len(alltweets)))
        # transform the tweepy tweets into a 2D array that will populate the csv
        outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]
                 
        #write the csv
        with open('datasets/{}_tweets.csv'.format(screen_name), 'a') as f:
                writer = csv.writer(f)
                #writer.writerow(["id","created_at","text"])
                writer.writerows(outtweets)
                #pass
 
 
if __name__ == '__main__':

        # Parse the supplied usernames
        parser = argparse.ArgumentParser(description='Harvest tweets for certain people')
        parser.add_argument('--username', metavar='u', type=str, nargs='*',
                        help='Enter the twitter handle you wish to download from')

        args = parser.parse_args()
        # print(args.username)

        for username in args.username:
                try:
                        #pass in the username of the account you want to download
                        print("\nGetting @{}'s tweets\n".format(username))
                        get_all_tweets(username)
                except:
                        print('\tError! Failed to fetch tweets for {}'.format(username))
         


