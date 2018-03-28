import last_fm
import time
import requests_mock
import pytest


MY_USER = "Cookie_crumbs"


def test_get_last_fm_data():
    listen_list = []
    with requests_mock.mock() as m:
        with open("test.xml") as f:
            mock_xml = f.read()
        m.get(last_fm.URL, text=mock_xml)
        last_track_date = last_fm.get_last_fm_data(MY_USER, time.time(), time.time(), listen_list)
        listen = listen_list[0]

        assert isinstance(listen, last_fm.Listen)
        assert listen.album
        assert listen.artist
        assert listen.date
        assert listen.track
        assert int(last_track_date)


day_zero = 1000000
NICE_TRACK = "Stockholm Syndrome"
MEH_TRACK = "Hysteria"
BAD_TRACK = "Intro"
SLOW_BURNER_TRACK = "Fury"

DISCOVERED_OFTEN = last_fm.Listen("Muse", "Absolution", NICE_TRACK, day_zero)
LISTENED_OFTEN = [
    DISCOVERED_OFTEN,
    last_fm.Listen("Muse", "Absolution", NICE_TRACK, day_zero + 24 * 60 * 60),
    last_fm.Listen("Muse", "Absolution", NICE_TRACK, day_zero + 24 * 60 * 60 + 100),
    last_fm.Listen("Muse", "Absolution", NICE_TRACK, day_zero + 24 * 60 * 60 + 200),]

DISCOVERED_SB = last_fm.Listen("Muse", "Absolution", SLOW_BURNER_TRACK, day_zero + 24 * 60 * 60 * 16)

HATED_INITIALLY = [
    last_fm.Listen("Muse", "Absolution", SLOW_BURNER_TRACK, day_zero),
    last_fm.Listen("Muse", "Absolution", SLOW_BURNER_TRACK, day_zero + 24 * 60 * 60 * 10),
    DISCOVERED_SB,
    last_fm.Listen("Muse", "Absolution", SLOW_BURNER_TRACK, day_zero + 24 * 60 * 60 * 16 + 100),]

LISTENED_INFREQUENTLY = [
    last_fm.Listen("Muse", "Absolution", MEH_TRACK, day_zero + 23 * 60 * 60 ),
    last_fm.Listen("Muse", "Absolution", MEH_TRACK, day_zero + 24 * 60 * 60 * 7),
]

LISTENED_ONCE = [
    last_fm.Listen("Muse", "Absolution", BAD_TRACK, day_zero + 24 * 60 * 60 * 8),
]

ALL_LISTENS = sorted(LISTENED_OFTEN + LISTENED_ONCE + LISTENED_INFREQUENTLY + HATED_INITIALLY, key=lambda x: x.date)


def test_generate_playlist():
    playlist = last_fm.generate_playlist(ALL_LISTENS)
    assert set(playlist.values()) == set((DISCOVERED_OFTEN, DISCOVERED_SB))
