import webapp2
import jinja2
import os

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
    def post(self):
        login_template = \
                jinja_current_directory.get_template('templates/login.html')

class CreateANewAccountPage(webapp2.RequestHandler):
    def get(self):
        NewAccount_template = \
                jinja_current_directory.get_template('templates/newaccount.html')
        self.response.write(welcome_template.render)

class ProfilePage(webapp2.RequestHandler):
    def get(self):
        # Profile_template = \




app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/login', LoginPage),
    ('/newaccount', CreateANewAccountPage)
], debug=True)
