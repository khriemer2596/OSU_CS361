from flask import Flask, render_template, url_for, redirect, request
import requests
import os
from pymarkovchain import MarkovChain  # can't get markov chain imported

API_KEY = os.environ.get('API_KEY')

app = Flask(__name__)
app.debug = True

@app.route('/', methods=['GET'])
def index():
    return render_template('home.html')

@app.route('/lyrics', methods=['POST'])
def lyrics():
    artist = request.form['artist']
    lines = int(request.form['lines'])

    if not artist:
        return redirect(url_for('index'))

    # Get a response of the top 5 tracks from artist name - have to pass api key in url: https://api.musixmatch.com/ws/1.1/track.search?apikey=keygoeshere&q_artist=justin%20bieber 
    uri = "http://api.musixmatch.com/ws/1.1/track.search?apikey=" + str(API_KEY) + "q_artist=" + str(artist) + "&f_has_lyric=1&page_size=5&s_track_rating=asc"
    params = {
        'api_key': API_KEY,
        'artist': artist,
    }
    response = requests.get(uri, params=params)
    track_list = response.json()
    
    # Get a response of the lyircs of popular tracks from artist name - not sure if this is working
    uri_2 = "http://api.musixmatch.com/ws/1.1/track.lyrics.get?apikey=" + str(API_KEY) + "track_id=" + str(track_list)
    params_2 = {
        'api_key': API_KEY,
        'artist': artist,
    }
    response = requests.get(uri_2, params=params_2)
    lyric_list = response.json()
    
    # Parse results into a long string of lyrics
    lyrics = ''
    for lyric_dict in lyric_list:
        lyrics += lyric_dict['snippet'].replace('...', '') + ' '

    # Generate a Markov model
    mc = MarkovChain()
    mc.generateDatabase(lyrics)

    # Add lines of lyrics
    result = []
    for line in range(0, lines):
        result.append(mc.generateString())    
    
    return render_template('lyrics.html', result=['hello', 'world'], artist=artist)

if __name__ == '__main__':
    app.run()