import csv
import datetime
import os
import json
import requests

from storage.storage import AbstractPollStorage


class JsonPollStorage(AbstractPollStorage):
    """
    Class that represent json file as storage.
    """

    def _get_valid_json_file_name(self):
        """
        Get valid name based on the current time and date.
        """
        date, time = str(datetime.datetime.now()).split(' ')
        return f'poll-{date}-{time.split(".")[0]}.json'

    def __init__(self, dir_path: str):
        self.data = {
            'message_id': None,
            'is_started': False,
            'is_music_upload': False,
            'songs': None
        }
        self.file_path = dir_path + self._get_valid_json_file_name()

    def get_message_id(self) -> str:
        """
        Method to get message id.
        """
        return self.data['message_id']

    def get_all_songs(self) -> list:
        """
        Method to get list of songs.
        """
        return self.data['songs']

    def get_selected_song(self, song_id:int) -> dict:
        """
        Method to get selected song.
        """
        for song in self.data['songs']:
            if song['value'] == song_id:
                return song

    def create_storage(self, message_id: str, songs: list):
        """
        Method that will create data and the way to store it.
        """
        self.data = {
            'message_id': message_id,
            'is_started': False,
            'is_music_upload': False,
            'songs': songs
        }
    
    def update_message_id(self, message_id: str):
        """
        Method that will update message id with new one
        """
        self.data['message_id'] = message_id

    def parse_csv_with_songs(self, file_url: str, next_line='\n', delimetr=';') -> list:
        """
        Function that will download csv file with songs.
        """
        response = requests.get(file_url)
        response.encoding = response.apparent_encoding

        header, *rows = response.text.split(next_line)
        
        # Check the right format fo the csv file
        header = header.split(delimetr)
        if not (header[0] == 'Title' and header[1] == 'Artist' and header[2] == 'Link'): 
            return [] 

        parsed_csv_data = []

        for index, row in enumerate(rows, start=1):
            row_as_list = row.split(delimetr)
            song = {
                'value': index,
                'title': row_as_list[0],
                'artist': row_as_list[1],
                'link': row_as_list[2] if row_as_list[2] else None,
                'voted_users': []
            }
            parsed_csv_data.append(song)

        return parsed_csv_data

    def save(self):
        print(self.data)
        with open(self.file_path, 'w') as f:
            f.write(json.dumps(self.data))

    def delete(self):
        pass