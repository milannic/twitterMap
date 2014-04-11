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

import jinja2
import twitter_map_admin_test
import twitter_map_config

#class tweetsDb()


class MainHandler(webapp2.RequestHandler):
    def get(self):
        #self.response.write(self.api.me().name)
        try:
            result = twitter_map_config.twitter_api.search("windows xp",count=100)
            for ele in result:
                self.response.write(ele.text)
        except:
            self.response.write("have reached the rate limit for search")

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/testsingletweet',twitter_map_admin_test.GetSingleTweet),
    ('/testposttweet',twitter_map_admin_test.PostSingleTweet),
    ('/testgetdatastore',twitter_map_admin_test.GetTweetFromDatastore),
    ('/testposthotkey',twitter_map_admin_test.PostTopHotKey),
    ('/testcleardb',twitter_map_admin_test.DeleteAllTweetEntries)
], debug=True)
