#! /usr/bin/env python

import json
import urllib
import urllib2
import sys
import argparse

headers = {}
headers['Content-Type'] = 'application/json'

parser = argparse.ArgumentParser(description="twitter map post hot key script")
parser.add_argument("-d","--debug",dest="debug",help="enable debug option",type=int,default=1)

options = parser.parse_args()
debug = options.debug


if not debug:
    url = 'http://cloudtwittermap.appspot.com/testposthotkey'
else:
    url = 'http://127.0.0.1:8080/testposthotkey'

with open('./output/twitter_dict_count','r') as input_json:
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
