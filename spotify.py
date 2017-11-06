import requests
from requests.auth import HTTPBasicAuth
import urllib


params = {"grant_type": "client_credentials"}

# token = requests.post("https://accounts.spotify.com/api/token", auth=HTTPBasicAuth(*auth), data=params).text
token = "BQBnGzw3ReuNRYEAp5EpfW9ClV0bAeNT3FqHeaP2FF6v35zXgA3m4P5Ofi7MaobYgwK-WRSsmdTj9WKiQQkhJA"


def whatever(track, artist):
    url = "https://api.spotify.com/v1/search?q=track:{track}+artist:{artist}&type=track&limit=1".format(track=urllib.quote_plus(track), artist=urllib.quote_plus(artist))

    result = requests.get(url, headers={'Authorization': "Bearer " + token}).text
    import json
    track = json.loads(result)["tracks"]["items"]
    if track:
        return json.loads(result)["tracks"]["items"][0]["uri"]
    return ""
# print whatever("Being Everyone", "After Forever")

with open("sample.csv") as f:
    artists = [item.split(",")[1] for item in f.readlines()]
    print(len(artists))
    print(len(set(artists)))
        # track, artist, _ = line.split(",")
        # print whatever(track, artist)