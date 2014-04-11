#! /usr/bin/env python

import json
import urllib
import urllib2
import sys

count = 0
headers = {}
headers['Content-Type'] = 'application/json'
if len(sys.argv) > 1:
    if sys.argv[1] == '1':
        url = 'http://cloudtwittermap.appspot.com/testposttweet'
else:
    url = 'http://127.0.0.1:8080/testposttweet'

with open('./output/twitter_raw','r') as input_json:
    for line in input_json:
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
        if count > 100:
            break
