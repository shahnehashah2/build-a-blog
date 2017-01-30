import webapp2

page_header = """<!DOCTYPE html>
<html>
<head>
    <title>Blog</title>
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
        content = page_header + page_footer
        self.response.write(content)

class NewPostHandler(webapp2.RequestHandler):
    def get(self):
        form = """
        <form action="/" method="post">
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
        """
        self.response.write(page_header+form+page_footer)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/newpost', NewPostHandler)
], debug=True)
