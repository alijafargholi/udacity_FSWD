import logging
import re
import urllib
from urllib  import urlencode
from urllib2 import urlopen
import ssl
import BeautifulSoup as B


def get_movie_info(url_link):
    """
    Returns some info from the given movie url

    :param url_link: (str) link to the movie on IMDB.
    :return: (list) list of info regarding the movie
    """
    try:
        content = B.BeautifulSoup(urlopen(url_link).read())
        # Name
        find_name = content.findAll("h1", {"itemprop": "name"})
        name = find_name[0].text.split(";")[0].strip("&nbsp")
        # Year
        find_year = content.findAll("span", {"id": "titleYear"})
        year = find_year[0].text.strip("(").strip(")")
        # Genres
        genres = content.findAll("span", {"itemprop": "genre"})
        genre = " - ".join([item.text for item in genres])
        # Poster URL
        find_poster_url = content.find("div", {"class": "poster"})
        poster_url = find_poster_url.find("img").get("src")
        # Trailer URL
        trailer_url = get_tailer_url(name)
        # Story description
        story = content.find("div", {"class": "summary_text"}).text

        # Creating a tuple that contains the movie data
        data = (name, story, year, trailer_url, poster_url, genre)

        return data

    except IOError as e:
        logging.error(e)


def get_tailer_url(movie_name):
    """ It finds the YouTube movie trailer from the given name.

    :param movie_name: (str) name of the movie.
    :return: (srt) YouTube movie trailer url
    """

    youtube_search_name = movie_name.replace(" ", "+") + "+Trailer"

    # http://stackoverflow.com/questions/27835619/ssl-certificate-verify-failed
    # -error
    context = ssl._create_unverified_context()

    url = 'http://www.youtube.com/results?search_query=' + youtube_search_name

    conn = urlopen(url, context=context)
    content = conn.read()
    conn.close()

    soup_content = B.BeautifulSoup(content)

    # feeling lucky
    first_youtube_result = soup_content.find("span",
                                             {"class": "yt-thumb-simple"})

    youtube_image_url = first_youtube_result.find("img").get("src")
    youtube_trailer_id_pattern = re.compile("vi/(.*)/")
    youtube_id = re.findall(youtube_trailer_id_pattern, youtube_image_url)[0]

    youtube_trailer_url = "https://www.youtube.com/watch?v=" + youtube_id

    return youtube_trailer_url
