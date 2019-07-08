from pathlib import Path
import sys

import docopt_subcommands as dsc
from exit_codes import ExitCode

from camtasia import use_project


@dsc.command()
def list_media_bin(_, args):
    """usage: {program} list-media-bin <project>

    List the contents of the media bin.
    """
    project_dir = args['<project>']
    with use_project(project_dir) as proj:
        for media in proj.media_bin:
            print(f'{media.id} {media.source}')

    return ExitCode.OK


@dsc.command()
def import_media(_, args):
    """usage: {program} import-media <project> <media-file>

    Import media into a project.
    """
    project_dir = args['<project>']
    with use_project(project_dir) as proj:
        try:
            proj.media_bin.import_media(Path(args['<media-file>']))
        except (OSError, ValueError) as exc:
            raise ExitCodeError(str(exc), ExitCode.OS_ERR) from exc

    return ExitCode.OK


def main(argv=None):
    if argv is None:
        argv = sys.argv

    try:
        return dsc.main('pytsc', argv=argv)
    except ExitCodeError as exc:
        print(str(exc), file=sys.stderr)
        return exc.code


class ExitCodeError(Exception):
    def __init__(self, msg, code):
        super().__init__(msg)
        self.code = code

    def __repr__(self):
        return f'ExitCodeError("{self.args[0]}", {self.code})'


if __name__ == '__main__':
    main()
