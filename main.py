import os
import string
import sys

import jinja2
import webapp2

reload(sys)
sys.setdefaultencoding('utf8')

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class MainPage(Handler):
    def get(self):
        message = self.request.get('message', '')
        coded_message = cipher(message.encode('utf-8'))
        self.render("mytemplate.html", message=coded_message)

def cipher(message):
    encoder = string.maketrans(
    "ABCDEFGHIJKLMabcdefghijklmNOPQRSTUVWXYZnopqrstuvwxyz",
    "NOPQRSTUVWXYZnopqrstuvwxyzABCDEFGHIJKLMabcdefghijklm")
    output = None
    for char in message:
        if (not output) and char.isalpha():
            output = string.translate(char, encoder)
        elif char.isalpha():
            output += string.translate(char, encoder)
        elif output:
            output += char
        else:
            output = char
    return output


app = webapp2.WSGIApplication([
    ('/', MainPage),
], debug=True)
