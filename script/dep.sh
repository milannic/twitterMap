#! /bin/sh
mkdir dep
cd dep
git clone https://github.com/tweepy/tweepy.git
cd tweepy
python setup.py install --user
cd ..
cd ..
