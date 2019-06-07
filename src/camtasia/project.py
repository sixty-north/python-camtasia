"""The Project class and related details.
"""

from typing import Iterable
import json
from pathlib import Path

from camtasia.authoring_client import AuthoringClient
from camtasia.frame_stamp import FrameStamp
from camtasia.marker import Marker


class Project:
    """The main entry-point for interacting with Camtasia projects.

    Args:
        file_path: Path to the Camtasia project (i.e. a cmproj directory). May be relative or absolute.
    """

    def __init__(self, file_path):
        self._file_path = Path(file_path).resolve()
        with (file_path / 'project.tscproj').open(mode='rt') as handle:
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
    def markers(self) -> Iterable[Marker]:
        for frame in self._data['timeline']['parameters']['toc']['keyframes']:
            yield Marker(name=frame['value'], time=FrameStamp(frame_number=frame['time'], frame_rate=self.edit_rate))
