"""High-level operations on Camtasia project.

Many parts of the camtasia API are very straightfoward and only involve one part of the project, e.g. listing markers on
a track or removing adding new media to the media bin. Some operations, though, required coordination of several parts
and are thus more complicated. This module provides some of these more complex operations as functions.
"""


def add_media_to_track(proj, track_index, media_id, start):
    """Add a track reference to media-bin media.

    Raises:
        KeyError: Specified track or media can't be found.
    """
    track = proj.timeline.tracks[track_index]
    media = proj.media_bin[media_id]
    track.add_media(media, start)


def remove_media(project, media_id, clear_tracks=False):
    """Remove a piece of media from the media-bin.
    
    By default, this will also remove references to the removed media from tracks.

    Args:
        media_id: The ID of the media bin media to remove.
        clear_tracks: Whether to remove references to the media from tracks.

    Raises:
        KeyError: The project has no media with the specified ID.
        ValueError: `clear_tracks` is False and references to the media is found on one or more tracks.
    """
    # Remove all track-medias referring to the bin media.
    for track in project.timeline.tracks:
        for mid in [track_media.id for track_media in track.medias if track_media.source == media_id]:
            if not clear_tracks:
                raise ValueError('Attempt to remove media from media-bin while references exist on tracks')
            del track.medias[mid]

    del project.media_bin[media_id]

