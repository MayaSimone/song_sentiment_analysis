"""
Import library to help pull data from websites.
"""
import requests

"""
Import to Beautiful Soup to work with HTML files.
"""
from bs4 import BeautifulSoup

"""
Import the Natural Language Toolkit.
"""
import nltk

"""
Import the sentiment intensity analyzer function from the vader module.
"""
from nltk.sentiment.vader import SentimentIntensityAnalyzer

"""

Import module to manipulate strings.
"""
import string

"""
Import module of time-related functions.
"""
import time


def format_name(band_name):
    """
    Format `band_name` to be used in a link.

    Remove all spaces and punctuation from `band_name`, and replace all
    uppercase letters with their lowercase counterparts. This matches the name
    formatting used in the URLs for AZ lyrics.

    Args:
        band_name: A string

    Returns:
        A string that consists of `band_name` with no spaces, punctuation, or
        uppercase characters.
    """
    # Replace all uppercase letters in `band_name` with their 
    # lowecase counterparts.
    formatted_name = band_name.lower()
    # Remove all punctuation from `band_name`.
    formatted_name = formatted_name.translate(str.maketrans('', '', string.punctuation))
    # Remove all spaces from `band_name`.
    formatted_name = formatted_name.replace(" ", "")
    return formatted_name


def links_by_album(band_name):
    """
    Create a list of links to song lyrics of a given artist, organized by
    album.

    For a given artist, `band_name`, if AZ lyrics has a page for them, create
    a list of the links to all the songs in an album, then store these
    lists in another list that represents songs per album for all albums.

    Args:
        band_name: A string representing the name of an artist whose lyrics are
        on AZ lyrics.

    Returns:
        A list of lists of song links per album. The song links are strings.
    """
    # Format `band_name` to be used in a link.
    url_name = format_name(band_name)

    # Request a response from the named artist's page on the AZ lyrics server.
    r = requests\
        .get(f"https://www.azlyrics.com/{url_name[0]}/{url_name}.html")
    # Process the HTML page response using Beautiful Soup
    full_page = BeautifulSoup(r.text, 'html.parser')
    # Find all elements with the `listAlbum` ID. This includes album titles as
    # well as links to the lyrics of each song within the albums.
    total_songs = full_page.body.find(id="listAlbum")

    # Initalize parameters for the loop.
    # Set the current song to the first valid element in `total_songs`.
    current_song = total_songs.next_element.next_element
    # Create an empty list to store the lists of song links in.
    song_links_by_album = []
    # Set the initial album index to -1 (0 would map to the first album in the
    # list).
    album_index = -1

    # While `current_song` is not empty, run through this loop
    while current_song != None:
        try:
            # If `current_song` is an album, add a new list within
            # `song_links_by_album` and increase the album index by one.
            if current_song["class"] == ["album"]:
                song_links_by_album.append([])
                album_index += 1
            # If `current_song` has a class, but the class is not "album", then
            # take the link from this element, and add it to it's respective
            # album list.
            else:
                # Some artists on AZ Lyrics have not released an album, so no
                # elements have an "album" class. This allows prevents an
                # indexing error in those cases.
                if album_index == -1:
                    album_index = 0
                song_links_by_album[album_index].append(current_song.a["href"])
            # Set `current_song` to the next valid sibling.
            current_song = current_song.next_sibling.next_sibling
        # If the current_song element has no class, resulting in a key error,
        # stop the loop.
        except KeyError:
            break

    # Return the list of album lists.
    return song_links_by_album

def get_album_titles(band_name):
    """
    Create a list of album titles of a given artist.

    For a given artist, `band_name`, if AZ lyrics has a page for them, create
    a list of all their album titles.

    Args:
        band_name: A string representing the name of an artist whose lyrics are
        on AZ lyrics.

    Returns:
        A list of album titles as strings.
    """

    # Format `band_name` to be used in a link.
    url_name = format_name(band_name)

    # Request a response from the named artist's page on the AZ lyrics server.
    r = requests\
        .get(f"https://www.azlyrics.com/{url_name[0]}/{url_name}.html")
    # Process the HTML page response using Beautiful Soup
    full_page = BeautifulSoup(r.text, 'html.parser')
    # Find all elements with the `listAlbum` ID. This includes album titles as
    # well as links to the lyrics of each song within the albums.
    page_body = full_page.body.find(id="listAlbum")

    # Initalize parameters for the loop
    # Set the current song to the first valid element in `total_songs`
    current_element = page_body.next_element.next_element
    # Create an empty list to store the album titles.
    album_titles = []

    # While `current_element` is not empty, run through this loop
    while current_element != None:
        try:
            # If `current_element` is an album, add the text component of this
            # element to the list of album titles. Remove any characters
            # preceding the first ':' in the string to remove the "Album: " or
            # "EP: " labels.
            if current_element["class"] == ["album"]:
                album_titles.append(current_element.get_text()\
                    .split(":",1)[1][1:])
            current_element = current_element.next_sibling.next_sibling
        # If the `current_element` has no class, resulting in a key error,
        # stop the loop.
        except KeyError:
            break
    # Some artists have an extra section of songs at the end of their page that
    # are not a part of any album and are listed under "Other Songs". Since
    # there is no ":" in that title, an empty string is added to the end of the
    # title list. The empty string is then replaced by "Other Songs".
    if album_titles[-1] == "":
        album_titles[-1] = "Other Songs"
    # Return the list of album titles.
    return album_titles


