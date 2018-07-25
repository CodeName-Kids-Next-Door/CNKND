import webapp2
import jinja2
import os
from models import Tournaments
from models import Profiles
from models import Probabilities
from models import Users
from google.appengine.api import users
from google.appengine.ext import ndb

jinja_current_directory = jinja2.Environment(
    loader = jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions = ['jinja2.ext.autoescape'],
    autoescape = True)

class ProList(object):
    def __init__(self, prolist, list_tournaments = []):
        self.prolist = prolist
        self.list_tournaments = list_tournaments
        pass
first_prolist = ProList(0)
class MainPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            email_address = user.nickname()
            cssi_user = Users.get_by_id(user.user_id())
            signout_link_html = '<a href="%s">Sign Out</a>' % users.create_logout_url('/')
        main_template = \
             jinja_current_directory.get_template('templates/main.html')
        self.response.write(main_template.render())
                # self.response.write('''
                #     <h2>Welcome %s %s (%s)!</h2> <br> <a href="profile">Profile</a> <br> %s <br>''' %
                #     (cssi_user.first_name,
                #     cssi_user.last_name,
                #     email_address,
                #     signout_link_html))

class LoginPage(webapp2.RequestHandler):
    # def get(self):
    #     login_template = \
    #           jinja_current_directory.get_template('templates/login.html')
    #     self.response.write(login_template.render())
    def get(self):
        user = users.get_current_user()
        main_template = \
                 jinja_current_directory.get_template('templates/login.html')
        self.response.write(main_template.render())
        if user:
            email_address = user.nickname()
            cssi_user = Users.get_by_id(user.user_id())
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
                    <input name="first_name" placeholder='First Name'/>
                    <br>
                    <input name="last_name" placeholder='Last Name'/>
                    <br>
                    <input name="profile_name" placeholder="User Name"/>
                    <input type="submit"/>
                    </form><br> %s <br>''' % (email_address, signout_link_html))
        else:
            self.response.write('''
                Please log in to use our site! <br>
                <a href="%s">Sign in</a>''' % (users.create_login_url('/login')))
    def post(self):
        user = users.get_current_user()
        if not user:
            self.error(500)
            return
        cssi_user = Users(
            first_name = self.request.get('first_name'),
            last_name = self.request.get('last_name'),
            profiles = self.request.get('profile_name'),
            id= user.user_id())
        cssi_user.put()
        new_profile = Profiles(name = cssi_user.profiles, first_name = cssi_user.first_name)
        new_profile.put()
        self.response.write('Thanks for signing up, %s'% cssi_user.first_name)
        self.response.write('''<br><a href="profile">Your Profile<a>''')
class ProfilePage(webapp2.RequestHandler):
    def get(self):
        profile_template = \
                jinja_current_directory.get_template('templates/profile.html')
        self.response.write(profile_template.render())
        user = users.get_current_user()
        if user:
            email_address = user.nickname()
            cssi_user = Users.get_by_id(user.user_id())
            signout_link_html = '<a href="%s">Sign Out</a>' % users.create_logout_url('/')
            if cssi_user:
                self.response.write('''
                    Welcome %s %s (%s)! <br> %s <br>''' %
                    (cssi_user.first_name,
                    cssi_user.last_name,
                    cssi_user.profiles,
                    signout_link_html))
    def post(self):
        x=1

class TournamentCreatorPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            email_address = user.nickname()
            cssi_user = Users.get_by_id(user.user_id())
            signout_link_html = '<a href="%s">Sign Out</a>' % users.create_logout_url('/')
            if cssi_user:
                tournament_Creator_template = \
                   jinja_current_directory.get_template('templates/tournament_Creator.html')
                self.response.write(tournament_Creator_template.render())
        else:
            self.response.write('''
                Please log in to use our site! <br>
                <a href="%s">Sign in</a>''' % (users.create_login_url('/login')))
            # tournament_Creator_template = \
            #    jinja_current_directory.get_template('templates/login.html')
            # self.response.write(tournament_Creator_template.render())
    def post(self):
        user = users.get_current_user()
        if user:
            email_address = user.nickname()
            cssi_user = Users.get_by_id(user.user_id())
            signout_link_html = '<a href="%s">Sign Out</a>' % users.create_logout_url('/')
        name = self.request.get('name')
        timer = 0
        if self.request.get("timer") == 'yes':
            timer = 999
        background_image = self.request.get('background_image')
        if background_image == '':
            background_image = self.request.get('background')
        bracket_style_font = self.request.get('style_font')
        bracket_style_color = self.request.get('style_color')
        if self.request.get('loser_bracket') == 'yes':
            loser_bracket = True
            print loser_bracket
        else:
            loser_bracket = False
        if self.request.get('public') == 'yes':
            public = True
        else:
            public = False
        new_tournament = Tournaments(name = name,
            background_image = background_image,
            background_color = bracket_style_color,
            background_font = bracket_style_font,
            loser_bracket = loser_bracket,
            public = public,
            creator = cssi_user.first_name)
        new_tournament.put()
        # new_profile_key = first_prolist.prolist
        # new_profile = new_profile_key.get()
        # url_string = new_profile_key.urlsafe()
        # new_profile_key = ndb.Key(urlsafe=url_string)
        # key = Key(urlsafe=url_string)
        # kind_string = key.kind()
        # ident = key.id()
        # profile = key.get()
        # p = Profiles.get_or_insert(key)
        tourn_query = Tournaments().query().fetch()
        profile_query = Profiles().query().fetch()
        tourn_dict = {'all': tourn_query,
            'player': profile_query,
            'title': new_tournament.name,
            'font': new_tournament.background_font,
            'color': new_tournament.background_color,
            'back': new_tournament.background_image}
        tournament_Viewer_template = jinja_current_directory.get_template('templates/tournament_Viewer.html')
        self.response.write(tournament_Viewer_template.render(tourn_dict))

class TournmanetParticipatePage(webapp2.RequestHandler):
    def get(self):
        tournament_Participate_template = \
            jinja_current_directory.get_template('templates/tournament_Participate.html')
        self.response.write(tournament_Participate_template.render())

class TournmanetViewerPage(webapp2.RequestHandler):
    def get(self):
        tourn_query = Tournaments().query().fetch()
        profile_query = Users().query().fetch()
        tourn_dict = {'all': tourn_query,
            'player': profile_query}
        tournament_Viewer_template = \
            jinja_current_directory.get_template('templates/tournament_Viewer.html')
        self.response.write(tournament_Viewer_template.render(tourn_dict))



app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/login', LoginPage),
    ('/profile', ProfilePage),
    ('/tournamentCreator', TournamentCreatorPage),
    ('/tournamentParticipate', TournmanetParticipatePage),
    ('/tournamentViewer', TournmanetViewerPage)
], debug=True)
