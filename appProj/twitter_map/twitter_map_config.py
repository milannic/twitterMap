import tweepy

consumer_key="hN6Ylemc3CHG36qmv9EhsJbi8"
consumer_secret="bZVvyKGt9lWzzuXjDmfYPtuSREtYYkk1PRbFnkels457qa7nWT"
access_token="355666620-Lskp23vAsID3kjuJMZBcGSZdGvemASqRcqKb3NqU"
access_token_secret="ZYBIZZw7BrPOy3fjjnWceHwVzHjkLqzvF2cB3j2cwTwww"
twitter_auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
twitter_auth.set_access_token(access_token,access_token_secret)
twitter_api = tweepy.API(twitter_auth)
top_hot_key_memcache_key="top_hot_keys"
re_construct_threshold = 10000
key_word_length = 10
batch_recon = 10