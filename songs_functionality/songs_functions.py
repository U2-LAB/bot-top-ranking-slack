# Contain functions that I do not know where to place

import json
import random
import requests
from os import system
from bs4 import BeautifulSoup

import json

from storage.storage import AbstractPollStorage


def get_all_songs(number_of_songs: int) -> list:
    """
    Download random songs from ZAYCEV.NET.
    """
    songs = []

    response = requests.get('https://zaycev.net')
    soup = BeautifulSoup(response.content, 'html.parser')

    all_top_songs = soup.find_all(class_='musicset-track__download-link')

    for index, song_a in enumerate(random.sample(all_top_songs, number_of_songs)):        
        song = {}
        song['value'] = index + 1
        song['title'] = song_a.get('title').split(' ', 2)[-1]
        song['link'] = 'https://zaycev.net' + song_a.get('href')
        song['voted_users'] = []

        songs.append(song)

    return songs

def download_song(title: str, link: str, path: str) -> None:
    system(f'wget -O {path}/{title}.mp3 "{link}"')

def delete_songs(path: str) -> None:
    system(f'rm {path}/*.mp3')

def make_valid_song_name(song: str) -> str:
    """
    Parse the title of the song and make it valid to store.
    """
    song_title = ''
    for symbol in song['title']:
        if symbol not in (' ', '(', ')', '.', ','):
            song_title += symbol
    return song_title