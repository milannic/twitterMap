#! /usr/bin/env python

import json
import urllib
import urllib2
count = 11
headers = {}
headers['Content-Type'] = 'application/json'
url = 'http://127.0.0.1:8080/testposttweet'
with open('./output/twitter_raw','r') as input_json:
    for line in input_json:
        if count>11:
            json_dict = json.loads(line)
            post_data = json.dumps(json_dict).encode('utf-8')
            req = urllib2.Request(url,post_data,headers)
            try:
                response = urllib2.urlopen(req)
                the_page = response.read()
                print the_page
            except Exception,e:
                print e
        count = count +1
        if count > 20:
            break
