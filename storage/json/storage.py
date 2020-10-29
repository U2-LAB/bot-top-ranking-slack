import csv
import datetime
import glob
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
        self.data = {}
        self.file_path = dir_path + self._get_valid_json_file_name()

    def create_storage(self, messages: list) -> None:
        """
        Method that will create data and the way to store it.
        """
        self.data = {
            'is_started': False,
            'is_music_upload': False,
            'messages': messages,
        }

    def get_all_songs(self) -> list:
        """
        Method to get list of songs.
        """
        all_songs = []
        for message in self.data.get('messages'):
            all_songs.extend(message.get('songs')) 
        return all_songs
    
    def get_all_messages_id(self) -> list:
        """
        Method that return all the messages ids.
        """
        return [message.get('id') for message in self.data.get('messages')]

    def get_message_from_song(self, song: dict) -> dict:
        """
        Get message with particular song.
        """
        for message in self.data.get('messages'):
            if song in message.get('songs'):
                return message

    def get_songs_chunk_with_selected_song(self, song_id: str) -> list:
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

    def save(self, is_started: bool, is_music_upload: bool) -> None:

        self.data['is_started'] = is_started
        self.data['is_music_upload'] = is_music_upload

        with open(self.file_path, 'w') as f:
            f.write(json.dumps(self.data))

    # For CSV
    def parse_csv_with_songs(self, file_url: str, next_line='\r\n', delimiter=';') -> list:
        """
        Function that will download csv file with songs.
        """
        response = requests.get(file_url)
        response.encoding = response.apparent_encoding

        header, *rows = response.text.split(next_line)

        # Check the right format fo the csv file
        header = header.split(delimiter)
        if not (header[0] == 'Title' and header[1] == 'Artist' and header[2] == 'Link'): 
            return [] 

        parsed_csv_data = []

        for index, row in enumerate(rows, start=1):
            if not row:
                continue
            
            row_as_list = row.split(delimiter)
            song = {
                'value': index,
                'title': row_as_list[0],
                'artist': row_as_list[1],
                'link': row_as_list[2] if row_as_list[2] else None,
                'voted_users': []
            }
            parsed_csv_data.append(song)

        return parsed_csv_data

    # For unfinished polls
    def drop_all(self) -> None:
        """
        Drop all json files with is_started=True
        """
        list_of_files = glob.glob('storage/json/history/*.json')

        for json_file in list_of_files:
            with open(json_file, 'r+') as f:
                poll_data = json.load(f)
                if poll_data.get('is_started'):
                    poll_data['is_started'] = False
                
                f.seek(0)
                f.truncate()

                f.write(json.dumps(poll_data))

    def check_for_unfinished_poll(self) -> list:
        """
        Function that check if the user has not finished polls and if True, return the first unfinished.
        """
        list_of_files = glob.glob('storage/json/history/*.json')
        
        for poll_file in list_of_files:
            with open(poll_file) as f:
                data = json.load(f)
                if data['is_started']:
                    return data



                