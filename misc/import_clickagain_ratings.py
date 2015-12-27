import csv
from statistik.models import Chart

import django
django.setup()


with open('misc/iidxfm_db.csv') as csvfile:
    reader = csv.reader(csvfile)

    for line in reader:
        if len(line) > 6:
            chart = Chart.objects.filter(song__music_id=int(line[0]), type=int(line[1])-1).first()
            if chart:
                base_difficulty = int(line[4])
                if base_difficulty >= 8:
                    normal = line[5]
                    hard = line[6]
                    if normal != '-1':
                        normal = int(normal) * .1 + float(base_difficulty)
                    else:
                        normal = None
                    if hard != '-1':
                        hard = int(hard) * .1 + float(base_difficulty)
                    else:
                        hard = None
                    if normal and hard:
                        chart.clickagain_nc = normal
                        chart.clickagain_hc = hard
                        chart.save()
                        print('%s[%s] %s:%s' % (chart.song.title, chart.get_type_display(), normal, hard))
