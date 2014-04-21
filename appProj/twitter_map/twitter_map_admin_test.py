import twitter_map_config
import twitter_map_db_model
import twitter_map_util
import webapp2
import json
import os
import cgi
import cgitb
import jinja2
from google.appengine.ext import ndb
from google.appengine.ext import db
from datetime import datetime

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

cgitb.enable()
#used for test


class GetSingleTweet(webapp2.RequestHandler):

    def get(self):
        haha = self.request.get("haha","hehe",0)
        try:
            res = twitter_map_config.twitter_api.get_status(454332406921580544)
            self.response.write(res.text)
        except:
            self.response.write("no such tweet")


class PostSingleTweet(webapp2.RequestHandler):

    def post(self):
        try:
            tweet_data = json.loads(self.request.body)
            tweet_ins = twitter_map_db_model.Tweet()
            #so longitude is at first
    #        tweet_data['coordinates']['coordinates'][0]
    #        #so latitude is the second
    #        tweet_data['coordinates']['coordinates'][1]
            tweet_ins.text = tweet_data['text'].encode('utf-8')
            hot_key_list = twitter_map_util.parseTweet(tweet_data['text'])
            tweet_ins.hk = hot_key_list
            tweet_ins.location = ndb.GeoPt(float(tweet_data['coordinates']['coordinates'][1]),float(tweet_data['coordinates']['coordinates'][0]))
            tweet_ins.tid = int(tweet_data['id'])
            tweet_ins.uid = int(tweet_data['user']['id'])
            tweet_ins.uname = tweet_data['user']['screen_name']
            ts = datetime.strptime(tweet_data['created_at'],'%a %b %d %H:%M:%S +0000 %Y')
            tweet_ins.date = ts
            tweet_ins.put()
            self.response.write("haha")
        except Exception,e:
            self.response.write(e)


class GetTweetFromDatastore(webapp2.RequestHandler):
    def get(self):
        haha = self.request.get("type","haha",0)
        try:
            q = twitter_map_db_model.Tweet.query().order(twitter_map_db_model.Tweet.uid)
            template_values = {
                'tweets': q,
            }
            template = JINJA_ENVIRONMENT.get_template('tweets.html')
            self.response.write(template.render(template_values))
        except Exception,e:
            self.response.write(e)




class PostTopHotKey(webapp2.RequestHandler):

    def post(self):
        try:
            hot_key_data = json.loads(self.request.body)
            hot_key_ins = twitter_map_db_model.HotKeyList()
            #print hot_key_data
            count = 0
            for ele in hot_key_data:
                hot_key_ins = twitter_map_db_model.HotKeyList()
                hot_key_ins.hid = count
                hot_key_ins.text = ele[0]
                hot_key_ins.count = ele[1]
                hot_key_ins.put()
                count = count+1
            self.response.write("haha")
        except Exception,e:
            self.response.write(e)
            #self.response.write("server internal error")


class DeleteAllTweetEntries(webapp2.RequestHandler):
    def get(self):
        try:
            ndb.delete_multi(twitter_map_db_model.Tweet.query().fetch(keys_only=True))
            self.response.write('succeed')
        except Exception,e:
            self.response.write(e)


class TestAutoGrabTweets(webapp2.RequestHandler):
    def get(self):
        res=twitter_map_util.getAndSaveTweet(100,2)
        self.response.write(res)


class TestReconsKeyWord(webapp2.RequestHandler):
    def get(self):
        res = twitter_map_util.reConstructHotKeyInfo()
        self.response.write(res)

class TestGql(webapp2.RequestHandler):
    def get(self):
        q = ndb.gql("SELECT hk FROM Tweet")
        global_dict = {}
        for p in q:
            if global_dict.has_key(p.hk[0]):
                global_dict[p.hk[0]] = global_dict[p.hk[0]]+1
            else:
                global_dict[p.hk[0]] = 1
        #print global_dict
        sorted_dict = sorted(global_dict.items(),key=lambda x:x[1])
        real_len = len(sorted_dict) and twitter_map_config.key_word_length>len(sorted_dict) or twitter_map_config.key_word_length
        sorted_dict = sorted_dict[len(sorted_dict)-real_len:len(sorted_dict)]
        print sorted_dict
        self.response.write("haha")


class TestReconstruct(webapp2.RequestHandler):


    def get(self):
        self.response.write("We are processing,so you don't need to worry about that")
        twitter_map_util.reConstructHotKeyInfo()

