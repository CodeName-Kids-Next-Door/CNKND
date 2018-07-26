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

# def rounder(list,):

class MainPage(webapp2.RequestHandler):
    def get(self):
        logout_link = users.create_logout_url('/')
        logout_dict = {'logout': logout_link, 'loader': "Logout"}
        user = users.get_current_user()
        if user:
            email_address = user.nickname()
            cssi_user = Users.get_by_id(user.user_id())
            signout_link_html = '<a href="%s">Sign Out</a>' % users.create_logout_url('/')
            if cssi_user:
                main_template = \
                     jinja_current_directory.get_template('templates/main.html')
                self.response.write(main_template.render(logout_dict))
        else:
            logout_dict['loader'] = "Login"
            logout_dict['logout'] = "/login"
            main_template = \
                 jinja_current_directory.get_template('templates/main.html')
            self.response.write(main_template.render(logout_dict))
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
        logout_link = users.create_logout_url('/')
        logout_dict = {'logout': '/login', 'loader': "Login"}
        main_template = \
                 jinja_current_directory.get_template('templates/login.html')
        user = users.get_current_user()
        if user:
            email_address = user.nickname()
            cssi_user = Users.get_by_id(user.user_id())
            signout_link_html = '<a href="%s">Sign Out</a>' % users.create_logout_url('/')
            if cssi_user:
                logout_dict['loader'] = "Logout"
                logout_dict['logout'] = logout_link
                self.response.write(main_template.render(logout_dict))
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
            self.response.write(main_template.render(logout_dict))
            # self.response.write('''
            #     Please log in to use our site! <br>
            #     <a href="%s">Sign in</a>''' % (users.create_login_url('/login')))
    def post(self):
        user = users.get_current_user()
        if not user:
            self.error(500)
            return
        cssi_user = Users(
            first_name = self.request.get('first_name'),
            last_name = self.request.get('last_name'),
            profiles = self.request.get('profile_name'),
            is_login = True,
            id= user.user_id())
        cssi_user.put()
        new_profile = Profiles(name = cssi_user.profiles, first_name = cssi_user.first_name)
        new_profile.put()
        self.response.write('Thanks for signing up, %s'% cssi_user.first_name)
        self.response.write('''<br><a href="profile">Your Profile<a>''')
class ProfilePage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        logout_link = users.create_logout_url('/')
        logout_dict = {'logout': logout_link}
        if user:
            email_address = user.nickname()
            cssi_user = Users.get_by_id(user.user_id())
            signout_link_html = '<a href="%s">Sign Out</a>' % users.create_logout_url('/')
            if cssi_user:
                profile_template = \
                        jinja_current_directory.get_template('templates/profile.html')
                self.response.write(profile_template.render(logout_dict))
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
        logout_link = users.create_logout_url('/')
        logout_dict = {'logout': logout_link}
        if user:
            email_address = user.nickname()
            cssi_user = Users.get_by_id(user.user_id())
            signout_link_html = '<a href="%s">Sign Out</a>' % users.create_logout_url('/')
            if cssi_user:
                tournament_Creator_template = \
                   jinja_current_directory.get_template('templates/tournament_Creator.html')
                self.response.write(tournament_Creator_template.render(logout_dict))
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
            timer = self.request.get('timer1')
        background_image = self.request.get('background_image')
        player1 = self.request.get('player1')
        player2 = self.request.get('player2')
        player3 = self.request.get('player3')
        player4 = self.request.get('player4')
        player5 = self.request.get('player5')
        player6 = self.request.get('player6')
        player7 = self.request.get('player7')
        player8 = self.request.get('player8')
        player9 = self.request.get('player9')
        player10 = self.request.get('player10')
        player11 = self.request.get('player11')
        player12 = self.request.get('player12')
        player13 = self.request.get('player13')
        player14 = self.request.get('player14')
        player15 = self.request.get('player15')
        player16 = self.request.get('player16')
        round0 =[player1,player2,player3,player4,player5,player6,player7,player8,player9,player10,player11,player12,player13,player14,player15,player16]
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
            creator = cssi_user.first_name,
            round0 = round0,
            )
        viewer = new_tournament.put()
        view_id = viewer.urlsafe()
        players = Profiles().query().fetch()
        self.redirect('/tournamentViewer?id=' + view_id)

class TournmanetParticipatePage(webapp2.RequestHandler):
    def get(self):
        tournament_Participate_template = \
            jinja_current_directory.get_template('templates/tournament_Participate.html')
        self.response.write(tournament_Participate_template.render())

