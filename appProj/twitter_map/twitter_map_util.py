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
import json
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
    try:
        hot_key_dict = memcache.get(twitter_map_config.top_hot_key_memcache_key)
        if hot_key_dict is not None:
            return hot_key_dict
        else:
            hot_key_dict = {}
            try:
                q = twitter_map_db_model.HotKeyList.query().order(twitter_map_db_model.HotKeyList.hid)
                for p in q:
                    hot_key_dict[p.text] = p.count
                if not hot_key_dict:
                    return -1
            except Exception, e:
                return -1
            else:
                memcache.add(twitter_map_config.top_hot_key_memcache_key, hot_key_dict)
                return hot_key_dict
    except Exception,e:
        print e
        return -1

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
        #print tweet.text
        tweet_ins.text = tweet.text
        hot_key_list = parseTweet(tweet.text)
        tweet_ins.hk = hot_key_list
        if tweet.coordinates is not None:
            try:
                tweet_ins.location = ndb.GeoPt(float(tweet.coordinates.coordinates[1]),
                                            float(tweet.coordinates.coordinates[0]))
            except Exception,e:
                pseudo_location = creatGeoWithinUSA()
                tweet_ins.location = ndb.GeoPt(pseudo_location[1], pseudo_location[0])
        else:
            pseudo_location = creatGeoWithinUSA()
            tweet_ins.location = ndb.GeoPt(pseudo_location[1], pseudo_location[0])
        #print tweet_ins.location
        tweet_ins.tid = tweet.id
        tweet_ins.uid = tweet.user.id
        tweet_ins.uname = tweet.user.screen_name
        tweet_ins.date = tweet.created_at

        #due to the limitation of the google App Engine,every time you call the database related function you need to
        #catch the error in case you have reached the limit
        tweet_ins.put()
    except Exception, e:
        print e
        return -1

def getAndSaveTweet(count, page):
    '''
    this function is used to get twitter by cron job.
    '''
    try:
        for single_page in tweepy.Cursor(twitter_map_config.twitter_api.search,
                                   q='i',
                                   count=count,
                                   result_type="recent",
                                   include_entities=True,
                                   lang="en").pages(page):
            for tweet in single_page:
                res = putTweetToDataStore(tweet)
                if res ==-1:
                    raise ValueError(res)
    except Exception,e:
        print e
        print "have reached the rate limit"
        return -1
    return "succeed"


def reConstructHotKeyInfo():
    '''
    This function takes out all the keyword list of the tweets to calculate the new key word list
    '''
    global_dict = {}
    sorted_dict = []
    try:
        #at first we flush the memcache
        hot_key_dict = memcache.get(twitter_map_config.top_hot_key_memcache_key)
        if hot_key_dict is not None:
            memcache.delete(twitter_map_config.top_hot_key_memcache_key)
    except Exception,e:
        print "operation memcache error"
        print e
        return -1;

    #then we clear the keyword list
    try:
        ndb.delete_multi(twitter_map_db_model.HotKeyList.query().fetch(keys_only=True))
    except Exception,e:
        print "database deletion error"
        print e
        return -1

    # Now we take out every ele in the datastore and construct the keyword
    try:
        q = ndb.gql("SELECT hk FROM Tweet")
        global_dict = {}
        for p in q:
            if global_dict.has_key(p.hk[0]):
                global_dict[p.hk[0]] = global_dict[p.hk[0]]+1
            else:
                global_dict[p.hk[0]] = 1
        #print global_dict
        sorted_dict = sorted(global_dict.items(),key=lambda x:x[1])
        real_len = len(sorted_dict) and twitter_map_config.key_word_length>len(sorted_dict) or twitter_map_config.key_word_length
        sorted_dict = sorted_dict[len(sorted_dict)-real_len:len(sorted_dict)]
        #sorted_dict
    except Exception,e:
        print "database read error"
        print e
        return -1
    if construHotKeyList(sorted_dict) != -1:
        pass
    else:
        print "construct new key list error"
        return -1
    print "succeed"
    return 0

def construHotKeyList(list):
    try:
        hot_key_data = list
        count = 0
        for ele in hot_key_data:
            hot_key_ins = twitter_map_db_model.HotKeyList()
            hot_key_ins.hid = count
            hot_key_ins.text = ele[0]
            hot_key_ins.count = ele[1]
            hot_key_ins.put()
            count = count+1
    except Exception,e:
        print "database operation error"
        return -1
    return 0

def getTweetByKeyword(keyword):
    try:
        tweets = memcache.get('keyword:%s' % keyword)
        if tweets is not None:
            return tweets
        else:
            if keyword == "":
                result = twitter_map_db_model.Tweet.query()
            else:
                result = twitter_map_db_model.Tweet.query(twitter_map_db_model.Tweet.hk == keyword)
            tweets = []
            for t in result:
                tweet = {"tid":str(t.tid), "location":{"lat":t.location.lat, "lon":t.location.lon,}, "date":t.date.strftime("%m/%d/%Y %H:%M:%S")}
                tweets.append(tweet)
            if keyword != "":
                memcache.add('keyword:%s' % keyword, tweets)
            return tweets
    except Exception, e:
        print e

def filterTweetByDate(tweets, startDate, endDate):
    if not startDate and not endDate:
        return tweets
    result = []
    for t in tweets:
        date = datetime.strptime(t['date'],"%m/%d/%Y %H:%M:%S")
        if (not startDate or date >= startDate) and (not endDate or date <= endDate):
            result.append(t)
    return result

def getTweetByID(tid):
    try:
        result = twitter_map_db_model.Tweet.query(twitter_map_db_model.Tweet.tid == tid)
        for t in result:
            tweet = {"uid":t.uid, "uname":t.uname, "tid":str(t.tid), "location":{"lat":t.location.lat, "lon":t.location.lon,}, "date":t.date.strftime("%m/%d/%Y %H:%M:%S"), "text":t.text,
                         "hk":t.hk}
        return tweet

    except Exception, e:
        print e