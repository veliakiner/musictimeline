import dateutil.parser


class Listen():
    def __init__(self, artist, album, track, date):
        self.artist = artist
        self.album = album
        self.track = track
        self.date = date

    def __str__(self):
        return str([self.artist, self.album, self.track, self.date])


listens = []
with open("C:/Users/Veli/Downloads/sample.csv") as f:
    for record in f.readlines()[::-1]:
        data = record.split(",")
        data[-1] = dateutil.parser.parse(data[-1], dayfirst=True)
        listens.append(Listen(*data))


periods = "year", "month", "day"


def artist_discovered(filter_on="Imaginaerum", attribute="song", selected_period=()):
    # for listen in listens:
    #     if getattr(listen, attribute) == filter_on:
    #         return listen.date, listen.track, listen.album, listen.artist
    relevant_listens = filter(lambda x: getattr(x, attribute).lower() == filter_on.lower(), listens)
    years = {}


    subperiods = periods[:len(selected_period) + 1]

    smallest_division = subperiods[-1]

    for listen in relevant_listens:
        if all([getattr(listen.date, subperiods[i]) == selected_period[i] for i in range(len(subperiods) - 1) ]):
            years[getattr(listen.date, smallest_division)] = years.get(getattr(listen.date, smallest_division), 0) + 1

    threshold = sum(years.values()) / len(years.keys())
    # threshold = 3
    year_discovered = None
    for key in sorted(years.keys()):
        if years[key] >= threshold and not year_discovered:
            year_discovered = key

        print key, years[key]

    return year_discovered


# print artist_discovered()
# print artist_discovered("Dark Passion Play", "album")
# print artist_discovered("Silhouette", "track")

# date = []
# for _ in range(3):
#     date.append(artist_discovered("Dystopia", "track", date))
# print(date)

listens_for_songs = {}
discovered_songs = {}



def song_discovered(listen_data):
    if len(listen_data) < 2:
        # INSUFFICIENT DATA FOR MEANINGFUL ANSWER
        return False
    latest_listen, prev_listen = listen_data[-1], listen_data[-2]
    if (latest_listen - prev_listen).days < 5:
        return prev_listen



current_day = None
for listen in listens:
    unique_song = (listen.track, listen.artist)
    latest_listen = listen.date.date()
    listens_for_songs[unique_song] = listens_for_songs.get(unique_song, []) + [latest_listen]
    total_listens = listens_for_songs[unique_song]
    discovered_date = song_discovered(total_listens)
    if discovered_date:
        discovered_songs[unique_song] = discovered_songs.get(unique_song, discovered_date)


with open("test.res", "w") as f:
    for item in sorted(discovered_songs.keys(), key=lambda x: discovered_songs[x]):
        f.write(str(item))
        f.write(" ")        
        f.write(str(discovered_songs[item]))
        f.write("\n")

with open("test.res") as f:
    with open("two.res") as g:
        assert f.readlines() == g.readlines()
        print "Test for algorithm consistency passed"