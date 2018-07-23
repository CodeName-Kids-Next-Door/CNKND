import webapp2
import jinja2
import os
from models import Tournaments
from models import Profiles
from models import Probabilities
from models import Users
from google.appengine.api import users

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
    # def get(self):
    #     login_template = \
    #           jinja_current_directory.get_template('templates/login.html')
    #     self.response.write(login_template.render())
    def get(self):
        user = users.get_current_user()
        if user:
            email_address = user.nickname()
            cssi_user = CssiUser.get_by_id(user.user_id())
            signout_link_html = '<a href="%s">Sign Out</a>' % users.create_logout_url('/')
            if cssi_user:
                self.response.write('''
                    <h2>Welcome %s %s (%s)!</h2> <br> <a href="profile">Profile</a> <br> %s <br>''' %
                    (cssi_user.first_name,
                    cssi_user.last_name,
                    email_address,
                    signout_link_html))
            else:
                self.response.write('''
                    <h2>Welcome to our site, %s! Please sign up!</h2> <br>
                    <form method="post">
                    <input name="first_name"/>
                    <input name="last_name"/>
                    <input type="submit"/>
                    </form><br> %s <br>''' % (email_address, signout_link_html))
        else:
            self.response.write('''
                Please log in to use our site! <br>
                <a href="%s">Sign in</a>''' % (users.create_login_url('/')))
    def post(self):
        user = users.get_current_user()
        if not user:
            self.error(500)
            return
        cssi_user = CssiUser(
            first_name = self.request.get('first_name'),
            last_name = self.request.get('last_name'),
            id= user.user_id())
        cssi_user.put()
        self.response.write('Thanks for signing up, %s'% cssi_user.first_name)
        self.response.write('''<br><a href="profile">Your Bank account<a>''')

class ProfilePage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            email_address = user.nickname()
            cssi_user = CssiUser.get_by_id(user.user_id())
            signout_link_html = '<a href="%s">Sign Out</a>' % users.create_logout_url('/')
            if cssi_user:
                self.response.write('''
                    Welcome %s %s (%s)! <br> %s <br>''' %
                    (cssi_user.first_name,
                    cssi_user.last_name,
                    email_address,
                    signout_link_html))
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
        name = self.request.get('name')
        background_image1 = self.request.get('background_image')
        background_image = self.request.get('background')
        bracket_style_font = self.request.get('style-font')
        bracket_style_color = self.request.get('style-color')
        loser_bracket = self.request.get('loser_bracket')
        public = self.request.get('public')


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
