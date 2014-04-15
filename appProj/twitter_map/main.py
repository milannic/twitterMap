#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import sys
sys.path.insert(0,'libs')
import tweepy
import os
import cgi
import json
import jinja2
import twitter_map_admin_test
import twitter_map_config
from datetime import datetime
import twitter_map_util



JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

#class tweetsDb()

class MainHandler(webapp2.RequestHandler):
    def __init__(self, request, response):
        self.initialize(request, response)
        self.auth = tweepy.OAuthHandler(twitter_map_config.consumer_key, twitter_map_config.consumer_secret)
        self.auth.set_access_token(twitter_map_config.access_token, twitter_map_config.access_token_secret)
        self.api = tweepy.API(self.auth)

    def get(self):
        #self.response.write(self.api.me().name)
        try:
            result = self.api.search("windows xp",count=100)

            template_values = {
                'tweets': result,
            }
            template = JINJA_ENVIRONMENT.get_template('index.html')
            self.response.write(template.render(template_values))
        except:
            self.response.write("have reached the rate limit for search")

class MapHandler(webapp2.RequestHandler):
    def __init__(self, request, response):
        self.initialize(request, response)

    def get(self):
        try:
            template = JINJA_ENVIRONMENT.get_template('map.html')
            self.response.write(template.render())

        except Exception, e:
            self.response.write(e)

class HotKeyHandler(webapp2.RequestHandler):
    def __init__(self, request, response):
        self.initialize(request, response)

    def get(self):
        try:
            keywords_dict = twitter_map_util.getHotKeyDict()
            self.response.out.write(json.dumps({'keywords_dict': keywords_dict}))

        except Exception, e:
            self.response.write(e)

class SearchHandler(webapp2.RequestHandler):
    def get(self):
        try:
            form = cgi.FieldStorage()
            keyword = ""
            startDate = ""
            endDate = ""
            if "keyword" in form:
                keyword = cgi.escape(form.getvalue('keyword'))
            if "startDate" in form:
                startDate = datetime.strptime(form.getvalue('startDate'),"%m/%d/%y %H:%M")
            if "endDate" in form:
                endDate = datetime.strptime(form.getvalue('endDate'),"%m/%d/%y %H:%M")
            tweets = twitter_map_util.getTweetByKeyword(keyword)
            tweets = twitter_map_util.filterTweetByDate(tweets,startDate,endDate)
            template_values = {
                'tweets': tweets,
            }
            self.response.out.write(json.dumps(template_values))

        except Exception, e:
            self.response.write(e)

class DisplayTweet(webapp2.RequestHandler):
    def get(self):
        try:
            form = cgi.FieldStorage()
            tid = ""
            if "tid" in form:
                tid = int(form.getvalue('tid'))
            tweet = twitter_map_util.getTweetByID(tid)
            template_values = {
                'tweet': tweet,
            }
            self.response.out.write(json.dumps(template_values))

        except Exception, e:
            self.response.write(e)

app = webapp2.WSGIApplication([
    #('/', MainHandler),
    ('/', MapHandler),
    ('/viewmap', MapHandler),
    ('/gethotkey',HotKeyHandler),
    ('/search', SearchHandler),
    ('/display', DisplayTweet),
    ('/testsingletweet',twitter_map_admin_test.GetSingleTweet),
    ('/testposttweet',twitter_map_admin_test.PostSingleTweet),
    ('/testgetdatastore',twitter_map_admin_test.GetTweetFromDatastore),
    ('/testposthotkey',twitter_map_admin_test.PostTopHotKey),
    ('/testcleardb',twitter_map_admin_test.DeleteAllTweetEntries),
    ('/testgql',twitter_map_admin_test.TestGql),
    ('/taskautograb',twitter_map_admin_test.TestAutoGrabTweets),
    ('/taskrecon',twitter_map_admin_test.TestReconstruct)
], debug=True)
