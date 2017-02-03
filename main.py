'''
This program creates and displays blogs. It adds new blogs and displays them in
time created fashion. It takes care of pagination and navigation links for
ease of use. It does not allow modification of the blogs.
'''

import webapp2
import cgi
import jinja2
import os
from google.appengine.ext import db
from math import ceil

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)

class Handler(webapp2.RequestHandler):

    # The following will be equivalent to:
    # t = jinja_env.get_template("base.html")
    # content = t.render(parameters that need to be passed for base.html)
    # self.response.write(content)

    def write(self, *args, **kwargs):
        self.response.out.write(*args, **kwargs)

    def render_str(self,template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kwargs):
        self.write(self.render_str(template, **kwargs))

class MainHandler(Handler):
    def get(self):
        page = self.request.get("page")
        if not page:
            page = 1
        else:
            page = int(page)
        offset = page*5 - 5
        limit = 5
        blogs = db.GqlQuery("select * from Blog order by submitted_time DESC")
        self.render("viewallblogs.html",
                    blogs=blogs.run(limit=limit, offset=offset),
                    page=page, count=blogs.count()/5)

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
            self.redirect('/blog/{}'.format(str(b.key().id())))

class Blog(db.Model):
    subject = db.StringProperty(required = True)
    body = db.TextProperty(required = True)
    submitted_time = db.DateTimeProperty(auto_now_add = True)

class ViewPostHandler(Handler):
    def get(self, id):
        id1 = long(id)
        b = Blog.get_by_id(id1)
        if not b:
            self.render('base.html')
            self.write("No blog found under that id")
        else:
            self.render("viewblog.html", blog1=b)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/blog', MainHandler),
    ('/newpost', NewPostHandler),
    webapp2.Route('/blog/<id:\d+>', ViewPostHandler)
], debug=True)