class TournmanetViewerPage(webapp2.RequestHandler):
    def get(self):
        tourn_id = self.request.get('id')
        key = ndb.Key(urlsafe = tourn_id)
        tourn_query = key.get()
        pairs0 = []
        for i in range(0, len(tourn_query.round0) / 2):
            pairs0.append([str(tourn_query.round0[i]), str(tourn_query.round0[len(tourn_query.round0) - i - 1])])
        pairs1 = []
        for i in range(0, len(tourn_query.round1) / 2):
            pairs1.append([str(tourn_query.round1[i]), str(tourn_query.round1[len(tourn_query.round1) - i - 1])])
        pairs2 = []
        for i in range(0, len(tourn_query.round2) / 2):
            pairs2.append([str(tourn_query.round2[i]), str(tourn_query.round2[len(tourn_query.round2) - i - 1])])
        pairs3 = []
        for i in range(0, len(tourn_query.round3) / 2):
            pairs2.append([str(tourn_query.round3[i]), str(tourn_query.round3[len(tourn_query.round3) - i - 1])])
        tourn_dict = {'all': tourn_query,
            'pairs0': pairs0,
            'pairs1': pairs1,
            'pairs2': pairs2,
            'pairs3': pairs3,
            'champions': tourn_query.champions,
            'title': tourn_query.name,
            'font': tourn_query.background_font,
            'color': tourn_query.background_color,
            'back': tourn_query.background_image,}
        tournament_Viewer_template = \
            jinja_current_directory.get_template('templates/tournament_Viewer.html')
        self.response.write(tournament_Viewer_template.render(tourn_dict))
    def post(self):
        winner = self.request.get('winner')
        tourn_id = self.request.get('id')
        key = ndb.Key(urlsafe = tourn_id)
        tourn = key.get()
        pairs0 = []
        for i in range(0, len(tourn.round0) / 2):
            pairs0.append([str(tourn.round0[i]), str(tourn.round0[len(tourn.round0) - i - 1])])
        pairs1 = []
        for i in range(0, len(tourn.round1) / 2):
            pairs1.append([str(tourn.round1[i]), str(tourn.round1[len(tourn.round1) - i - 1])])
        pairs2 = []
        for i in range(0, len(tourn.round2) / 2):
            pairs2.append([str(tourn.round2[i]), str(tourn.round2[len(tourn.round2) - i - 1])])
        pairs3 = []
        for i in range(0, len(tourn.round3) / 2):
            pairs2.append([str(tourn.round3[i]), str(tourn.round3[len(tourn.round3) - i - 1])])
        pairs3 = tourn.round3
        next_round1 = tourn.round1
        next_round2 = tourn.round2
        next_round3 = tourn.round3
        next_round4 = tourn.champions
        viewer = tourn.put()
        view_id = viewer.urlsafe()
        if len(next_round1) < 8:
            if winner == "player10":
                next_round1.append(pairs0[0][0])
                pass
            elif winner == "player20":
                next_round1.append(pairs0[0][1])
                pass
            elif winner == "player11":
                next_round1.append(pairs0[1][0])
                pass
            elif winner == "player21":
                next_round1.append(pairs0[1][1])
                pass
            elif winner == "player12":
                next_round1.append(pairs0[2][0])
                pass
            elif winner == "player22":
                next_round1.append(pairs0[2][1])
                pass
            elif winner == "player13":
                next_round1.append(pairs0[3][0])
                pass
            elif winner == "player23":
                next_round1.append(pairs0[3][1])
                pass
            elif winner == "player14":
                next_round1.append(pairs0[4][0])
                pass
            elif winner == "player24":
                next_round1.append(pairs0[4][1])
                pass
            elif winner == "player15":
                next_round1.append(pairs0[5][0])
                pass
            elif winner == "player25":
                next_round1.append(pairs0[5][1])
                pass
            elif winner == "player16":
                next_round1.append(pairs0[6][0])
                pass
            elif winner == "player26":
                next_round1.append(pairs0[6][1])
                pass
            elif winner == "player17":
                next_round1.append(pairs0[7][0])
                pass
            elif winner == "player27":
                next_round1.append(pairs0[7][1])
                pass
            tourn.round1 = next_round1
            print next_round1
            tourn.put()
            self.redirect('/tournamentViewer?id=' + view_id)
        elif len(next_round2) < 4:
            if winner == "player110":
                next_round2.append(pairs1[0][0])
                pass
            elif winner == "player120":
                next_round2.append(pairs1[0][1])
                pass
            elif winner == "player111":
                next_round2.append(pairs1[1][0])
                pass
            elif winner == "player121":
                next_round2.append(pairs1[1][1])
                pass
            if winner == "player112":
                next_round2.append(pairs1[2][0])
                pass
            elif winner == "player122":
                next_round2.append(pairs1[2][1])
                pass
            elif winner == "player113":
                next_round2.append(pairs1[3][0])
                pass
            elif winner == "player123":
                next_round2.append(pairs1[3][1])
                pass
            tourn.round2 = next_round2
            tourn.put()
            print tourn.round2
            self.redirect('/tournamentViewer?id=' + view_id)
        elif len(next_round3) < 2:
            if winner == "player210":
                next_round3.append(pairs2[0][0])
                pass
            elif winner == "player220":
                next_round3.append(pairs2[0][1])
                pass
            if winner == "player211":
                next_round3.append(pairs2[1][0])
                pass
            elif winner == "player221":
                next_round3.append(pairs2[1][1])
                pass
            tourn.round3 = next_round3
            tourn.put()
            print len(tourn.round3)
            self.redirect('/tournamentViewer?id=' + view_id)
        elif len(next_round4) < 1:
            if winner == "player310":
                next_round4.append(str(pairs3[0]))
                pass
            elif winner == "player320":
                next_round4.append(str(pairs3[1]))
                pass
            tourn.champions = next_round4
            tourn.put()
            print tourn.champions
            self.redirect('/tournamentViewer?id=' + view_id)
        pass


app = webapp2.WSGIApplication([('/', MainPage),
    ('/login', LoginPage),
    ('/profile', ProfilePage),
    ('/tournamentCreator', TournamentCreatorPage),
    ('/tournamentParticipate', TournmanetParticipatePage),
    ('/tournamentViewer', TournmanetViewerPage)
], debug=False)
