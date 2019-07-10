from pathlib import Path
import sys

import docopt_subcommands as dsc
from exit_codes import ExitCode, ExitCodeError

from camtasia import new_project, use_project
from camtasia import operations


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
            print(f'{media.id} {media.identity} {media.source}')

    return ExitCode.OK


@dsc.command()
def media_bin_rm(_, args):
    """usage: {program} media-bin-rm [options] <project> <media-id>

    Remove a media from the media bin by ID. 

    By default this will abort if there are track references to the media. Use the --force flag to remove any track
    references as well.

    Options: 
        --force  Remove track references as well.
    """
    project_dir = args['<project>']

    try:
        media_id = int(args['<media-id>'])
    except ValueError:
        return ExitCode.USAGE

    with use_project(project_dir) as proj:
        try:
            operations.remove_media(proj, media_id, clear_tracks=args['--force'])
        except KeyError as exc:
            raise ExitCodeError(str(exc), ExitCode.DATA_ERR)

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
            operations.add_media_to_track(proj, track_index, media_id, start)
        except KeyError as exc:
            raise ExitCodeError(str(exc), ExitCode.DATA_ERR) from exc

    return ExitCode.OK


# TODO: Markers

@dsc.command()
def timeline_markers_ls(_, args):
    """usage: {program} timeline-markers-ls <project>

    List the timeline markers.
    """
 
    project_dir = args['<project>']

    with use_project(project_dir, save_on_exit=False) as proj:
        for marker in proj.timeline.markers:
            print(f'{marker.name} {marker.time.frame_number} {marker.time}')

    return ExitCode.OK


@dsc.command()
def track_markers_ls(_, args):
    """usage: {program} track-markers-ls <project> [<track-index>]

    List all track markers, or just those for a specific track.
    """
    project_dir = args['<project>']
    track_index = None if args['<track-index>'] is None else int(args['<track-index>'])

    with use_project(project_dir, save_on_exit=False) as proj:
        if track_index is None:
            tracks = proj.timeline.tracks
        else:
            tracks = [proj.timeline.tracks[track_index]]

        for track in tracks:
            for media in track.medias:
                for marker in media.markers:
                    print(marker.name, marker.time.frame_number, marker.time)

    return ExitCode.OK


@dsc.command()
def track_media_ls(_, args):
    """usage: {program} track-media-ls <project> [<track-index>]

    List all media on all tracks, or just for a specific track.
    """
    project_dir = args['<project>']
    track_index = None if args['<track-index>'] is None else int(args['<track-index>'])

    with use_project(project_dir, save_on_exit=False) as proj:
        if track_index is None:
            tracks = proj.timeline.tracks
        else:
            tracks = [proj.timeline.tracks[track_index]]

        for track in tracks:
            for media in track.medias:
                source_media = proj.media_bin[media.source]
                print(f'{media.id} {media.start.frame_number} {media.duration.frame_number} {source_media.identity}')

    return ExitCode.OK


def main(argv=None):
    try:
        return dsc.main('pytsc', argv=argv)
    except ExitCodeError as exc:
        print(str(exc), file=sys.stderr)
        return exc.code


if __name__ == '__main__':
    sys.exit(main())
