import json

import unittest
from unittest.mock import patch, mock_open

from storage.json.json_storage import JsonPollStorage


class TestJsonPollStorage(unittest.TestCase):
    """
    Testing of JsonPollStorage.
    """

    def setUp(self):
        self.storage = JsonPollStorage('')
        self.storage.data['messages'] = [{
            'id': 1,
            'songs': [{
                'value': 1,
                'title': 'Title1',
                'artist': 'Artist1',
                'link': 'Link1'
            },
            {
                'value': 2,
                'title': 'Title2',
                'artist': 'Artist2',
                'link': 'Link2'
            }]
            },
            {
            'id': 2,
            'songs': [{
                'value': 3,
                'title': 'Title3',
                'artist': 'Artist3',
                'link': 'Link3'
            },
            {
                'value': 4,
                'title': 'Title4',
                'artist': 'Artist4',
                'link': 'Link4'
            }] 
            },
            {
            'id': 3,
            'songs': [{
                'value': 5,
                'title': 'Title5',
                'artist': 'Artist5',
                'link': 'Link5'
            },
            {
                'value': 6,
                'title': 'Title6',
                'artist': 'Artist6',
                'link': 'Link6'
            }]
        }]

    def test_get_all_songs(self):
        self.assertEqual(6, len(self.storage.get_all_songs()))
        
    def test_get_all_messages_id(self):
        self.assertEqual(3, len(self.storage.get_all_messages_id()))

    def test_get_message_from_song(self):
        song_in_messages = {
            'value': 2,
            'title': 'Title2',
            'artist': 'Artist2',
            'link': 'Link2'
        }
        right_message = {
            'id': 1,
            'songs': [{
                'value': 1,
                'title': 'Title1',
                'artist': 'Artist1',
                'link': 'Link1'
            },
            {
                'value': 2,
                'title': 'Title2',
                'artist': 'Artist2',
                'link': 'Link2'
            }]
        }

        self.assertEqual(right_message, self.storage.get_message_from_song(song_in_messages))

    def test_get_songs_chunk_with_selected_song_id(self):
        song_id = '3'
        right_chunk = [{
            'value': 3,
            'title': 'Title3',
            'artist': 'Artist3',
            'link': 'Link3'
            },
            {
            'value': 4,
            'title': 'Title4',
            'artist': 'Artist4',
            'link': 'Link4'
        }]
        self.assertEqual(right_chunk, self.storage.get_songs_chunk_with_selected_song_id(song_id))

        # Test last chunk
        song_id = '6'
        right_chunk = [{
                'value': 5,
                'title': 'Title5',
                'artist': 'Artist5',
                'link': 'Link5'
            },
            {
                'value': 6,
                'title': 'Title6',
                'artist': 'Artist6',
                'link': 'Link6'
        }]
        self.assertEqual(right_chunk, self.storage.get_songs_chunk_with_selected_song_id(song_id))

    def test_save(self):
        with patch('builtins.open', mock_open()) as mocked_open:
            self.storage.save()
            mocked_open.assert_called_once_with(self.storage.file_path, 'w')
            handler = mocked_open()
            handler.write.assert_called_once_with(json.dumps(self.storage.data))

    @patch('storage.json.json_storage.glob')
    @patch('storage.json.json_storage.json')
    def test_drop_all(self, mocked_json, mocked_glob):
        mocked_glob.glob.return_value = ['test.json']
        with patch('builtins.open', mock_open()) as mocked_open:
            mocked_json.load.return_value = {'is_started': True}
            self.storage.drop_all()
            self.assertEqual(mocked_json.load.return_value, {'is_started': False})
            mocked_open().write(json.dumps({'is_started': False}))
    
    @patch('storage.json.json_storage.glob')
    @patch('storage.json.json_storage.json')
    def test_check_for_unfinished_poll(self, mocked_json, mocked_glob):
        mocked_glob.glob.return_value = ['test.json']
        with patch('builtins.open', mock_open()) as mocked_open:
            mocked_json.load.return_value = {'is_started': True}
            result = self.storage.check_for_unfinished_poll()
            self.assertEqual(result, {'is_started': True})

            mocked_json.load.return_value = {'is_started': False}
            result = self.storage.check_for_unfinished_poll()
            self.assertEqual(result, None)
        