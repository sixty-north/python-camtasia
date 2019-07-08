"""The Project class and related details.
"""

import json
from pathlib import Path

from camtasia.authoring_client import AuthoringClient
from camtasia.media_bin import MediaBin
from camtasia.timeline import Timeline


class Project:
    """The main entry-point for interacting with Camtasia projects.

    Args:
        file_path: Path to the Camtasia project (i.e. a cmproj directory). May be relative or absolute.
    """

    def __init__(self, file_path):
        self._file_path = file_path
        self._data = json.loads(self._project_file.read_text())

    @property
    def file_path(self) -> Path:
        "The full path to the Camtasia project."
        return self._file_path

    def save(self):
        with self._project_file.open(mode='wt') as handle:
            json.dump(self._data, handle)

    @property
    def authoring_client(self) -> AuthoringClient:
        "Details about the software used to edit the project."
        return AuthoringClient(**self._data['authoringClientName'])

    @property
    def edit_rate(self) -> int:
        "The editing framerate."
        return self._data['editRate']

    @property
    def media_bin(self) -> MediaBin:
        return MediaBin(self._data['sourceBin'], self._file_path)

    @property
    def timeline(self) -> Timeline:
        return Timeline(self._data['timeline'], self.edit_rate)

    @property
    def _project_file(self):
        "The project's main JSON data file, i.e. the 'tscproj' file."
        return self.file_path / 'project.tscproj'

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
