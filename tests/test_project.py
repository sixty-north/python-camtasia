def test_authoring_client(simple_video):
    ac = simple_video.authoring_client
    assert ac.name == 'Camtasia'
    assert ac.platform == 'Mac'
    assert ac.version == '2019.0.1'


def test_edit_rate(simple_video):
    assert simple_video.edit_rate == 30
