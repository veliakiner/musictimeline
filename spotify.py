import requests
import urllib
import json
from requests.auth import HTTPBasicAuth


params = {"grant_type": "client_credentials"}

# token = requests.post("https://accounts.spotify.com/api/token", auth=HTTPBasicAuth(*auth), data=params).text
token = "BQBY56HOjdVj7LW9JKMQC2_90hFmwOHU8WkOC5EBAs-raSPwGd5Y51Lo6raZmfEjYR-dJrtweLk22IBhwCw"
# print token


def generate_spotify_url(track, artist):
    url = "https://api.spotify.com/v1/search?q=track:{track}+artist:{artist}&type=track&limit=1".format(track=urllib.quote_plus(track), artist=urllib.quote_plus(artist))
    res = requests.get(url,
                          headers={'Authorization': "Bearer " + token})
    assert res.status_code == 200
    result = res.text
    track = json.loads(result)["tracks"]["items"]
    if track:
        return json.loads(result)["tracks"]["items"][0]["uri"]
    return ""


import csv


with open("test.csv") as f:
    track_no = len(f.readlines())
with open("test.csv") as f:

    for line_no, line in enumerate(csv.reader(f, quotechar='"',delimiter=",",quoting=csv.QUOTE_ALL)):
        print "Writing track {} of {}".format(line_no + 1, track_no)
        track, artist, _ = line.split(",")
        with open("spotify_playlist.txt", "a") as f:
            f.write(generate_spotify_url(track, artist) + "\n")