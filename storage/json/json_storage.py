import csv
import datetime
import glob
import os
import json
import requests

from playhouse.shortcuts import model_to_dict
from typing import List, Union

from storage.storage import AbstractPollStorage
from storage.songs import Song

class JsonPollStorage(AbstractPollStorage):
    """
    Class that represent json file as storage.
    """

    def _get_valid_json_file_name(self) -> str:
        """
        Get valid name based on the current time and date.
        """
        date, time = str(datetime.datetime.now()).split(' ')
        return f'poll-{date}-{time.split(".")[0]}.json'

    def __init__(self, dir_path: str):
        self.data = {
            'is_started': False,
            'is_music_upload': False,
            'messages': [],
        }
        self.file_path = dir_path + self._get_valid_json_file_name()

    def get_all_songs(self) -> List[dict]:
        """
        Method to get list of songs.
        """
        songs = []
        for song in Song.select().order_by(Song.author).execute():
            songs.append(model_to_dict(song))
        return songs
    
    def get_all_messages_id(self) -> List[str]:
        """
        Method that return all the messages ids.
        """
        return [message.message_id for message in Song.select(Song.message_id).group_by(Song.message_id).execute()]

    def get_message_from_song(self, song: dict) -> Union[dict, None]:
        """
        Get message with particular song.
        """
        for message in self.get_all_messages_id():
            if Song.select().where(Song.id_music << [music.id_music for music in Song.select().where(Song.message_id == message).execute()]).count():
                return {
                    "id" : message,
                    "songs" : [model_to_dict(song) for song in Song.select().where(Song.message_id == message).order_by(Song.author).execute()]
                }

    def get_songs_chunk_with_selected_song_id(self, song_id: str) -> List[dict]:
        """
        Get song object form song id.
        """
        messages = self.get_all_messages_id()
        prev_msg = messages[0]
        for next_msg in messages[1:]:
            if Song.get(Song.message_id == prev_msg).id_music < int(song_id) <= Song.get(Song.message_id == next_msg).id_music:
                songs = []
                for song in Song.select().where(Song.message_id == prev_msg).order_by(Song.author).execute():
                    songs.append(model_to_dict(song))
                return songs
            else:
                prev_msg = next_msg
        songs = []
        for song in Song.select().where(Song.message_id == messages[-1]).order_by(Song.author).execute():
            songs.append(model_to_dict(song))
        return songs

    def save(self) -> None:
        with open(self.file_path, 'w') as f:
            f.write(json.dumps(self.data))

    # For unfinished polls
    def drop_all(self, path='storage/json/history/') -> None:
        """
        Drop all json files with is_started=True
        """
        list_of_files = glob.glob(path+'*.json')

        for json_file in list_of_files:
            with open(json_file, 'r+') as f:
                poll_data = json.load(f)
                if poll_data.get('is_started'):
                    poll_data['is_started'] = False
                
                f.seek(0)
                f.truncate()

                f.write(json.dumps(poll_data))

    def check_for_unfinished_poll(self, path='storage/json/history/') -> Union[list, None]:
        """
        Function that check if the user has not finished polls and if True, return the first unfinished.
        """
        list_of_files = glob.glob(path+'*.json')
        
        for poll_file in list_of_files:
            with open(poll_file) as f:
                data = json.load(f)
                if data['is_started']:
                    self.file_path = poll_file
                    return data
