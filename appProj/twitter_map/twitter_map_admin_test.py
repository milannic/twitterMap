import twitter_map_config
import twitter_map_db_model
import twitter_map_util
import webapp2
import json
import os
import cgi
import jinja2
from google.appengine.ext import ndb
from google.appengine.ext import db
from datetime import datetime

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

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


class QueryTweet():
    @classmethod
    def getByKeyword(self, keyword):
        try:
            tweets = twitter_map_db_model.Tweet.query(twitter_map_db_model.Tweet.hk0 == 0).order(twitter_map_db_model.Tweet.uid)
            return tweets;

        except Exception, e:
            print e


class MapHandler(webapp2.RequestHandler):
    def __init__(self, request, response):
        self.initialize(request, response)

    def get(self):
        try:
            result = QueryTweet.getByKeyword('')
            tweets = []
            for t in result:
                tweet = {"uid":t.uid, "uname":t.uname, "lat":t.location.lat, "lon":t.location.lon, "date":t.date.strftime("%Y-%m-%d %H:%M:%S"), "text":t.text, "hk0":t.hk0,
                             "hk1":t.hk1, "hk2":t.hk2, "hk3":t.hk3, "hk4":t.hk4, "hk5":t.hk5, "hk6":t.hk6}
                tweets.append(json.dumps(tweet))
            template_values = {
                'tweets': tweets,
            }
            template = JINJA_ENVIRONMENT.get_template('map.html')
            self.response.write(template.render(template_values))

        except Exception, e:
            self.response.write(e)


    # def post(self):
    #     keyword = cgi.escape(self.request.get('keyword'))
    #     try:
    #         tweets = QueryTweet.getByKeyword(keyword)
    #         template_values = {
    #             'keyword': keyword,
    #             'tweets': tweets,
    #         }
    #         template = JINJA_ENVIRONMENT.get_template('map.html')
    #         self.response.write(template.render(json.dumps(template_values)))
    #
    #     except Exception, e:
    #         self.response.write(e)


class PostTopHotKey(webapp2.RequestHandler):

    def post(self):
        try:
            hot_key_data = json.loads(self.request.body)
            hot_key_ins = twitter_map_db_model.HotKeyList()
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