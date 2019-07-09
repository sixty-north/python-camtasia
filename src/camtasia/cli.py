from pathlib import Path
import sys

import docopt_subcommands as dsc
from exit_codes import ExitCode, ExitCodeError

from camtasia import use_project


@dsc.command()
def media_bin_ls(_, args):
    """usage: {program} media-bin-ls <project>

    List the contents of the media bin.
    """
    project_dir = args['<project>']
    with use_project(project_dir) as proj:
        for media in proj.media_bin:
            print(f'{media.id} {media.source}')

    return ExitCode.OK


@dsc.command()
def media_bin_rm(_, args):
    """usage: {program} media-bin-rm <project> <media-id>

    Remove a media from the media bin by ID.
    """
    project_dir = args['<project>']

    try:
        media_id = int(args['<media-id>'])
    except ValueError:
        return ExitCode.USAGE

    with use_project(project_dir) as proj:
        proj.media_bin.remove(media_id)

    return ExitCode.OK


@dsc.command()
def media_bin_import(_, args):
    """usage: {program} media-bin-import <project> <media-file>

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
    try:
        return dsc.main('pytsc', argv=argv)
    except ExitCodeError as exc:
        print(str(exc), file=sys.stderr)
        return exc.code


if __name__ == '__main__':
    sys.exit(main())
