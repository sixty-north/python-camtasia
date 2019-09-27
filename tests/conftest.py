import pathlib

import pytest

from camtasia.project import load_project, new_project


@pytest.fixture
def media_root(pytestconfig):
    root = pathlib.Path(str(pytestconfig.rootdir))
    return root / 'tests' / 'resources' / 'media'


@pytest.fixture(scope='session')
def simple_video_path(pytestconfig):
    "Path to simple_video.cmproj."
    root = pathlib.Path(str(pytestconfig.rootdir))
    return root / 'tests' / 'resources' / 'simple-video.cmproj'


@pytest.fixture(scope='session')
def simple_video(simple_video_path):
    "The 'simple-video' Project."
    return load_project(simple_video_path)


@pytest.fixture
def temp_path(tmpdir):
    return pathlib.Path(str(tmpdir))


@pytest.fixture
def project(temp_path):
    proj_path = temp_path / 'project.cmproj'
    new_project(proj_path)
    return load_project(proj_path)
