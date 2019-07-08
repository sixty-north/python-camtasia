from itertools import islice

from camtasia.frame_stamp import FrameStamp
from camtasia.timeline.marker import Marker


def test_authoring_client(simple_video):
    ac = simple_video.authoring_client
    assert ac.name == 'Camtasia'
    assert ac.platform == 'Mac'
    assert ac.version == '2019.0.1'


def test_edit_rate(simple_video):
    assert simple_video.edit_rate == 30


def test_number_tracks(simple_video):
    assert len(list(simple_video.timeline.tracks)) == 1


def test_first_track(simple_video):
    track = next(islice(simple_video.timeline.tracks, 1))
    assert track.name == 'populated-track'
    assert not track.audio_muted
    assert not track.video_hidden


def test_first_track_medias(simple_video):
    track = next(islice(simple_video.timeline.tracks, 1))
    media = next(islice(track.medias, 1))
    markers = sorted(media.markers, key=lambda x: x.time)
    assert markers == [
        Marker(time=FrameStamp(60, simple_video.edit_rate),
               name='media-marker-1'),
        Marker(time=FrameStamp(120, simple_video.edit_rate),
               name='media-marker-2'),
    ]
    

def test_second_media_markers_are_empty(simple_video):
    track = next(islice(simple_video.timeline.tracks, 1))
    media = next(islice(track.medias, 1, 2))
    markers = list(media.markers)
    assert markers == []


def test_timeline_markers(simple_video):
    markers = sorted(simple_video.timeline.markers, key=lambda x: x.time)
    assert markers == [
        Marker(time=FrameStamp(150, simple_video.edit_rate), name='marker-1'),
        Marker(time=FrameStamp(300, simple_video.edit_rate), name='marker-2'),
        Marker(time=FrameStamp(450, simple_video.edit_rate), name='marker-3'),
        Marker(time=FrameStamp(600, simple_video.edit_rate), name='marker-4'),
        Marker(time=FrameStamp(750, simple_video.edit_rate), name='marker-5'),
        Marker(time=FrameStamp(900, simple_video.edit_rate), name='marker-6'),
    ]
