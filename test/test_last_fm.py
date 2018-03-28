import last_fm
import time
import requests_mock


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