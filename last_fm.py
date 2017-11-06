import dateutil.parser


class Listen():
    def __init__(self, artist, album, track, date):
        self.artist = artist
        self.album = album
        self.track = track
        self.date = date

    def __str__(self):
        return str([self.artist, self.album, self.track, self.date])


def read_csv(path):
    listens = []
    with open(path) as f:
        for record in f.readlines()[::-1]:
            data = record.split(",")
            data[-1] = dateutil.parser.parse(data[-1], dayfirst=True)
            listens.append(Listen(*data))
    print("Opened data source")
    return listens


listens_for_songs = {}


def song_discovered(listen_data):
    if len(listen_data) < 2:
        # INSUFFICIENT DATA FOR MEANINGFUL ANSWER
        return False
    latest_listen, prev_listen = listen_data[-1], listen_data[-2]
    if (latest_listen - prev_listen).days < 5:
        return prev_listen


def generate_playlist(listens):
    discovered_songs = {}
    for listen in listens:
        unique_song = (listen.track, listen.artist)
        latest_listen = listen.date.date()
        listens_for_songs[unique_song] = \
            listens_for_songs.get(unique_song, []) + [latest_listen]
        total_listens = listens_for_songs[unique_song]
        discovered_date = song_discovered(total_listens)
        if discovered_date:
            discovered_songs[unique_song] = discovered_songs.get(
                unique_song, discovered_date)
    return discovered_songs


def write_playlist_to_file(discovered_songs, output_file):
    with open(output_file, "w") as f:
        for item in sorted(
                discovered_songs.keys(), key=lambda x: discovered_songs[x]):
            for thing in (item[0], ",", item[1], ",",
                          discovered_songs[item], "\n"):
                f.write(str(thing))


if __name__ == "__main__":
    path = "C:/Users/Veli/Downloads/Cookie_crumbs.csv"
    playlist = generate_playlist(read_csv(path))
    write_playlist_to_file(playlist, "veli's songs.csv")
