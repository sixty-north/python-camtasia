from camtasia.frame_stamp import FrameStamp
from camtasia.project import Marker


def test_authoring_client(simple_video):
    ac = simple_video.authoring_client
    assert ac.name == 'Camtasia'
    assert ac.platform == 'Mac'
    assert ac.version == '2019.0.1'


def test_edit_rate(simple_video):
    assert simple_video.edit_rate == 30


def test_markers(simple_video):
    markers = list(simple_video.markers)
    markers.sort(key=lambda x: x.time)
    assert markers == [
        Marker(time=FrameStamp(150, simple_video.edit_rate), name='marker-1'),
        Marker(time=FrameStamp(300, simple_video.edit_rate), name='marker-2'),
        Marker(time=FrameStamp(450, simple_video.edit_rate), name='marker-3'),
        Marker(time=FrameStamp(600, simple_video.edit_rate), name='marker-4'),
        Marker(time=FrameStamp(750, simple_video.edit_rate), name='marker-5'),
        Marker(time=FrameStamp(900, simple_video.edit_rate), name='marker-6'),
    ]




