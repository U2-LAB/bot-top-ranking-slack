import unittest
from unittest.mock import patch

import songs_functionality.songs_functions as songs_funcs

class TestSongsFunctions(unittest.TestCase):
    """
    Testing of SongsFunctions.
    """
    @patch('songs_functionality.songs_functions.system')
    def test_download_song(self, mocked_system):
        songs_funcs.download_song('test_song', 'http://test.json', '.')
        mocked_system.assert_called_once_with('wget -O ./test_song.mp3 "http://test.json"')
    
    @patch('songs_functionality.songs_functions.system')
    def test_delete_songs(self, mocked_system):
        songs_funcs.delete_songs('test/path')
        mocked_system.assert_called_once_with('rm test/path/*.mp3')
    
    def test_make_valid_song_name(self):
        song = {
            'title': 'Song about love',
            'artist': 'ArtistName ArtistSurname'
        }

        title = songs_funcs.make_valid_song_name(song)

        self.assertEqual(title, 'ArtistName-ArtistSurname-Song-about-love')

    def test_sort_songs(self):
        all_songs = [
            {
                'value': 1,
                'title': 'Title1',
                'artist': 'Artist1',
                'link': 'Link1',
                'voted_users': [1]
            },
            {
                'value': 2,
                'title': 'Title2',
                'artist': 'Artist2',
                'link': 'Link2',
                'voted_users': []
            },
            {
                'value': 3,
                'title': 'Title3',
                'artist': 'Artist3',
                'link': 'Link3',
                'voted_users': [1,2,3]
            },
            {
                'value': 4,
                'title': 'Title4',
                'artist': 'Artist4',
                'link': 'Link4',
                'voted_users': [1, 2]
            }
        ]

        sorted_songs = [
            {
                'value': 3,
                'title': 'Title3',
                'artist': 'Artist3',
                'link': 'Link3',
                'voted_users': [1,2,3]
            },
            {
                'value': 4,
                'title': 'Title4',
                'artist': 'Artist4',
                'link': 'Link4',
                'voted_users': [1, 2]
            },
            {
                'value': 1,
                'title': 'Title1',
                'artist': 'Artist1',
                'link': 'Link1',
                'voted_users': [1]
            },
            {
                'value': 2,
                'title': 'Title2',
                'artist': 'Artist2',
                'link': 'Link2',
                'voted_users': []
            }
        ]

        self.assertEqual(sorted_songs, songs_funcs.sort_songs(all_songs))