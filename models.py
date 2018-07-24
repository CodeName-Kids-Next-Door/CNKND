from google.appengine.ext import ndb

class Tournaments(ndb.Model):
    name = ndb.StringProperty(required = True)
    background_image = ndb.StringProperty()
    background_color = ndb.StringProperty()
    background_font = ndb.StringProperty()
    loser_bracket = ndb.BooleanProperty()
    public = ndb.BooleanProperty(required = True)
    players = ndb.StringProperty(repeated = True)
    champions = ndb.StringProperty()

class Profiles(ndb.Model):
    name = ndb.StringProperty(required = True)
    first_name = ndb.StringProperty(required =True)
    wins = ndb.IntegerProperty()
    loses = ndb.IntegerProperty()
    tournaments_created = ndb.StringProperty(repeated = True)
    tournaments_participated = ndb.StringProperty(repeated = True)
    championships = ndb.IntegerProperty()

class Users(ndb.Model):
    first_name = ndb.StringProperty(required = True)
    last_name = ndb.StringProperty(required = True)
    profiles = ndb.StringProperty()

class Probabilities(ndb.Model):
    profile = ndb.StringProperty(required = True)
    strength = ndb.IntegerProperty(required = True)
    rank = ndb.IntegerProperty(required = True)
