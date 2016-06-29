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

import jinja2
import webapp2


# GLOBAL VARIABLE
ALPHABET = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
            'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

TEMPLATE_LOCATION = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                 "templates")
jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(TEMPLATE_LOCATION), autoescape=True)

index_template = jinja_env.get_template("index.html")


class MainHandler(webapp2.RequestHandler):
    @staticmethod
    def rot_it(phrase):
        new_phrase = ''
        for i in phrase:
            if i.isalpha():
                new_index = ALPHABET.index(i.lower())+13
                if new_index > 25:
                    new_index -= 26
                new_character = ALPHABET[new_index]
                if i.isupper():
                    new_character = new_character.upper()
                new_phrase += new_character
                continue
            else:
                new_phrase += i
        return new_phrase

    def get(self):
        self.response.write(index_template.render())

    def post(self):
        new_data = self.request.get("text")

        self.response.write(index_template.render(data=self.rot_it(new_data)))


app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
