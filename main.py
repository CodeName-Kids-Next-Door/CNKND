import webapp2
import jinja2
import os
from models import Tournaments
from models import Profiles
from models import Probabilities

jinja_current_directory = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions = ['jinja2.ext.autoescape'],
    autoescape = True)

class MainPage(webapp2.RequestHandler):
    def get(self):
        main_template = \
             jinja_current_directory.get_template('templates/main.html')
        self.response.write(main_template.render())

class LoginPage(webapp2.RequestHandler):
    def get(self):
        login_template = \
              jinja_current_directory.get_template('templates/login.html')
        self.response.write(login_template.render())
    def post(self):
        x = 1

class ProfilePage(webapp2.RequestHandler):
    def get(self):
        profile_template = \
                jinja_current_directory.get_template('templates/profile.html')
        self.response.write(profile_template.render())
    def post(self):
        x=1

class TournamentCreatorPage(webapp2.RequestHandler):
    def get(self):
        tournament_Creator_template = \
                   jinja_current_directory.get_template('templates/tournament_Creator.html')
        self.response.write(tournament_Creator_template.render())
    def post(self):
        x =1

class TournmanetParticipatePage(webapp2.RequestHandler):
    def get(self):
        tournament_Participate_template = \
            jinja_current_directory.get_template('templates/tournament_Participate.html')
        self.response.write(tournament_Participate_template.render())

class TournmanetViewerPage(webapp2.RequestHandler):
    def get(self):
        tournament_Viewer_template = \
            jinja_current_directory.get_template('templates/tournament_Viewer.html')
        self.response.write(tournament_Viewer_template.render())



app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/login', LoginPage),
    ('/profile', ProfilePage),
    ('/tournamentCreator', TournamentCreatorPage),
    ('/tournamentParticipate', TournmanetParticipatePage),
    ('/tournamentViewer', TournmanetViewerPage)
], debug=True)
