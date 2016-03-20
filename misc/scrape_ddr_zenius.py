import json
import re
import requests
from bs4 import BeautifulSoup

TITLES_PAGE = 'https://zenius-i-vanisher.com/v5.2/gamedb.php?gameid=1129'
NOTECOUNTS_PAGE = 'https://zenius-i-vanisher.com/v5.2/gamedb.php?gameid=1129&show_notecounts=1&sort=&sort_order=asc'


def main():
    result_lists = []
    for url in [TITLES_PAGE, NOTECOUNTS_PAGE]:
        resp = requests.get(url)
        soup = BeautifulSoup(resp.content)
        rows = soup.find_all('table')[2].find_all('tr')
        result_lists.append(rows)


    db = []
    version = None


    for rows in zip(*result_lists):
        h_row = [c.text for c in rows[0].find_all('th')]
        if h_row and h_row[0] != 'Song Name':
            version = re.sub('\s*\d+ songs', '', h_row[0])

        else:
            s_row = [c.text for c in rows[0].find_all('td')]
            if s_row:
                if len(s_row) > 12:
                    s_row.pop(2)

                song_name = s_row[0].strip()
                artist = s_row[1].strip()
                [min_bpm, max_bpm] = s_row[2].split('-') if '-' in s_row[2] else [
                    s_row[2], s_row[2]]

                song = {
                    'title': song_name,
                    'artist': artist,
                    'min_bpm': min_bpm,
                    'max_bpm': max_bpm,
                    'version': version,
                    'charts': {}
                }

                chart_infos = [i.text for i in rows[1].find_all('td')[2:11]]
                for idx, chart_info in enumerate(chart_infos):
                    try:
                        level, notecounts = chart_info.split('\n')[:2]
                    except IndexError:
                        pass
                    else:
                        vals = []
                        for i in notecounts.split('/'):
                            try:
                                v = int(i)
                            except ValueError:
                                v = None
                            finally:
                                vals.append(v)

                        if len(vals) == 3:
                            song['charts'][idx] = {
                                'difficulty': int(level),
                                'notes': vals[0],
                                'holds': vals[1],
                                'shock': vals[2]
                            }
                db.append(song)

    with open('ddr.json', 'w') as outfile:
        json.dump(db, outfile, indent=4)



if __name__ == '__main__':
    main()
