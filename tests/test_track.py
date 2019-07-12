from pathlib import Path

import pytest

from camtasia.project import Project


class TestTrack:
    def test_track_name(self, project):
        project.timeline.tracks.insert_track(2, 'test-track')
        track = project.timeline.tracks[2]
        assert track.name == 'test-track'

    def test_track_index(self, project):
        project.timeline.tracks.insert_track(2, 'test-track')
        track = project.timeline.tracks[2]
        assert track.index == 2

    def test_track_audio_muted(self, project):
        project.timeline.tracks.insert_track(2, 'test-track')
        track = project.timeline.tracks[2]
        assert track.audio_muted == False

    def test_track_video_hidden(self, project):
        project.timeline.tracks.insert_track(2, 'test-track')
        track = project.timeline.tracks[2]
        assert track.video_hidden == False

    def test_initially_has_no_medias(self, project):
        project.timeline.tracks.insert_track(2, 'test-track')
        track = project.timeline.tracks[2]
        assert len(track.medias) == 0


class TestTrackMedia:
    def test_initially_has_no_markers(self, project: Project, media_root: Path):
        media_path = media_root / 'llama.jpg'
        bin_media = project.media_bin.import_media(media_path)
        track = project.timeline.tracks.insert_track(2, 'test-track')
        media = track.medias.add_media(bin_media, 0)
        assert len(list(media.markers)) == 0

    def test_adding_media_increases_length(self, project: Project, media_root: Path):
        media_path = media_root / 'llama.jpg'
        bin_media = project.media_bin.import_media(media_path)
        track = project.timeline.tracks.insert_track(2, 'test-track')
        track.medias.add_media(bin_media, 0)
        assert len(track.medias) == 1

    def test_iteration(self, project: Project, media_root: Path):
        media_path = media_root / 'llama.jpg'
        bin_media = project.media_bin.import_media(media_path)
        track = project.timeline.tracks.insert_track(2, 'test-track')
        track.medias.add_media(bin_media, 0)
        media = list(track.medias)
        assert len(media) == 1

    def test_get_media_by_id(self, project: Project, media_root: Path):
        media_path = media_root / 'llama.jpg'
        bin_media = project.media_bin.import_media(media_path)
        track = project.timeline.tracks.insert_track(2, 'test-track')
        media_id = track.medias.add_media(bin_media, 0).id
        media = track.medias[media_id]
        assert media.id == media_id
        assert media.source == bin_media.id

    def test_add_overlapping_media_raises_ValueError(self, project: Project, media_root: Path):
        track = project.timeline.tracks.insert_track(2, 'test-track')

        # Add image at start of track
        track.medias.add_media(
            project.media_bin.import_media(media_root / 'llama.jpg'), 0)

        # Add another image at the same place
        with pytest.raises(ValueError):
            track.medias.add_media(
                project.media_bin.import_media(media_root / 'monkey.jpg'), 0)

    def test_add_non_overlapping_media(self, project: Project, media_root: Path):
        track = project.timeline.tracks.insert_track(2, 'test-track')

        # Add image at start of track
        media1 = track.medias.add_media(
            project.media_bin.import_media(media_root / 'llama.jpg'), 0)

        # Add another image at the same place
        track.medias.add_media(
            project.media_bin.import_media(media_root / 'monkey.jpg'), media1.start + media1.duration)

