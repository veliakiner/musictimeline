


def song_discovered(listen_data):
    if len(listen_data) < 2:
        # INSUFFICIENT DATA FOR MEANINGFUL ANSWER
        return False
    latest_listen, prev_listen = listen_data[-1], listen_data[-2]
    if (latest_listen - prev_listen).days < 5:
        return prev_listen


def generate(listens):
listens_for_songs = {}
discovered_songs = {}
for listen in listens:
    unique_song = (listen.track, listen.artist)
    latest_listen = listen.date.date()
    listens_for_songs[unique_song] = listens_for_songs.get(unique_song, []) + [latest_listen]
    total_listens = listens_for_songs[unique_song]
    discovered_date = song_discovered(total_listens)
    if discovered_date:
        discovered_songs[unique_song] = discovered_songs.get(unique_song, discovered_date)
    return discovered_songs


def write_playlist(data):
    with open("playlist.csv", "w") as f:
        for item in sorted(discovered_songs.keys(), key=lambda x: discovered_songs[x]):
            for thing in (item[0], ",", item[1], ",", discovered_songs[item],"\n"):
                f.write(str(thing))
