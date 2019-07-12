import pathlib

import pytest

from camtasia.project import load_project


@pytest.fixture(scope='session')
def simple_video_path():
    "Path to simple_video.cmproj."
    root = pathlib.Path(str(pytest.config.rootdir))
    return root / 'tests' / 'resources' / 'simple-video.cmproj'


@pytest.fixture(scope='session')
def simple_video(simple_video_path):
    "The 'simple-video' Project."
    return load_project(simple_video_path)


@pytest.fixture
def temp_path(tmpdir):
    return pathlib.Path(str(tmpdir))
