import requests
import urllib
import json
from requests.auth import HTTPBasicAuth


params = {"grant_type": "client_credentials"}

token_json = requests.post("https://accounts.spotify.com/api/token", auth=HTTPBasicAuth(*auth), data=params).text
token = json.loads(token_json)["access_token"]


def generate_spotify_url(track, artist, retry_attempted=False):
    url = "https://api.spotify.com/v1/search?q=track:{track}+artist:{artist}&type=track&limit=1".format(track=urllib.quote_plus(track), artist=urllib.quote_plus(artist))
    res = requests.get(url,
                          headers={'Authorization': "Bearer " + token})
    if res.status_code != 200:
        if res.status_code == 401:
            print "Refreshing token"
            if retry_attempted:
                raise RuntimeError("Oh shit")
            global token
            token_json = requests.post("https://accounts.spotify.com/api/token", auth=HTTPBasicAuth(*auth), data=params).text
            token = json.loads(token_json)["access_token"]
            if not retry_attempted:
                return generate_spotify_url(track, artist, True)
    result = res.text
    track = json.loads(result)["tracks"]["items"]
    if track:
        return json.loads(result)["tracks"]["items"][0]["uri"]
    return ""


import csv
import re


with open("wew.csv") as f:
    track_no = len(f.readlines())
    # files = f.readlines()
with open("spotify_playlist.txt", "w") as f:
    f.write("")

with open("wew.csv") as f:
    for line_no, line in enumerate(csv.reader(f, quotechar='"',delimiter=",",quoting=csv.QUOTE_ALL)):
        try:
            print "Writing track {} of {}".format(line_no + 1, track_no)
            track, artist, _ = line
            url = generate_spotify_url(track, artist)
            if not url:
                print "Track not found on Spotify: {} - {}".format(artist, track)
                pattern = r'{}[ -]*'.format(artist)
                artist_crap = re.findall(pattern, track, re.IGNORECASE)
                if artist_crap:
                    track = track.replace(artist_crap[0], "")
                    print "Artist found in track. Correcting possible scrobble error. Searching for {} - {}".format(artist, track),
                    url = generate_spotify_url(track, artist)
                    if url:
                        print "- Correction worked."
                    else:
                        print ""
            if url:
                with open("spotify_playlist.txt", "a") as g:
                    g.write(generate_spotify_url(track, artist) + "\n")
        except Exception as e:
            print e