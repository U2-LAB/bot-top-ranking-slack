import csv
import requests
from bs4 import BeautifulSoup

SONG_COUNT = 25

def get_all_songs() -> list:
    """
    Download random songs from ZAYCEV.NET.
    """
    songs = []

    response = requests.get('https://zaycev.net')
    soup = BeautifulSoup(response.content, 'html.parser')

    all_top_songs = soup.find_all(class_='musicset-track')

    for song_bs in all_top_songs[:SONG_COUNT]:
        # If track is banned on the site, it will be shown in the class of the tag
        if 'track-is-banned' in song_bs.get('class'):  
            continue
        
        song = []
        song.append(song_bs.find(class_='musicset-track__track-name').find('a').text)
        song.append(song_bs.find(class_='musicset-track__artist').find('a').text)
        song.append('https://zaycev.net' + song_bs.find(class_='musicset-track__download-link').get('href'))

        songs.append(song)

    return sorted(songs, key=lambda song: song[1])

def form_csv(songs: list, delimiter=';') -> None:
    """
    Create csv file for tests.
    """
    with open('media/csv/test.csv', 'w') as f:
        writer = csv.writer(f, delimiter=delimiter)

        writer.writerow(['Title', 'Artist', 'Link'])
        for song in songs:
            writer.writerow(song) 


if __name__ == "__main__":
    songs = get_all_songs()
