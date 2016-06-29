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
import re

import webapp2
import jinja2

# Location of HTML templates
TEMPLATE_LOCATION = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                 "templates")

# GLOBAL VARIABLES
# ReEx pattern for inputs
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")

# username to pass to welcome page
USERNAME = ""

# Gathering the templates
jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(TEMPLATE_LOCATION), autoescape=True)

index_template = jinja_env.get_template('index.html')
sign_up_template = jinja_env.get_template('user_signup.html')
welcome_page_template = jinja_env.get_template('welcome_page.html')


# Verifying the username input
def verify_username(pass_phrase):
    if not USER_RE.match(pass_phrase):
        return "That wasn't a valid username."
    return ""


# Verifying the password input
def verify_password(pass_phrase):
    if not PASSWORD_RE.match(pass_phrase):
        return "That wasn't a valid password."
    return ""


# Verifying the email input
def verify_email(pass_phrase):
    if not EMAIL_RE.match(pass_phrase):
        return "That's not a valid email."
    return ""


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
    """
    Rendering the index page.
    """
    def get(self):
        self.render(index_template)

    def post(self):
        self.redirect("/signup")


class SignUpPage(Handler):
    """
    Rendering the Sign Up page and validating the inputs.
    """
    def get(self):
        self.render(sign_up_template)

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        username_error = verify_username(username)
        password_error = verify_password(password)
        email_error = verify_email(email)

        if password != verify:
            verify_error = "Your passwords didn't match."
        else:
            verify_error = ""

        if (username_error or password_error or verify_error or
                email_error):
            self.render(sign_up_template,
                        username_error=username_error,
                        password_error=password_error,
                        verify_error=verify_error,
                        email_error=email_error,
                        old_username=username,
                        old_email=email)
        else:
            global USERNAME
            USERNAME = username
            self.redirect('/welcome')


class WelcomePage(Handler):
    """
    Rendering the welcome page once the inputs are verified.
    """
    def get(self):
        global USERNAME
        self.render(welcome_page_template, username=USERNAME)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/signup', SignUpPage),
    ('/welcome', WelcomePage),
], debug=True)
