from pathlib import Path
import sys

import docopt_subcommands as dsc
from exit_codes import ExitCode, ExitCodeError

from camtasia import new_project, use_project


@dsc.command()
def new_project_handler(_, args):
    """usage: {program} new-project <project>

    Create a new, empty project.
    """
    new_project(args['<project>'])


@dsc.command()
def media_bin_ls(_, args):
    """usage: {program} media-bin-ls <project>

    List the contents of the media bin.
    """
    project_dir = args['<project>']
    with use_project(project_dir, save_on_exit=False) as proj:
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
        del proj.media_bin[media_id]

    return ExitCode.OK


@dsc.command()
def media_bin_import(_, args):
    """usage: {program} media-bin-import <project> <media-file>

    Import media into a project.
    """
    project_dir = args['<project>']
    with use_project(project_dir) as proj:
        try:
            media = proj.media_bin.import_media(Path(args['<media-file>']))
            print(media.id)
        except (OSError, ValueError) as exc:
            raise ExitCodeError(str(exc), ExitCode.OS_ERR) from exc

    return ExitCode.OK


@dsc.command()
def tracks_ls(_, args):
    """usage: {program} tracks-ls <project>

    List the tracks in the timeline.
    """
    project_dir = args['<project>']
    with use_project(project_dir, save_on_exit=False) as proj:
        for track in proj.timeline.tracks:
            print(f'{track.index} name={track.name} muted={track.audio_muted} hidden={track.video_hidden}')

    return ExitCode.OK


@dsc.command()
def track_add_media(_, args):
    """usage: {program} track-add-media <project> <track-index> <media-id> <start>

    Add media from the media-bin to a track.
    """
    project_dir = args['<project>']
    track_index = int(args['<track-index>'])
    media_id = int(args['<media-id>'])
    start = int(args['<start>'])

    with use_project(project_dir) as proj:

        try:
            track = proj.timeline.tracks[track_index]
        except KeyError as exc:
            raise ExitCodeError(f'No track with index {track_index}', ExitCode.DATA_ERR) from exc

        try:
            media = proj.media_bin[media_id]
        except KeyError as exc:
            raise ExitCodeError(f'No media with id {media_id}', ExitCode.DATA_ERR) from exc

        track.add_media(media, start)

    return ExitCode.OK


# TODO: Markers


def main(argv=None):
    try:
        return dsc.main('pytsc', argv=argv)
    except ExitCodeError as exc:
        print(str(exc), file=sys.stderr)
        return exc.code


if __name__ == '__main__':
    sys.exit(main())
