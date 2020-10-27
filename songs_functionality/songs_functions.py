from os import system

from storage.storage import AbstractPollStorage


def download_song(title: str, link: str, path: str) -> None:
    system(f'wget -O {path}/{title}.mp3 "{link}"')

def delete_songs(path: str) -> None:
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
    Sort all_songs all_songs.
    Use bubble sort.
    """
    # Get duplicate of the data
    # not to change the real order of the songs.
    all_songs = all_songs[:] 

    for i in range(len(all_songs)-1):
        for j in range(len(all_songs)-i-1):
            if len(all_songs[j]['voted_users']) < len(all_songs[j+1]['voted_users']):
                all_songs[j], all_songs[j+1] = all_songs[j+1], all_songs[j]

    return all_songs