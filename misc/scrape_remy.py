from bs4 import BeautifulSoup
import urllib.request
import unicodecsv

SITE = 'https://remywiki.com/AC_SINOBUZ'
VERSION = 24

soup = BeautifulSoup(urllib.request.urlopen(SITE), 'html.parser')

tables = soup.find_all('table', {'class': 'wikitable'})

id_counter = 0
with open('new_songs.csv', 'wb') as song_file:
    with open('new_charts.csv', 'wb') as chart_file:
        for table in tables:
            song_writer = unicodecsv.writer(song_file)
            chart_writer = unicodecsv.writer(chart_file)
            for row in table.find_all('tr'):
                cells = row.find_all('td')
                if len(cells) == 11:
                    genre = cells[0].text.strip()
                    title = cells[1].a.text.strip()
                    artist = cells[2].text.strip()
                    min_bpm = cells[3].text.strip()
                    if '-' in min_bpm:
                        bpm = min_bpm.split('-')
                        min_bpm = bpm[0].strip()
                        max_bpm = bpm[1].strip()
                    else:
                        max_bpm = min_bpm.strip()
                    spn = cells[5].text.strip()
                    sph = cells[6].text.strip()
                    spa = cells[7].text.strip()
                    dpn = cells[8].text.strip()
                    dph = cells[9].text.strip()
                    dpa = cells[10].text.strip()
                    song_page = urllib.request.urlopen('https://remywiki.com' + cells[1].a['href'])
                    song_soup = BeautifulSoup(song_page, 'html.parser')
                    song_table = song_soup.find('table', {'class': 'wikitable'})
                    for note_row in song_table.find_all('tr'):
                        note_cells = note_row.find_all('td')
                        if len(note_cells) == 8 and 'Notecounts' in note_cells[0].text:
                            spn_note = note_cells[2].text.split('/')[0].strip()
                            sph_note = note_cells[3].text.split('/')[0].strip()
                            spa_note = note_cells[4].text.split('/')[0].strip()
                            dpn_note = note_cells[5].text.split('/')[0].strip()
                            dph_note = note_cells[6].text.split('/')[0].strip()
                            dpa_note = note_cells[7].text.split('/')[0].strip()
                            break
                    song_id = VERSION * 1000 + id_counter
                    id_counter += 1
                    alt_title = title
                    song_row = [song_id, '4194305', min_bpm, max_bpm, title,
                                artist, genre, alt_title, artist]
                    song_writer.writerow(song_row)
                    for (play_type, level, note_count) in [(0, spn, spn_note),
                                                           (1, sph, sph_note),
                                                           (2, spa, spa_note),
                                                           (3, dpn, dpn_note),
                                                           (4, dph, dph_note),
                                                           (5, dpa, dpa_note)]:
                        if level == '-' or note_count == '-':
                            continue
                        chart_row = ['', song_id, play_type, '', level, note_count]
                        chart_writer.writerow(chart_row)
                    print(title)
