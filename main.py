import webapp2
import cgi
import jinja2
import os
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *args, **kwargs):
        self.response.out.write(*args, **kwargs)

    def render_str(self,template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kwargs):
        self.write(self.render_str(template, **kwargs))

class MainHandler(Handler):
    def get(self):
        # Query recent-most 5 entries to be displayed
        blogs = db.GqlQuery("select * from Blog order by submitted_time DESC limit 5")
        self.render("base.html", blogs=blogs)

class NewPostHandler(Handler):
    def makeForm(self, error='', subject='', body=''):
        self.render("base.html")
        self.render("blogform.html",error=error, subject=subject, body=body)

    def get(self):
        self.makeForm()

    def post(self):
        subject = self.request.get('subject')
        body = self.request.get('body')
        error = ''
        if not subject or not body:
            error = 'Need both Subject and Body'
            self.makeForm(error, subject, body)
        else:
            b = Blog(subject = subject, body = body)
            b.put()
            self.redirect('/')

class ViewPostHandler(webapp2.RequestHandler):
    def get(self, id):
        #Display the subject and body for this id
        pass

class Blog(db.Model):
    subject = db.StringProperty(required = True)
    body = db.TextProperty(required = True)
    submitted_time = db.DateTimeProperty(auto_now_add = True)



app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/newpost', NewPostHandler),
    webapp2.Route('/blog/<id:\d+>', ViewPostHandler)
], debug=True)
