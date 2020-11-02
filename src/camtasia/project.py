"""The Project class and related details.
"""

from contextlib import contextmanager
import json
from pathlib import Path
import pkg_resources
import shutil
import os

from camtasia.authoring_client import AuthoringClient
from camtasia.media_bin import MediaBin
from camtasia.timeline import Timeline


class Project:
    """The main entry-point for interacting with Camtasia projects.

    Args:
        file_path: Path to the Camtasia project (i.e. a cmproj directory). May be relative or absolute.
        encoding: Encoding of the project file.
    """

    def __init__(self, file_path: Path, encoding=None):
        self._file_path = file_path
        self._data = json.loads(self._project_file.read_text(encoding=encoding))
        self._encoding = encoding

    @property
    def file_path(self) -> Path:
        "The full path to the Camtasia project."
        return self._file_path

    def save(self):
        with self._project_file.open(mode='wt', encoding=self._encoding) as handle:
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
        return MediaBin(self._data.setdefault('sourceBin', []), self._file_path)

    @property
    def timeline(self) -> Timeline:
        return Timeline(self._data['timeline'])

    @property
    def _project_file(self):
        "The project's main JSON data file, i.e. the 'tscproj' file."
        if self.file_path.is_dir():
            for file in self.file_path.iterdir():
                if file.is_file() and file.suffix == '.tscproj':
                    return file
            raise FileNotFoundError("No .tscproj file was found in directory")
        else:
            return self.file_path

    def __repr__(self):
        return f'Project(file_path="{self.file_path}")'


def load_project(file_path, encoding=None):
    """Load a Camtasia project at the specific path.

    Args:
        file_path: The path (pathlib.Path or str) to the Camtasia project.
        encoding: Encoding of the project file.

    Return: A new Project instance.
    """
    file_path = Path(file_path).resolve()
    return Project(file_path, encoding=encoding)


@contextmanager
def use_project(file_path, save_on_exit=True, encoding=None):
    """Context manager for working with Projects.

    This loads the project on enter. If the with-block exits normally and `save_on_exit` is true, then this saves the
    project. If it exits exceptionally then edits are discarded.

    Args: 
        file_path: The path (pathlib.Path or str) to the Camtasia project.
        save_on_exit: Whether to save the project on normal exit.
        encoding: Encoding of the project file.

    Yields: A new Project instance.
    """
    proj = load_project(file_path, encoding=encoding)

    yield proj

    if save_on_exit:
        proj.save()


def new_project(file_path):
    """Create a new, empty project at `file_path`.
    """
    project_template_dir = pkg_resources.resource_filename('camtasia', os.path.join('resources', 'new.cmproj'))
    shutil.copytree(project_template_dir, file_path)
    