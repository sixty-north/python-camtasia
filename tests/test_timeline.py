from itertools import islice

from camtasia.timeline.marker import Marker


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
        Marker(time=60, name='media-marker-1'),
        Marker(time=120, name='media-marker-2'),
    ]


def test_second_media_markers_are_empty(simple_video):
    track = next(islice(simple_video.timeline.tracks, 1))
    media = next(islice(track.medias, 1, 2))
    markers = list(media.markers)
    assert markers == []


def test_timeline_markers(simple_video):
    markers = sorted(simple_video.timeline.markers, key=lambda x: x.time)
    assert markers == [
        Marker(time=150, name='marker-1'),
        Marker(time=300, name='marker-2'),
        Marker(time=450, name='marker-3'),
        Marker(time=600, name='marker-4'),
        Marker(time=750, name='marker-5'),
        Marker(time=900, name='marker-6'),
    ]
