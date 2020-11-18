import csv
import datetime
import glob
import os
import json
import requests

from typing import List, Union

from storage.storage import AbstractPollStorage


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
        all_songs = []
        for message in self.data.get('messages'):
            all_songs.extend(message.get('songs')) 
        return all_songs
    
    def get_all_messages_id(self) -> List[str]:
        """
        Method that return all the messages ids.
        """
        return [message.get('id') for message in self.data.get('messages')]

    def get_message_from_song(self, song: dict) -> Union[dict, None]:
        """
        Get message with particular song.
        """
        for message in self.data.get('messages'):
            if song in message.get('songs'):
                return message

    def get_songs_chunk_with_selected_song_id(self, song_id: str) -> List[dict]:
        """
        Get song object form song id.
        """
        prev_msg = self.data['messages'][0]
        for next_msg in self.data['messages'][1:]:
            if prev_msg['songs'][0]['value'] <= int(song_id) < next_msg['songs'][0]['value']:
                return prev_msg.get('songs')
            else:
                prev_msg = next_msg
        return self.data['messages'][-1]['songs']

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