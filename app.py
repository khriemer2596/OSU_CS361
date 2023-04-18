# Sources:
# Musixmatch API: https://developer.musixmatch.com/documentation
# Musixmatch API integration with Python:
# https://github.com/hudsonbrendon/python-musixmatch/blob/master/README.md

from flask import Flask, render_template, url_for, redirect, request
import requests
import os
from pymarkovchain import MarkovChain
from musixmatch import Musixmatch

API_KEY = os.environ.get("API_KEY")

musixmatch = Musixmatch(API_KEY)

app = Flask(__name__)
app.debug = True


@app.route("/", methods=["GET"])  # route for home page
def home():
    return render_template("home.html")


@app.route("/lyrics", methods=["POST"])  # route for lyrics page
def lyrics():
    artist = request.form["artist"]
    lines = int(request.form["lines"])
    number_of_tracks = (
        10  # use top 10 tracks per artist to generate new lyrics
    )

    if not artist:
        return redirect(url_for("home.html"))

    # Get a response of the top 10 tracks using artist name, sorted in
    # descending order
    uri = (
        "http://api.musixmatch.com/ws/1.1/track.search?apikey="
        + str(API_KEY)
        + "&q_artist="
        + str(artist)
        + "&f_has_lyrics=1&page_size="
        + str(number_of_tracks)
        + "&s_track_rating=desc"
    )
    response = requests.get(uri)
    track_info = response.json()
    track_list_id = []
    for i in range(
        0, number_of_tracks
    ):  # build list of top 10 track IDs for the artist
        track_list_id.append(
            track_info["message"]["body"]["track_list"][i]["track"]["track_id"]
        )
    # Get a response of the lyrics of the tracks in track_list_id using
    # musixmatch module
    lyric_list = []
    for track_id in track_list_id:  # iterate through track_list_id
        lyric_body = musixmatch.track_lyrics_get(
            track_id
        )  # use musixmatch module
        lyric_body_iso = lyric_body["message"]["body"]["lyrics"]["lyrics_body"]
        lyric_list.append(
            lyric_body_iso
        )  # build lyric list using isolated lyrics from track_list_id

    # Parse lyric list into a string of lyrics
    lyrics = ""
    for lyric in lyric_list:
        lyric_snip = lyric.removesuffix(
            "\n...\n\n******* This Lyrics is NOT for Commercial use *******\n(1409623310964)"
        )
        lyrics += lyric_snip

    # Use Markov Chain
    mc = MarkovChain()
    mc.generateDatabase(lyrics)

    # Append new lyrics to result
    result = []
    for line in range(0, lines):
        result.append(mc.generateString())

    return render_template("lyrics.html", result=result, artist=artist)


@app.route("/bands", methods=["GET"])  # route for bands page
def bands():
    return render_template("bands.html")


@app.route("/bands-country", methods=["POST"])  # route for bands-country page
def bands_country():
    country = request.form["country"]
    uri = (
        "https://api.musixmatch.com/ws/1.1/chart.artists.get?apikey="
        + str(API_KEY)
        + "&page=1&page_size=100&country="
        + country
    )
    print(uri)
    response = requests.get(uri)
    artist_sample = response.json()
    artist_sample_list = []

    length_of_artist_list = len(artist_sample["message"]["body"]["artist_list"])
    
    for i in range(0, length_of_artist_list):
        artist_sample_list.append(
            artist_sample["message"]["body"]["artist_list"][i]["artist"]["artist_name"]
        )

    return render_template(
        "bands-country.html",
        artist_sample_list=artist_sample_list,
        country=country.upper(),
    )


@app.route("/how_it_works", methods=["GET"])  # route for how_it_works page
def how_it_works():
    return render_template("how_it_works.html")


if __name__ == "__main__":
    app.run()
