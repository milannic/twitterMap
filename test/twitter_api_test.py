import tweepy
import json
import sys
import uuid
from datetime import date

class StdOutListener(tweepy.StreamListener):
    """ A listener handles tweets are the received from the stream.
    This is a basic listener that just prints received tweets to stdout.

    """
    def on_data(self, data):
        #print data
        global accumu_len
        global max_len
        global filter_name
        global debug
        global prefix
        json_data = json.loads(data)
        #print data
#        if json_data.has_key('text'):
#            print json_data['text']
#        if json_data.has_key('created_at'):
#            print json_data['created_at']
#        if json_data.has_key('location'):
#            print json_data['location']
        if json_data.has_key('coordinates'):
            if json_data['coordinates']:
                accumu_len = accumu_len+len(data)
                if debug:
                    print "hahahahahah"
                    print data
                    print accumu_len
                    haha=raw_input("stop")
                with open("./output/twitter_raw_%s_%s"%(str(date.today()),prefix),'a') as output:
                    json.dump(json_data,output)
                    output.write('\n')
                if accumu_len > max_len:
                    sys.exit(0)
        return True

    def on_error(self, status):
        print status


if __name__=="__main__":
    prefix = str(uuid.uuid1())[1:3]
    accumu_len=0
    max_len=1000000000
    filter_name=""
    consumer_key="hN6Ylemc3CHG36qmv9EhsJbi8"
    consumer_secret="bZVvyKGt9lWzzuXjDmfYPtuSREtYYkk1PRbFnkels457qa7nWT"
    access_token="355666620-Lskp23vAsID3kjuJMZBcGSZdGvemASqRcqKb3NqU"
    access_token_secret="ZYBIZZw7BrPOy3fjjnWceHwVzHjkLqzvF2cB3j2cwTwww"

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)
    l = StdOutListener()
    if len(sys.argv) > 1:
        debug = sys.argv[1]
    else:
        debug = 0
    if debug:
        print api.me().name
        print api.me().id

    filter_name = ""

    with open("filter_list","r") as filter_list_in:
        for each_line in filter_list_in:
            if filter_name:
                filter_name = filter_name +","+each_line.replace("\n","")
            else:
                filter_name = each_line.replace("\n","")


    stream = tweepy.Stream(auth,l)
    #print dir(stream)
    #stream.sample()
    if debug:
        print filter_name
        haha=raw_input("stop")
    stream.filter(track=[filter_name],languages=['en'])
    #stream.filter()


