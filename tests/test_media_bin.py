import datetime as dt
from pathlib import Path


def test_number_of_media(simple_video):
    assert len(list(simple_video.media_bin)) == 2


def test_media_contents(simple_video):
    media = list(simple_video.media_bin)

    assert media[0].source == Path(
        "./recordings/1559817572.462711/Rec 6-6-2019.trec")
    assert media[0].rect == (0, 0, 5120, 2880)
    assert media[0].last_modification == dt.datetime(
        year=2019, month=6, day=6, hour=10, minute=38, second=30)

    assert media[1].source == Path(
        "./media/1562574964.179914/Screenshot 2019-07-08 at 08.52.00.png")
    assert media[1].rect == (0, 0, 970, 334)
    assert media[1].last_modification == dt.datetime(
        year=2019, month=7, day=8, hour=6, minute=52, second=5)
