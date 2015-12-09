import csv
from statistik.models import Song, Chart

with open('assets/chart.csv', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:

        music_id = int(row[1])
        type = int(row[2])
        difficulty = int(row[4])
        note_count = int(row[5])

        print('importing chart %d:%d' % (music_id, type))

        chart = Chart(
            song=Song.objects.get(music_id=music_id),
            type=type,
            difficulty=difficulty,
            note_count=note_count
        )

        chart.save()