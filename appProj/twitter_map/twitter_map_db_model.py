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
    hk = ndb.StringProperty(repeated=True)



class HotKeyList(ndb.Model):
    """
    7 integers corresponding hot key text
    """
    hid = ndb.IntegerProperty()
    text = ndb.StringProperty()
    count = ndb.IntegerProperty()