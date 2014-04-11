import twitter_map_config
import twitter_map_db_model
import twitter_map_util
import webapp2
import json
from google.appengine.ext import ndb
from datetime import datetime

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
            #self.response.write("server internal error")
