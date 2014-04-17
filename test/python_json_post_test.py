#! /usr/bin/env python

import json
import urllib
import urllib2
import sys
import argparse

parser = argparse.ArgumentParser(description="twitter map post script")
parser.add_argument("-d","--debug",dest="debug",help="enable debug option",type=int,default=1)
parser.add_argument("-s","--start",dest="start",help="start position",type=int,default=0)
parser.add_argument("-e","--end",dest="end",help="end position",type=int,default=20)



count = 0

headers = {}
headers['Content-Type'] = 'application/json'


options = parser.parse_args()

debug = options.debug
start = options.start
end = options.end

if start<0 or end <0 or start>end:
    print "invalid parameter"
    sys.exit(1)



if not debug:
    url = 'http://cloudtwittermap.appspot.com/testposttweet'
else:
    url = 'http://127.0.0.1:8080/testposttweet'


with open('./output/twitter_raw','r') as input_json:
        for line in input_json:
            if count>=start:
                json_dict = json.loads(line)
                post_data = json.dumps(json_dict).encode('utf-8')
                req = urllib2.Request(url,post_data,headers)
                try:
                    response = urllib2.urlopen(req)
                    the_page = response.read()
                    print the_page
                except Exception,e:
                    print e
            print count 
            count = count +1
            if count >= end:
                break
