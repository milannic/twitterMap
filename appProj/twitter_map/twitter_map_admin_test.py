import sys
import tweepy
import twitter_map_config
import twitter_map_db_model
import webapp2
import json
from datetime import datetime
from google.appengine.api import images
import time

#used for test


class UploadSingleTweet(webapp2.RequestHandler):
    def __init__(self, request, response):
        self.initialize(request, response)
        self.auth = tweepy.OAuthHandler(twitter_map_config.consumer_key, twitter_map_config.consumer_secret)
        self.auth.set_access_token(twitter_map_config.access_token, twitter_map_config.access_token_secret)
        self.api = tweepy.API(self.auth)

    def get(self):
        haha = self.request.get("haha","hehe",0)
        try:
            res = self.api.get_status(haha)
            self.response.write(res.text)
        except:
            self.response.write("no such tweet")


class PostSingleTweet(webapp2.RequestHandler):
    def __init__(self, request, response):
        self.initialize(request, response)
        self.auth = tweepy.OAuthHandler(twitter_map_config.consumer_key, twitter_map_config.consumer_secret)
        self.auth.set_access_token(twitter_map_config.access_token, twitter_map_config.access_token_secret)
        self.api = tweepy.API(self.auth)

    def post(self):
        tweet_data = json.loads(self.request.body)
        tweet_ins = twitter_map_db_model.Tweet()

#        print tweet_data['created_at']
#        print tweet_data['text']
#        print tweet_data['id']
#        print tweet_data['user']['id']
#        print tweet_data['user']['screen_name']
        #so longitude is at first
#        print tweet_data['coordinates']['coordinates'][0]
#        #so latitude is the second
#        print tweet_data['coordinates']['coordinates'][1]
        tweet_ins.text = tweet_data['text']
        tweet_ins.hk0 = 0
        tweet_ins.hk1 = 0
        tweet_ins.hk2 = 0
        tweet_ins.hk3 = 0
        tweet_ins.hk4 = 0
        tweet_ins.hk5 = 0
        tweet_ins.hk6 = 0
        tweet_ins.longitude = float(tweet_data['coordinates']['coordinates'][0])
        tweet_ins.latitude = float(tweet_data['coordinates']['coordinates'][1])
        tweet_ins.tid = int(tweet_data['id'])
        tweet_ins.uid = int(tweet_data['user']['id'])
        tweet_ins.uname = tweet_data['user']['screen_name']
        ts = datetime.strptime(tweet_data['created_at'],'%a %b %d %H:%M:%S +0000 %Y')
        tweet_ins.date = ts
        tweet_ins.put()

        try:
            self.response.write("haha")
        except:
            self.response.write("no such tweet")
