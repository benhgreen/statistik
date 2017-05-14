import json
import re
import requests
from bs4 import BeautifulSoup

TITLES_PAGE = 'https://zenius-i-vanisher.com/v5.2/gamedb.php?gameid=2979'
NOTECOUNTS_PAGE = 'https://zenius-i-vanisher.com/v5.2/gamedb.php?gameid=2979&show_notecounts=1&sort=&sort_order=asc'


def main():
    result_lists = []
    for url in [TITLES_PAGE, NOTECOUNTS_PAGE]:
        resp = requests.get(url)
        soup = BeautifulSoup(resp.content, "html.parser")
        rows = soup.find_all('table')[2].find_all('tr')
        result_lists.append(rows)


    db = []
    game_version = None
    versions = {'DDR 1stMIX': 101,
                'DDR 2ndMIX': 102,
                'DDR 3rdMIX': 103,
                'DDR 4thMIX': 104,
                'DDR 5thMIX': 105,
                'DDRMAX': 106,
                'DDRMAX2': 107,
                'DDR EXTREME': 108,
                'DDR SuperNOVA': 109,
                'DDR SuperNOVA2': 110,
                'DDR X': 111,
                'DDR X2': 112,
                'DDR X3 VS 2ndMIX': 113,
                'DDR 2013': 114,
                'DDR 2014': 115,
                'DDR A': 116}

    id_counter = 0
    for rows in zip(*result_lists):
        h_row = [c.text for c in rows[0].find_all('th')]
        if h_row and h_row[0] != 'Song Name':
            game_version = re.sub('\s*\d+ songs', '', h_row[0])
            id_counter = 0

        else:
            s_row = [c.text for c in rows[0].find_all('td')]
            if s_row:
                if len(s_row) > 12:
                    s_row.pop(2)

                song_name = s_row[0].strip()
                title_cell = rows[0].find_all('td')[0].next.next
                if title_cell.name == 'span':
                    alt_title = title_cell.get('onmouseover', None)
                    if alt_title:
                        alt_title = str(alt_title).replace("this.innerHTML='", '').replace("';", '')
                else:
                    alt_title = song_name
                # TODO: alt artist
                if song_name != alt_title:
                    print(song_name, "|", alt_title)
                else:
                    print(song_name)
                artist = s_row[1].strip()
                [bpm_min, bpm_max] = s_row[2].split('-') if '-' in s_row[2] else [
                    s_row[2], s_row[2]]

                version = versions[game_version]
                music_id = versions[game_version] * 1000 + id_counter

                song = {
                    'game': 1,
                    'music_id': music_id,
                    'title': song_name,
                    'alt_title': alt_title,
                    'artist': artist,
                    'bpm_min': bpm_min,
                    'bpm_max': bpm_max,
                    'game_version': version,
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
                id_counter += 1
                # print(song_name, music_id)

    with open('ddr.json', 'w') as outfile:
        json.dump(db, outfile, indent=4)



if __name__ == '__main__':
    main()
