import requests
import xmltodict
import time
import os


API_KEY = os.environ.get("LASTFM_API_KEY")
SECRET = os.environ.get("LASTFM_SECRET")

assert API_KEY, "API key not set in environment. Did you run secrets.bat first?"
assert SECRET, "Secret not set in environment. Did you run secrets.bat first?"


class Listen():
    def __init__(self, artist, album, track, date):
        self.artist = artist
        self.album = album
        self.track = track
        self.date = int(date)

    def __str__(self):
        return str([self.artist, self.album, self.track, self.date])


listens_for_songs = {}


def song_discovered(listen_data):
    if len(listen_data) < 2:
        # INSUFFICIENT DATA FOR MEANINGFUL ANSWER
        return False
    latest_listen, prev_listen = listen_data[-1], listen_data[-2]
    if (latest_listen.date - prev_listen.date) < 5  * 60 * 60 * 24:
        return prev_listen


def generate_playlist(listens):
    """Walks through listen history starting from the listening history start.

    For every listen encountered, this will check when the last listen was to determine whether the song was discovered."""
    discovered_songs = {}
    for listen in listens:
        unique_song = (listen.track, listen.artist)
        latest_listen = listen
        listens_for_songs[unique_song] = \
            listens_for_songs.get(unique_song, []) + [latest_listen]
        total_listens = listens_for_songs[unique_song]
        discovered_date = song_discovered(total_listens)
        if discovered_date:
            discovered_songs[unique_song] = discovered_songs.get(
                unique_song, discovered_date)
    return discovered_songs


URL = "http://ws.audioscrobbler.com/2.0/?method=user.getRecentTracks"
query = "&user={}&api_key={}&from={}&to={}&limit=200"


def get_last_fm_data(username, start, end, listen_list):
    history = requests.get(URL + query.format(username, API_KEY, start, end)).text
    y = xmltodict.parse(history)
    tracks = y.get("lfm").get("recenttracks").get("track")
    if not tracks:
        return None
    for track in tracks:
        listen = Listen(track.get("artist").get("#text"), track.get("album").get("#text"), track.get("name"), track.get("date").get("@uts"))
        listen_list.append(listen)
        now = track.get("date").get("@uts")
    return now


def get_all_last_fm_data(username):
    """Returns all your Last.fm scrobbles in chronological order."""
    listens = []
    now = time.time()
    while now:
        now = get_last_fm_data(username, 1, now, listens)
    # The Last.FM API returns tracks in reverse chronological order, up to the maximum allowed per request.
    # This means it's far easier to return scrobbles in this order, but the algorithm needs to start from the beginning
    # - otherwise it will mark a song with a date corresponding to it's latest clustering in your history, rather than the first one which is what we're looking for.
    return listens[::-1]
