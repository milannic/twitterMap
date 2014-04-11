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
import jinja2
import twitter_map_admin_test
import twitter_map_config

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
        template = JINJA_ENVIRONMENT.get_template('map.html')
        self.response.write(template.render())

    def post(self):
        keyword = cgi.escape(self.request.get('keyword'))
        template_values = {
            'keyword': keyword,
        }
        template = JINJA_ENVIRONMENT.get_template('map.html')
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/viewmap', MapHandler),
    ('/testsingletweet',twitter_map_admin_test.UploadSingleTweet)
], debug=True)
