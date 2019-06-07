"""The Project class and related details.
"""

from typing import Iterable
import json
from pathlib import Path

from camtasia.authoring_client import AuthoringClient
from camtasia.frame_stamp import FrameStamp
from camtasia.marker import Marker
from camtasia.track import Track


class Project:
    """The main entry-point for interacting with Camtasia projects.

    Args:
        file_path: Path to the Camtasia project (i.e. a cmproj directory). May be relative or absolute.
    """

    def __init__(self, file_path):
        self._file_path = file_path
        with (self.file_path / 'project.tscproj').open(mode='rt') as handle:
            self._data = json.load(handle)

    @property
    def file_path(self) -> Path:
        "The full path to the Camtasia project."
        return self._file_path

    @property
    def authoring_client(self) -> AuthoringClient:
        "Details about the software used to edit the project."
        return AuthoringClient(**self._data['authoringClientName'])

    @property
    def edit_rate(self) -> int:
        "The editing framerate."
        return self._data['editRate']

    @property
    def tracks(self) -> Iterable[Track]:
        timeline_data = self._data['timeline']
        for idx, attrs in enumerate(timeline_data['trackAttributes']):
            # As far as I can tell, there's only ever one scene. Hence the 0.
            data = timeline_data['sceneTrack']['scenes'][0]['csml']['tracks'][idx]
            yield Track(attrs, data, self.edit_rate)

    @property
    def timeline_markers(self) -> Iterable[Marker]:
        for frame in self._data['timeline']['parameters']['toc']['keyframes']:
            yield Marker(name=frame['value'], time=FrameStamp(frame_number=frame['time'], frame_rate=self.edit_rate))

    def __repr__(self):
        return f'Project(file_path="{self.file_path}")'


def load_project(file_path):
    """Load a Camtasia project at the specific path.

    Args:
        file_path: The path (pathlib.Path or str) to the Camtasia project.

    Return: A new Project instance.
    """
    file_path = Path(file_path).resolve()
    return Project(file_path)
