import requests
from urllib.parse import quote_plus
import json
from requests.auth import HTTPBasicAuth
import os
import re


SPOTIFY_KEY = os.environ.get("SPOTIFY_KEY")
SPOTIFY_SECRET = os.environ.get("SPOTIFY_SECRET")
auth = [SPOTIFY_KEY, SPOTIFY_SECRET]


params = {"grant_type": "client_credentials"}


def generate_spotify_url(track, artist):
    token_json = requests.post("https://accounts.spotify.com/api/token", auth=HTTPBasicAuth(*auth), data=params).text
    token = json.loads(token_json)["access_token"]
    url = "https://api.spotify.com/v1/search?q=track:{track}+artist:{artist}&type=track&limit=1".format(track=quote_plus(track), artist=quote_plus(artist))
    res = requests.get(url,
                       headers={'Authorization': "Bearer " + token})
    result = res.text
    track = json.loads(result)["tracks"]["items"]
    if track:
        return json.loads(result)["tracks"]["items"][0]["uri"]
    return ""


def generate_url(track, artist):
    try:
        url = generate_spotify_url(track, artist)
        if not url:
            print("Track not found on Spotify: {} - {}".format(artist, track))
            pattern = r'{}[ -]*'.format(artist)
            artist_crap = re.findall(pattern, track, re.IGNORECASE)
            if artist_crap:
                track = track.replace(artist_crap[0], "")
                print("Artist found in track. Correcting possible scrobble error. Searching for {} - {}".format(artist, track),)
                url = generate_spotify_url(track, artist)
                if url:
                    print("- Correction worked.")
                else:
                    print("")
        if url:
            print(url)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    generate_url("Psycho", "System of a Down")
