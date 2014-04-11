#! /usr/bin/env python

import json
import urllib
import urllib2
import sys
import re
import argparse


stop_word_list = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now','www','https','http','com','net','org','done','rt','could']

count = 0
headers = {}
headers['Content-Type'] = 'application/json'
global_dict = {}

parser = argparse.ArgumentParser(description="twitter map parser")
parser.add_argument("-d","--debug",dest="debug",help="enable debug option",type=int,default=0)
parser.add_argument("-t","--threshold",dest="threshold",help="filter the top threshold keyword",type=int,default=20)
parser.add_argument("-o","--output",dest="output",help="whether send the result to the output",type=int,default=1)

options = parser.parse_args()

debug = options.debug
threshold = options.threshold
output = options.output




try:
    if len(sys.argv) > 1:
        threshold = int(sys.argv[1])
except Exception,e:
    print e

with open('./output/twitter_raw','r') as input_json:
    for line in input_json:
        json_dict = json.loads(line)
        post_data = json.dumps(json_dict).encode('utf-8')
        re_json = json.loads(post_data)
        parse_text = re_json['text'].encode('ascii','ignore')
        filter_text = parse_text.lower()
        filter_text = filter_text.replace('\n',' ')
        filter_text = filter_text.replace('#',' ')
        filter_text = filter_text.replace('-','_')
        #filter http link 
        filter_text = re.sub(r'http[s]?://(.*?) ',' ',filter_text)
        #filter tail http link
        filter_text = re.sub(r'http[s]?://(.*?)$',' ',filter_text)
        filter_text = re.sub(r'&(.*?)\s',' ',filter_text)
        filter_text = re.sub(r'i\'m',' ',filter_text)
        filter_text = re.sub(r'@(.*?)\s',' ',filter_text)
        filter_text = re.sub(r'[^\w]',' ',filter_text)
        if debug:
            if re.match(r'.*\bco\b.*',filter_text):
                print parse_text
                print filter_text
                raw_input("haha")
        if filter_text.strip():
            filter_text_list = filter_text.split(" ")
            filter_text_list = list(set(filter_text_list))
            count = count+1
            for ele in filter_text_list:
                if ele:
                    if len(ele) != 1:
                        if ele not in stop_word_list:
                            if global_dict.has_key(ele):
                                global_dict[ele] = global_dict[ele]+1
                            else:
                                global_dict[ele] = 1

sorted_dict = sorted(global_dict.items(),key=lambda x:x[1])

if threshold > len(sorted_dict):
    print sorted_dict
    real_threshold = sorted_dict[0][1]
else:
    print sorted_dict[len(sorted_dict)-threshold:len(sorted_dict)]
    real_threshold = sorted_dict[len(sorted_dict)-threshold][1]


for key in global_dict.keys():
    if global_dict[key] < real_threshold:
        global_dict.pop(key,None)

if output:
    with open('./output/twitter_dict_count_%d'%(threshold),'w') as output_json:
        json.dump(global_dict,output_json,indent=4)

