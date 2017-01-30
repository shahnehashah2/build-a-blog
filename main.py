import webapp2
import cgi

page_header = """<!DOCTYPE html>
<html>
<head>
    <title>Blog</title>
    <style type="text/css">
        .error {
            color: red;
        }
    </style>
</head>
<body>
    <h1>
        <a href="/">BlogPage</a>
    </h1>
"""

# html boilerplate for the bottom of every page
page_footer = """
</body>
</html>
"""

class MainHandler(webapp2.RequestHandler):
    def get(self):
        # Query recent-most 5 entries to be displayed
        content = page_header + page_footer
        self.response.write(content)

class NewPostHandler(webapp2.RequestHandler):
    def get(self):
        error = self.request.get('error')
        error = ('<p class="error">' + cgi.escape(error) + '</p><br>'
                if error else '')
        form = """
        <form method="post">
            {}
            <label>
                <strong>Subject</strong>
            </label>
            <br>
            <input type="text" name="subject" style = "width:800px;">
            <br><br>
            <label>
                <strong>Body</strong>
            </label>
            <br>
            <input type="text" name="body" style = "height:400px; width:800px;">
            <br>
            <input type="submit">
        </form>
        """.format(error)
        self.response.write(page_header + form + page_footer)

    def post(self):
        subject = self.request.get('subject')
        body = self.request.get('body')
        if not subject or not body:
            error = 'Need both Subject and Body'
            self.redirect('/newpost?error=' + error)

        # Otherwise add in database and redirect to home page

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/newpost', NewPostHandler)
], debug=True)
