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
        Marker(time=150, end_time=150, value='marker-1', duration=0),
        Marker(time=300, end_time=300, value='marker-2', duration=0),
        Marker(time=450, end_time=450, value='marker-3', duration=0),
        Marker(time=600, end_time=600, value='marker-4', duration=0),
        Marker(time=750, end_time=750, value='marker-5', duration=0),
        Marker(time=900, end_time=900, value='marker-6', duration=0),
    ]




