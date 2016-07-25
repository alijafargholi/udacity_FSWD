                      Rotten-Potato (Project1: Movie Trailer Website)

What is it?
-----------

It's first project of the Full Stack Web Developer Nanodegree form Udacity. The
Goal of this project is a simple website that shows my favorite movies.

Here is the link to the app: [**Rotten-Potato**](http://rotten-potato.appspot.com/)

How it does it?
----------------

The requirement of this project was to have the list of the movies and
information regarding the movie, such as the name, trailer URL, poster URL,
and so on, hard-coded and created as an python class. But I wanted to make
it some what dynamic that you can copy the information form the movie's IMDB
link and story it into a database. Once you give the link to the movie's imdb
 page, via [BeautifulSoup](https://www.crummy
 .com/software/BeautifulSoup/bs4/doc/), the app pulls the data form the imdb
 page and stores the needed data, such as the name, poster url, into the
 database. Once the new data is added to the database, it'll reload the page
 and pulls all the saved movies information from the database and show them
 on the page.

Installation
------------

This app is using [Google App Engine](https://console.cloud.google.com) so make sure you have that
[installed](https://cloud.google.com/appengine/downloads). It also requires **Jinja2**, **Webapp2** and **sll**. To install
them you can manually do that or use the following to install it while your
at root of the project directory:

```pip install -r requirements.txt```

Licensing
---------

[THE BEER-WARE LICENSE](https://en.wikipedia.org/wiki/Beerware)


Contacts
--------

If you have question or concern regarding this app, please feel free to
[contact me](http://alijafargholi.com/contact/).
