import csv
import requests
from bs4 import BeautifulSoup


def get_all_songs() -> list:
    """
    Download random songs from ZAYCEV.NET.
    """
    songs = []

    response = requests.get('https://zaycev.net')
    soup = BeautifulSoup(response.content, 'html.parser')

    all_top_songs = soup.find_all(class_='musicset-track')

    for song_bs in all_top_songs:
        song = []
        song.append(song_bs.find(class_='musicset-track__track-name').find('a').text)
        song.append(song_bs.find(class_='musicset-track__artist').find('a').text)
        song.append('https://zaycev.net' + song_bs.find(class_='musicset-track__download-link').get('href'))

        songs.append(song)

    return songs

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
    form_csv(songs)