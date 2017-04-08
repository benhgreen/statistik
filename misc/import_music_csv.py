import csv

import django
import psycopg2
from django.conf import settings
from statistik.models import Song


with open('music.csv', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    songs = []
    for row in reader:
        is_black_another = False


        music_id=int(row[0])
        bpm_min=int(row[2])
        bpm_max=int(row[3])
        artist=row[5]
        genre=row[6]
        alt_artist = row[8]

        if int(row[1]) >= 917505 or music_id > 21216:
            title = row[4]
            alt_title = row[7]
        else:
            title = row[7]
            alt_title = row[4]

        if title not in songs:
            game_version = None
            songs.append(title)
        # TODO: remove this after using it, it's just for avoiding copula duplicates
        else:
            continue
        # else:
        #     game_version = Song.objects.get(title=title).game_version
        #     print('creating black another for song %s' % title)
        #     title += '†'
        #     alt_title += '†'



        new_song = Song(
            music_id=music_id,
            bpm_min=bpm_min,
            bpm_max=bpm_max,
            title=title,
            artist=artist,
            alt_artist=alt_artist,
            genre=genre,
            alt_title=alt_title,
            game_version=game_version or music_id//1000
        )
        try:
            new_song.save()
            print('Added song %s' % title)
        except (psycopg2.IntegrityError, django.db.utils.IntegrityError):
            print('%s already in database' % title)
            continue
