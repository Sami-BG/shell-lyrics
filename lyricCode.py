import os
import sys
import time
import json
import spotipy
import urlfetch
import requests
from bs4 import BeautifulSoup
import spotipy.util as util

#GENIUS_CLIENT_ID = 'hOWGPvlo2PW8B9kxMjoO_iPdKOoDf4ezKquD4nuByUwLf5QB6LvcryU7O-W72Rkt'
#GENIUS_CLIENT_SECRET = genius_secret

#browses Genius' database and finds the URL of the lyrics page for song_title, artist_name
def geniusLyrics(song_title, artist_name):
    token = '04fBxzwfDZlmqkf_rOGdMnr75nORvaIbuHbE3aS6ts7-6hIuTx1dWUBH5_HF2u1R'
    base_url = 'https://api.genius.com'
    headers = {'Authorization': 'Bearer ' + token}
    search_url = base_url + '/search'
    data = {'q': song_title + ' ' + artist_name}
    genius_response = requests.get(search_url, data=data, headers=headers)
# Search for matches in the request response
    json = genius_response.json()
    trackData = None
    for match in json['response']['hits']:
        if artist_name.lower() in match['result']['primary_artist']['name'].lower():
            trackData = match
            break
    if trackData:
        trackURL = trackData['result']['url']
        scrapSongLyrics(trackURL)
    else:
        print("No lyrics found!")

#scraps the lyrics page on the Genius site for the lyrics and prints
def scrapSongLyrics(url):
    page = requests.get(url)
    html = BeautifulSoup(page.text, 'html.parser')
    lyrics = html.find('div', class_='lyrics').get_text()
    if not lyrics.strip():
        lyrics = "No lyrics!"
    print(lyrics)

#returns a string of the track artist of a given track
def getArtistName(track):
    return track['item']['album']['artists'][0]['name']

#returns a string of the track name of a given track
def getTrackName(track):
    return track['item']['name']

#checks track equality between 2 tracks. this is done because the same track retrieved
#at different times has different timestamps.
def tracksEqual(trackA, trackB):
    return getArtistName(trackA) == getArtistName(trackB) and getTrackName(trackA) == getTrackName(trackB)


SPOTIPY_CLIENT_ID = '8be03ebe381c49f6a5f678e50dc906bc'
SPOTIPY_CLIENT_SECRET = spotify_secret
SPOTIPY_REDIRECT_URI = 'http://google.com/'

scope = 'user-read-currently-playing'
cache = '.spotipyoauthcache'
#sets the client_id, client_secret, redirect_uri as environment variables on the local machine
def set_environ(client_id, client_secret, redirect_uri):
    os.environ["SPOTIPY_CLIENT_ID"] = client_id
    os.environ["SPOTIPY_CLIENT_SECRET"] = client_secret
    os.environ["SPOTIPY_REDIRECT_URI"] = redirect_uri

set_environ(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI)


username=""

#opens URL that prompts user to sign in to their spotify and redirects them to url
#with the code. prompts them to paste the code so we can extract token
try:
    token = util.prompt_for_user_token(username, scope)
except:
    token = util.prompt_for_user_token(username, scope)

#we create our spotify Object using obtained token
spotifyObject = spotipy.Spotify(auth=token)

#loop that checks the track. prints lyrics if it didnt before.
def masterLoop():

      currentTrack = spotifyObject.current_user_playing_track()
      prevTrack = currentTrack
      ifCounter = 0
      while True:
          currentTrack = spotifyObject.current_user_playing_track()
          try:
              time.sleep(0.5)
          except KeyboardInterrupt:
                      print("Goodbye!")
                      sys.exit(1)
          # if condition detects track change.
          # current track must exist, and:
          #               tracks must be different
          #               or first time going through if statement
          if currentTrack is not None and (ifCounter == 0 or not tracksEqual(prevTrack, currentTrack)):
              ifCounter = ifCounter + 1
              prevTrack = currentTrack
              #Artist for the current track.
              trackArtist = getArtistName(currentTrack)
              #Current track's name
              trackName = getTrackName(currentTrack)

              print("---------------------------------------------------------")
              print(getTrackName(currentTrack) + " by " + getArtistName(currentTrack))
              geniusLyrics(trackName, trackArtist)
              print("^ are lyrics for " + getTrackName(currentTrack) + " by " + getArtistName(currentTrack))
              print("Press Ctrl+C to quit.")


masterLoop()
