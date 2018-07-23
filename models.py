from google.appengine.ext import ndb

class Tournaments(ndb.Model):
    name = ndb.StringProperty(required = True)
    background_image = ndb.StringProperty()
    bracket_style = ndb.StringProperty(required = True)
    loser_bracket = ndb.BooleanProperty()
    public = ndb.BooleanProperty(required = True)

class Profiles(ndb.Model):
    name = ndb.StringProperty(required = True)
    wins = ndb.IntegerProperty()
    loses = ndb.IntegerProperty()
    tournaments_created = ndb.PickelProperty()
    tournaments_participated = ndb.PickelProperty()