def collate_lyrics(band_name):
    """
    Create a list of strings of all the songs in an album, per album.

    For a given artist, `band_name`, if AZ lyrics has a page for them, add the
    lyrics of every song in an album to a string. Then, add this string to the
    list `lyrics_by_album`.

    Args:
        band_name: A string representing the name of an artist whose lyrics are
        on AZ lyrics.

    Returns:
        A list of all the lyrics from an artist,`band_name`, separated by
        album. The lyrics are stored in strings.
    """

    # Create a list of the links to every song lyric page, separated by album.
    album_links_list = links_by_album(band_name)
    # Create an empty list to store the lyrics strings.
    lyrics_by_album = []

    # For each list in `album_links_list`, run this loop.
    for album in album_links_list:
        # Create an empty string to store the lyrics from each song.
        total_lyrics = ""
        
        # For each song lyrics link in the `album` list, run this loop.
        for song in album:
            # Request a response from the lyrics page on the AZ lyrics server.
            r = requests.get(f"https://www.azlyrics.com{song[2:]}")
            # Process the HTML page response using Beautiful Soup
            song_page =  BeautifulSoup(r.text, 'html.parser')
            # Find the element with the class `"ringtone"`.
            page_body = song_page.find(class_="ringtone")
            # Create a start point of elements to look at.
            start_point = page_body.next_sibling.next_sibling.next_sibling\
                .next_sibling.next_sibling
            try:
                # If the page has a line under the song title naming a
                # featuring artist or original artist of the song, the song
                # lyrics will be further down the page.
                if start_point["class"] == ["feat"]:
                    lyrics = start_point.next_sibling.next_sibling\
                        .next_sibling.next_sibling.next_sibling
                    # Add the song lyrics to the string of all the song lyrics
                    # in the album.
                    total_lyrics += lyrics.get_text()
            except KeyError:
                # If the page doesn't have a featuring line under the song
                # title, the lyrics will be further up the page.
                lyrics = start_point.next_sibling.next_sibling
                # Add the song lyrics ot the string of all the song lyrics in
                # the album.
                total_lyrics += lyrics.get_text()
            # Add a 10 second pause to each loop, to prevent AZ lyrics from
            # banning the user's IP address for requesting data too frequently.
            time.sleep(10)
        # Add the string of all the lyrics from an album to a list.
        lyrics_by_album.append(total_lyrics)
    # Return the list of song lyrics by album.
    return lyrics_by_album


def analyze_sentiment(band_name="falloutboy"):
    """
    Analyze the sentiment of the lyrics of a given artist, by album.

    For a given artist, `band_name`, if AZ lyrics has a page for them, conduct
    sentiment analysis on the lyrics of each album, using the Vader module of
    the Natural Langauge Toolkit.

    Args:
        band_name: A string representing the name of an artist whose lyrics are
        on AZ lyrics.

    Returns:
        A list of lists representing the positive, negative, and compound
        sentiment scores of each album. The first list is the positive scores,
        the second the negative scores, and the last list is the compound
        scores. The sentiment scores are floats.
    """

    # Create a list of all of an artist's song lyrics, separated by album.
    album_lyrics = collate_lyrics(band_name)
    # Create a list of all the album titles from the artist.
    album_list = get_album_titles(band_name)

    # Assign the Sentiment Intensity Analyzer function to a shorter variable
    # name.
    sia = SentimentIntensityAnalyzer()

    # Some artists have an extra section of songs at the end of their page that
    # are not a part of any album so they are labelled under "Other Songs".
    # This is not a legitimate album, so no sentiment analyis should be
    # conducted on that list of lyrics.
    if album_list[-1] == "Other Songs":
        num_albums = len(album_list) - 1
    else:
        num_albums = len(album_list)

    # Create empty lists to store the positive, negative, and compound
    # sentiment scores of each album.
    pos_score = []
    neg_score = []
    comp_score = []

    # For each album of an artist, conduct sentiment analysis on all the
    # lyrics, and save the positive, negative, and compound sentiment scores to
    # their respective lists.
    for album_index in range(num_albums):
        ss = sia.polarity_scores(album_lyrics[album_index])
        pos_score.append(ss["pos"])
        neg_score.append(ss["neg"])
        comp_score.append(ss["compound"])

    # Return a list of the positive, negative, and compound sentiment score lists.
    return [pos_score, neg_score, comp_score]
