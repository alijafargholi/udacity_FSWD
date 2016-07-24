import logging
import re
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
        # Trailer ID
        trailer_id = get_trailer_id(name)
        # Story description
        story = content.find("div", {"class": "summary_text"}).text

        # Creating a tuple that contains the movie data
        data = (name, story, year, trailer_id, poster_url, genre)

        return data

    except IOError as e:
        logging.error(e)


def get_trailer_id(movie_name):
    """ It finds the YouTube movie trailer ID from the given name.
The+Secret+Life+of+Pets+trailer
    :param movie_name: (str) name of the movie.
    :return: (srt) YouTube movie trailer ID from YouTube
    """

    youtube_search_name = movie_name.replace(" ", "+") + "+Trailer"

    # TODO: Figure out why I need to use ssl!!
    # http://stackoverflow.com/questions/27835619/ssl-certificate-verify-failed
    # -error
    context = ssl._create_unverified_context()

    url = 'http://www.youtube.com/results?search_query=' + youtube_search_name

    conn = urlopen(url, context=context)
    content = conn.read()
    conn.close()

    soup_content = B.BeautifulSoup(content)

    # feeling lucky. Gathering the trailer info base on the assumption that
    # the  first hit is the main trailer
    # get the first thumbnail
    first_youtube_result = soup_content.find("span",
                                             {"class": "yt-thumb-simple"})
    # get the thumbnail image src path
    youtube_image_url = first_youtube_result.find("img").get("src")
    # gather the video id from the link, using regular expression.
    youtube_trailer_id_pattern = re.compile("vi/(.*)/")
    youtube_id = re.findall(youtube_trailer_id_pattern, youtube_image_url)[0]

    return youtube_id
