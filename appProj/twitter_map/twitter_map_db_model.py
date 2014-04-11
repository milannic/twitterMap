from google.appengine.ext import ndb


class Tweet(ndb.Model):

    """
    Data Model of Tweet
    Tweet ID, UserID, UserName, Coordinates.Longitude, Coordinates.Latitue, Created Date and Tweet.text
    And we add 7 hot keys
    """
    tid = ndb.IntegerProperty()
    uid = ndb.IntegerProperty()
    uname = ndb.StringProperty()
    location = ndb.GeoPtProperty()
    date = ndb.DateTimeProperty()
    text = ndb.StringProperty()
    hk0 = ndb.IntegerProperty()
    hk1 = ndb.IntegerProperty()
    hk2 = ndb.IntegerProperty()
    hk3 = ndb.IntegerProperty()
    hk4 = ndb.IntegerProperty()
    hk5 = ndb.IntegerProperty()
    hk6 = ndb.IntegerProperty()

class HotKeywordsCount(ndb.Model):
    """
    We store a hashmap in the datastore
    """
    count = ndb.IntegerProperty()
    text = ndb.StringProperty()


class HotKeyList(ndb.Model):
    """
    7 integers corresponding hot key text
    """
    hid = ndb.IntegerProperty()
    text = ndb.StringProperty()
    count = ndb.IntegerProperty()