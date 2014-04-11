import sys
import tweepy
import twitter_map_config
import webapp2

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
        haha = self.request.get("haha","hehe",0)
        try:
            res = self.api.get_status(haha)
            self.response.write(res.text)
        except:
            self.response.write("no such tweet")