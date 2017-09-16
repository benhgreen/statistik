import csv
import django
import sys
from pathlib import Path

root_directory = str(Path(__file__).resolve().parents[1])
sys.path.append(root_directory)

from statistik.models import Chart

django.setup()

with open('misc/iidxfm_db.csv') as csvfile:
    reader = csv.reader(csvfile)

    print("Importing Clickagain Ratings...")
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
                        chart.clickagain_nc = normal - .1
                        chart.clickagain_hc = hard - .1
                        chart.save()
                        print('%s[%s] %s:%s' % (chart.song.title, chart.get_type_display(), normal, hard))
