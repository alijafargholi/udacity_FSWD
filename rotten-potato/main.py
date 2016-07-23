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

# Import local modules
import gather_movie_data

# Location of HTML templates
TEMPLATE_LOCATION = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                 "templates")

# Gathering the templates
jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(TEMPLATE_LOCATION), autoescape=True)

TEMP = gather_movie_data.get_movie_info("http://www.imdb.com/title/tt0120737/")


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


class MainHandler(Handler):
    def get(self):
        self.render("index.html", movies=[TEMP])


app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
