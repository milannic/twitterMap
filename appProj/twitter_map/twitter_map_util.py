"""
This py file contains some utils used by the application
such as how to parse a tweet

"""
import tweepy
import re
import twitter_map_config
from  google.appengine.api import memcache
from google.appengine.ext import ndb
import random
import twitter_map_db_model
from datetime import datetime

stop_word_list = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself',
                  'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself',
                  'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that',
                  'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
                  'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as',
                  'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through',
                  'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off',
                  'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how',
                  'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not',
                  'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should',
                  'now', 'www', 'https', 'http', 'com', 'net', 'org', 'done', 'rt', 'could']


def creatGeoWithinUSA():
    logi = random.uniform(-120,-70)
    lati = random.uniform(30,50)
    return [logi,lati]


def getHotKeyDict():
    '''
    this function query the memcache to see whether current hot key list is in the memcache otherwise it just query the
    data store, -1 means currently we won't have hot key info, it will only be in the debug stage.
    and whenever you want to get information about the hot key dict you should use this function
    '''
    hot_key_dict = memcache.get(twitter_map_config.top_7_hotkey_memcache_key)
    if hot_key_dict is not None:
        return hot_key_dict
    else:
        hot_key_dict = {}
        try:
            q = twitter_map_db_model.HotKeyList.query().order(twitter_map_db_model.HotKeyList.hid)
            for p in q:
                hot_key_dict[p.text] = p.hid
            if not hot_key_dict:
                return -1
        except Exception, e:
            return -1
        else:
            memcache.add(twitter_map_config.top_7_hotkey_memcache_key, hot_key_dict)
            return hot_key_dict


def parseTweet(tweet_text):
    '''
    when received a new tweet, you should use this function to determine how much hot keys it contains now
    '''
    #hot_key_list = [0, 0, 0, 0, 0, 0, 0]
    #hot_key_dict = getHotKeyDict()
    #print hot_key_dict
    key_list = []
    parse_text = tweet_text.encode('ascii', 'ignore')
    filter_text = parse_text.lower()
    filter_text = filter_text.replace('\n', ' ')
    filter_text = filter_text.replace('#', ' ')
    filter_text = filter_text.replace('-', '_')
    #filter http link
    filter_text = re.sub(r'http[s]?://(.*?) ', ' ', filter_text)
    #filter tail http link
    filter_text = re.sub(r'http[s]?://(.*?)$', ' ', filter_text)
    filter_text = re.sub(r'&(.*?)\s', ' ', filter_text)
    filter_text = re.sub(r'i\'m', ' ', filter_text)
    filter_text = re.sub(r'@(.*?)\s', ' ', filter_text)
    filter_text = re.sub(r'[^\w]', ' ', filter_text)
    if filter_text.strip():
        filter_text_list = filter_text.split(" ")
        filter_text_list = list(set(filter_text_list))
        for ele in filter_text_list:
            if ele:
                if len(ele) != 1:
                    if ele not in stop_word_list:
                        #print type(ele)
                        key_list.append(ele)

    return key_list


def putTweetToDataStore(tweet):
    try:
        tweet_ins = twitter_map_db_model.Tweet()
        #so longitude is at first
        #        tweet_data['coordinates']['coordinates'][0]
        #        #so latitude is the second
        #        tweet_data['coordinates']['coordinates'][1]
        print tweet.text
        tweet_ins.text = tweet.text
        hot_key_list = parseTweet(tweet.text)
        tweet_ins.hk = hot_key_list
        if tweet.coordinates is not None:
            tweet_ins.location = ndb.GeoPt(float(tweet.coordinates.coordinates[1]),
                                           float(tweet.coordinates.coordinates[0]))
        else:
            pseudo_location = creatGeoWithinUSA()
            tweet_ins.location = ndb.GeoPt(pseudo_location[1], pseudo_location[0])
        print tweet_ins.location
        tweet_ins.tid = tweet.id
        tweet_ins.uid = tweet.user.id
        tweet_ins.uname = tweet.user.screen_name
        tweet_ins.date = tweet.created_at
        print tweet_ins.put()
        return 0
    except Exception, e:
        print e
        return -1

def getAndSaveTweet(count, page):
    '''
    this function is used
    '''
    try:
        for single_page in tweepy.Cursor(twitter_map_config.twitter_api.search,
                                   q='i',
                                   count=100,
                                   result_type="recent",
                                   include_entities=True,
                                   lang="en").pages(page):
            for tweet in single_page:
                res = putTweetToDataStore(tweet)
    except Exception,e:
        print e
        print "have reached the rate limit"
        return -1
    return "succeed"


def reConstructHotKeyInfo():
    pass

