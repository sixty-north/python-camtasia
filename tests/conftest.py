import pathlib

import pytest

from camtasia.project import Project


@pytest.fixture(scope='session')
def simple_video():
    "The 'simple-video' Project."

    root = pathlib.Path(str(pytest.config.rootdir))
    return Project(root / 'tests' / 'examples' / 'simple-video.cmproj')

