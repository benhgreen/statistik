import csv, sys, django, psycopg2

root_directory = str(Path(__file__).resolve().parents[1])
sys.path.append(root_directory)

from statistik.models import Song, Chart

with open('misc/chart.csv', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:

        music_id = int(row[1])
        type = int(row[2])
        difficulty = int(row[4])
        try:
            note_count = int(row[5])
        except ValueError:
            note_count = None


        chart = Chart(
            song=Song.objects.get(music_id=music_id),
            type=type,
            difficulty=difficulty,
            note_count=note_count
        )

        try:
            chart.save()
            print('importing chart %d:%d' % (music_id, type))
        except (psycopg2.IntegrityError, django.db.utils.IntegrityError):
            print('chart %d:%d already in database' % (music_id, type))
            continue
