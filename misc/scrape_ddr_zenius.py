import re
import requests
from django.conf import settings
from bs4 import BeautifulSoup
from statistik.models import Song, Chart

MAIN_SITE = 'https://zenius-i-vanisher.com/v5.2/gamedb.php?gameid=1129'


def main():
    resp = requests.get(MAIN_SITE)
    soup = BeautifulSoup(resp.content)
    rows = soup.find_all('table')[2].find_all('tr')


    for row in rows:
        h_row = [c.text for c in row.find_all('th')]
        if h_row and h_row[0] != 'Song Name':
            version = re.sub('\s*\d+ songs', '', h_row[0])
            print('\n', version, '\n')

        else:
            s_row = [c.text for c in row.find_all('td')]
            if s_row:
                if len(s_row) > 12:
                    s_row.pop(2)

                song_name = s_row[0].strip()
                artist = s_row[1]
                [min_bpm, max_bpm] = s_row[2].split('-') if '-' in s_row[2] else [
                    s_row[2], s_row[2]]

                s = Song.objects.filter(title=song_name).first()
                if s:
                    print('----> ' + song_name)
                else:
                    print(song_name)
                # if not s:
                #     s = Song.objects.create(title=song_name,
                #                             artist=artist,
                #                             bpm_min=min_bpm,
                #                             bpm_max=max_bpm,
                #                             game_version='foo')


if __name__ == '__main__':
    main()
