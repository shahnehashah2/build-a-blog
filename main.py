import webapp2
import cgi
import jinja2
import os
from google.appengine.ext import db
import logging

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)

def get_posts(offset, limit=5):
    limit1 = int(limit)
    offset = int(offset)
    blogs = db.GqlQuery("""select * from Blog order by submitted_time DESC limit %s""" %limit1)
    logging.info('Number of blogs = ************' +str(blogs.count()))
    return blogs


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
        page = self.request.get("page")
        if not page:
            page = 1
        else:
            page = int(page)
        offset = page*5 - 5
        #blogs = get_posts(offset,5)
        blogs = db.GqlQuery("select * from Blog order by submitted_time DESC limit 5")
        self.render("base.html", blogs=blogs)
        self.render("pagination.html", page=page, count=blogs.count())

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
        if not Blog.get_by_id(id1):
            self.render('base.html')
            self.write("No blog found under that id")
        else:
            b = db.GqlQuery("select * from Blog where id = :id", id=id1)
            logging.info("This should be printed*********" + str(b))
            self.render("base.html", blogs=b)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/blog', MainHandler),
    ('/newpost', NewPostHandler),
    webapp2.Route('/blog/<id:\d+>', ViewPostHandler)
], debug=True)
