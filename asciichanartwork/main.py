#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import webapp2
import jinja2

from google.appengine.ext import db

# Location of HTML templates
TEMPLATE_LOCATION = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                 "templates")

# Gathering the templates
jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(TEMPLATE_LOCATION), autoescape=True)


class Handler(webapp2.RedirectHandler):
    """
    Handling the rendering the template.
    """

    def write(self, *args, **kwargs):
        self.response.write(*args, **kwargs)

    @staticmethod
    def render_str(template, **parms):
        t = jinja_env.get_template(template)
        return t.render(parms)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))


class Submission(db.Model):
    title = db.StringProperty(required=True)
    art = db.TextProperty(required=True)
    rate = db.IntegerProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)


class MainHandler(Handler):
    def get(self):
        self.render("index.html")


class Submit(Handler):
    def get(self):
        self.render("submit.html")

    def post(self):
        title = self.request.get("title")
        artwork = self.request.get("artwork")

        if title and artwork:
            new_art = Submission(title=title, art=artwork, rate=0)
            new_art.put()
            self.redirect("/gallery")
        else:
            self.render("submit.html", error="Both title and artwork are "
                                             "required!",
                        title_value=title,
                        artwork_value=artwork)


class Gallery(Handler):
    def get(self):
        arts = db.GqlQuery("SELECT * FROM Submission ORDER BY created DESC")

        if arts:
            self.render("gallery.html", arts=arts)
        else:
            self.render("index.html")

    def post(self):
        pass


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/submit', Submit),
    ('/gallery', Gallery),
], debug=True)
