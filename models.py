from google.appengine.ext import ndb

class Tournaments(ndb.Model):
    name = ndb.StringProperty(required = True)
    background_image = ndb.StringProperty()
    background_color = ndb.StringProperty(required = True)
    background_font = ndb.StringProperty(required = True)
    loser_bracket = ndb.BooleanProperty(required = True)
    public = ndb.BooleanProperty(required = True)
    players = ndb.StringProperty(repeated = True)
    champions = ndb.StringProperty()
    creator = ndb.StringProperty(required = True)
    round0 = ndb.StringProperty(repeated =True)
    round1 = ndb.StringProperty(repeated = True)
    round2 = ndb.StringProperty(repeated = True)
    round3 = ndb.StringProperty(repeated = True)

class Profiles(ndb.Model):
    name = ndb.StringProperty(required = True)
    first_name = ndb.StringProperty(required =True)
    wins = ndb.IntegerProperty()
    loses = ndb.IntegerProperty()
    tournaments_participated = ndb.StringProperty(repeated = True)
    championships = ndb.IntegerProperty()

class Users(ndb.Model):
    first_name = ndb.StringProperty(required = True)
    last_name = ndb.StringProperty(required = True)
    profiles = ndb.StringProperty()
    is_login = ndb.BooleanProperty()

class Probabilities(ndb.Model):
    profile = ndb.StringProperty(required = True)
    strength = ndb.IntegerProperty(required = True)
    rank = ndb.IntegerProperty(required = True)

class MatchWinner(ndb.Model):
    winner = ndb.StringProperty(required = True)
