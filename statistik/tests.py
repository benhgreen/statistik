from django.test import TestCase
from statistik.controller import (get_charts_by_ids, get_charts_by_query,
                                  create_new_user)
from statistik.models import Song, Chart

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

SAMPLE_USER_DATA = [{
    'username': 'ben',
    'password': 'lel',
    'dj_name': 'blarg',
    'playside': 0,
    'best_techniques': [],
    'location': 'USA'
},{
    'username': 'jimwich',
    'password': 'asdfasdf',
    'dj_name': 'fdsaa',
    'playside': 1,
    'best_techniques': [],
    'location': 'USA'
}]


def create_some_songs():
    return [Song.objects.create(**song_data) for song_data in SAMPLE_SONG_DATA]

def create_some_charts(songs):
        return [Chart.objects.create(song=song,
                                     type=0,
                                     difficulty=1,
                                     note_count=0)
                for song in songs]


def create_some_users():
    return [create_new_user(user_data) for user_data in SAMPLE_USER_DATA]


def create_some_reviews(charts, users):
    pass


class SongTests(TestCase):
    def setUp(self):
        self.songs = create_some_songs()
        self.charts = create_some_charts(self.songs)
        self.users = create_some_users()
        self.reviews = create_some_reviews(self.charts, self.users)

    def test_get_charts(self):
        """
        Test filtering charts by id and query
        """
        r = get_charts_by_ids([1, 2])
        self.assertEqual(len(r), 2)

        r = get_charts_by_query(version=1)
        self.assertEqual(len(r), 2)

        r = get_charts_by_query(version=1, difficulty=10)
        self.assertEqual(len(r), 0)

        r = get_charts_by_query(version=1, play_style='DP')
        self.assertEqual(len(r), 0)
