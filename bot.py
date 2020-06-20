import os
import time
import tweepy
import random

SLEEP_TIME = 600

def get_random_sentence_from_file():
    with open('lyrics.txt', encoding="utf8") as f:
        lines = f.read().splitlines()
    return random.choice(lines)


def twitter_api():
    keys_file = open("keys.txt")
    lines = keys_file.readlines()
    consumer_key = lines[0].rstrip()
    consumer_secret = lines[1].rstrip()
    access_token = lines[2].rstrip()
    access_token_secret = lines[3].rstrip()

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    return api

api = twitter_api()
for tweet in tweepy.Cursor(api.search, q='#twentyonepilots').items():
    follow = 0
    try:
        print('\nTweet by: @' + tweet.user.screen_name)
        #tweet.retweet()
        #print('Retweeted the tweet')
        # Favorite the tweet
        tweet.favorite()
        print('Favorited the tweet')
        #Follow the user who tweeted
        #check that bot is not already following the user
        if not tweet.user.following:
            tweet.user.follow()
            print('Followed the user')
            follow +=1
        if (follow==5):
            tweet_text = str(get_random_sentence_from_file())
            tweet_text = tweet_text.replace('\\n','\n') + '\n#twentyonepilots'
            print(tweet_text)
            api.update_status(status=tweet_text)
            print("status Upadate Successfull")
            follow = 0
        time.sleep(SLEEP_TIME)

    except tweepy.TweepError as e:
        print(e.reason)

    except StopIteration:
        break