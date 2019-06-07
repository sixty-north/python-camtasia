"""Utilities and helper functions.
"""


def media_markers(project):
    """Get all media markers in a project.

    Args:
        project: The Project to fetch data from.

    Returns: An iterable of `(Marker, Media, Track)` tuples.
    """
    return (
        (marker, media, track)
        for track in project.tracks
        for media in track.medias
        for marker in media.markers
    )
