from django.test import TestCase
from statistik.models import Song

SAMPLE_SONG_DATA = [{
    'music_id': 1,
    'title': 'Boys Like You',
    'artist': 'Who Is Fancy',
    'genre': 'Pop',
    'bpm_min': 120,
    'bpm_max': 120,
    'game_version': 1
}, {
    'music_id': 2,
    'title': 'Gangster Trippin',
    'artist': 'Fatboy Slim',
    'genre': 'Pop',
    'bpm_min': 120,
    'bpm_max': 120,
    'game_version': 1
}]


def create_some_songs():
    return [Song.objects.create(**song_data) for song_data in SAMPLE_SONG_DATA]


class SongTests(TestCase):
    def setUp(self):
        self.songs = create_some_songs()