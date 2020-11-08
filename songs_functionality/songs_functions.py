from chat.messages.chat_msg_functions import send_msg_to_user
from chat.files import upload_file

from os import system
from storage.storage import AbstractPollStorage
from slack import WebClient


def download_song(title: str, link: str, path: str) -> None:
    """
    Function, that downloads song from the web using wget command.
    """
    system(f'wget -O {path}/{title}.mp3 "{link}"')

def delete_songs(path: str) -> None:
    """
    Function, that deletes all teh songs from path dir.
    """
    system(f'rm {path}/*.mp3')

def make_valid_song_name(song: dict) -> str:
    """
    Parse the title of the song and make it valid to store.
    """ 
    song_title = '-'.join([song['artist'], song['title']])
    song_title = song_title.replace(' ', '-')
    return song_title

def sort_songs(all_songs: list) -> list:
    """
    Sort all_songs in desc order, using bubble sort.
    """
    # Get duplicate of the data
    # not to change the real order of the songs.
    all_songs = all_songs[:] 

    for i in range(len(all_songs)-1):
        for j in range(len(all_songs)-i-1):
            if len(all_songs[j]['voted_users']) < len(all_songs[j+1]['voted_users']):
                all_songs[j], all_songs[j+1] = all_songs[j+1], all_songs[j]

    return all_songs

def upload_song(client: WebClient, request_form: dict, song: dict):
    song_title = make_valid_song_name(song)
    try:
        download_song(song_title, song['link'], './media/songs')
        upload_file(client, request_form, './media/songs/{}.mp3'.format(song_title))
        delete_songs('./media/songs')
    except FileNotFoundError:
        send_msg_to_user(client, request_form, f"The error occured during downloading song.\nBut the song is {song['artist']} - {song['title']}")
        