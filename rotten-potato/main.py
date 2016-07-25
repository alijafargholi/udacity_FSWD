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
# Import Standard Libraries
import os
import webapp2
import jinja2
import time

# Import Google app database
from google.appengine.ext import db

# Import local modules
import gather_movie_data

# Location of HTML templates
TEMPLATE_LOCATION = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                 "templates")

# Gathering the templates
jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(TEMPLATE_LOCATION), autoescape=True)


class Movies(db.Model):
    """ This is the entity for storing the movie's data into the database.
    """

    name = db.StringProperty(required=True)
    story = db.TextProperty(required=True)
    year = db.IntegerProperty(required=True)
    trailer_id = db.StringProperty(required=True)
    poster_url = db.StringProperty(required=True)
    genre = db.StringProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)


class Handler(webapp2.RedirectHandler):
    """ Handling the rendering the template.
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
    """ The main handler to show the home page.
    """
    def get(self):
        # gather all the existing data from the database and sort it by the
        # data added
        movies = db.GqlQuery("SELECT * FROM Movies ORDER BY created DESC")

        # Render out the home page and pass in the movies info
        self.render("index.html", movies=movies)

    def post(self):
        """ It handles new imdb link submission. Once a new link is posted,
        it'll scrap the data from the imdb page and add the info to the
        database and reload the page.
        """

        # get the new link
        new_link = self.request.get("imdb_link")

        # scrap the given url
        new_movie_data = gather_movie_data.get_movie_info(new_link)

        # save the data into the database
        new_movie = Movies(name=new_movie_data[0],
                           story=new_movie_data[1],
                           year=int(new_movie_data[2]),
                           trailer_id=new_movie_data[3],
                           poster_url=new_movie_data[4],
                           genre=new_movie_data[5])
        new_movie.put()

        # Wait for 2 seconds and make sure the data is added to the database
        # so when the page is reloaded it shows the just added movie.
        time.sleep(2)
        self.redirect("/")


app = webapp2.WSGIApplication([
    ('/', MainHandler),
], debug=True)
