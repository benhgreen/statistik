import json
import sys
import django
import psycopg2
from pathlib import Path

root_directory = str(Path(__file__).resolve().parents[1])
sys.path.append(root_directory)

from statistik.constants import DDR
from statistik.models import Song, Chart


def main():
    with open('misc/ddr.json', 'r') as ddr_file:
        data = json.load(ddr_file)
        for song in data:
            music_id = song['music_id']
            title = song['title']
            artist = song['artist']
            alt_artist = artist
            alt_title = title
            genre = None
            bpm_min = song['bpm_min']
            bpm_max = song['bpm_max']
            game_version = song['game_version']
            game = DDR

            # TODO: have this update it if it already exists
            new_song = Song(
                music_id=music_id,
                bpm_min=bpm_min,
                bpm_max=bpm_max,
                title=title,
                artist=artist,
                alt_artist=alt_artist,
                genre=genre,
                alt_title=alt_title,
                game_version=game_version or music_id // 1000,
                game=game or game_version // 100
            )
            try:
                new_song.save()
                print('Added song %s' % title)
            except (psycopg2.IntegrityError, django.db.utils.IntegrityError) as e:
                # print(e)
                print('%s already in database' % title)
                pass  # might be some new charts

            for chart in song['charts']:
                difficulty = song['charts'][chart]['difficulty']
                note_count = song['charts'][chart]['notes']
                type = int(chart)

                chart = Chart(
                    song=Song.objects.get(music_id=music_id),
                    type=type + 100,
                    difficulty=difficulty,
                    note_count=note_count
                )

                try:
                    chart.save()
                    print('importing chart %d:%d' % (music_id, type))
                except (psycopg2.IntegrityError, django.db.utils.IntegrityError) as e:
                    # print(e)
                    continue


if __name__ == '__main__':
    main()