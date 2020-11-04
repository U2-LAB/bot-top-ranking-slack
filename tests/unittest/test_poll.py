import unittest
from unittest.mock import patch

from poll import Poll


class TestPoll(unittest.TestCase):
    """
    Testing Poll.
    """
    def setUp(self):
        self.poll = Poll()
        
    def test_get_is_started(self):
        self.poll.storage.data = {
            'is_started': True
        }
        self.assertTrue(self.poll.is_started)

    def test_set_is_started(self):
        self.poll.is_started = False
        self.assertFalse(self.poll.is_started)
    
        with self.assertRaises(TypeError):
            self.poll.is_started = 5

    def test_get_is_music_upload(self):
        self.poll.storage.data = {
            'is_music_upload': True
        }
        self.assertTrue(self.poll.is_music_upload)

    def test_set_is_music_upload(self):
        self.poll.is_music_upload = False
        self.assertFalse(self.poll.is_music_upload)
    
        with self.assertRaises(TypeError):
            self.poll.is_music_upload = 5

    @patch('poll.JsonPollStorage.get_all_songs')
    def test_update_votes(self, mock_func):
        mock_func.return_value = [{
                'value': 1,
                'title': 'Title1',
                'artist': 'Artist1',
                'link': 'Link1',
                'voted_users': []
            },
            {
                'value': 2,
                'title': 'Title2',
                'artist': 'Artist2',
                'link': 'Link2',
                'voted_users': []
        }]

        add_user_result = [{
                'value': 1,
                'title': 'Title1',
                'artist': 'Artist1',
                'link': 'Link1',
                'voted_users': ['User1']
            },
            {
                'value': 2,
                'title': 'Title2',
                'artist': 'Artist2',
                'link': 'Link2',
                'voted_users': []
        }]

        remove_user_result = [{
                'value': 1,
                'title': 'Title1',
                'artist': 'Artist1',
                'link': 'Link1',
                'voted_users': []
            },
            {
                'value': 2,
                'title': 'Title2',
                'artist': 'Artist2',
                'link': 'Link2',
                'voted_users': []
        }]

        self.poll.update_votes('User1','1')
        self.assertEqual(mock_func.return_value, add_user_result)

        self.poll.update_votes('User1','1')
        self.assertEqual(mock_func.return_value, remove_user_result)

    def test_divide_all_songs_into_chunks(self):
        start_list = [[1,2,3,4,5,6]]
        good_result = [[1,2], [3,4], [5,6]]

        result = self.poll.divide_all_songs_into_chunks(start_list, 2)
        self.assertEqual(result, good_result)

        start_list = [[1,2,3,4,5]]
        good_result = [[1,2], [3,4], [5]]

        result = self.poll.divide_all_songs_into_chunks(start_list, 2)
        self.assertEqual(result, good_result)

    def test_create_poll_block(self):
        good_value_1 = [
            {
                'value': 1,
                'title': 'Title1',
                'artist': 'Artist1',
                'link': 'Link1',
                'voted_users': []
            },
            {
                'value': 2,
                'title': 'Title2',
                'artist': 'Artist2',
                'link': 'Link2',
                'voted_users': [1]
            }
        ]
        good_result_1 = [{
            "type": "section",
            "text": {
                "type": "plain_text",
                "text": "#"
            } 
            },
            {
            "type": "section",
            "text": {
                "type": "plain_text",
                "text": "1) Artist1 - Title1 ----- 0 votes"
            },
            'accessory': {
                'type': 'button',
                'text': {
                    'type': 'plain_text',
                    'text': 'Vote/Unvote'
                },
                'value': '1'
            }
            },
            {
            "type": "section",
            "text": {
                "type": "plain_text",
                "text": "2) Artist2 - Title2 ----- 1 votes"
            },
            'accessory': {
                'type': 'button',
                'text': {
                    'type': 'plain_text',
                    'text': 'Vote/Unvote'
                },
                'value': '2'
            }
        }]

        # Check different indexes
        good_value_2 = [
            {
                'value': 10,
                'title': 'Title10',
                'artist': 'Artist10',
                'link': 'Link10',
                'voted_users': []
            },
            {
                'value': 11,
                'title': 'Title11',
                'artist': 'Artist11',
                'link': 'Link11',
                'voted_users': []
            }
        ]
        good_result_2 = [{
            "type": "section",
            "text": {
                "type": "plain_text",
                "text": "#"
            } 
            },
            {
            "type": "section",
            "text": {
                "type": "plain_text",
                "text": "10) Artist10 - Title10 ----- 0 votes"
            },
            'accessory': {
                'type': 'button',
                'text': {
                    'type': 'plain_text',
                    'text': 'Vote/Unvote'
                },
                'value': '10'
            }
            },
            {
            "type": "section",
            "text": {
                "type": "plain_text",
                "text": "11) Artist11 - Title11 ----- 0 votes"
            },
            'accessory': {
                'type': 'button',
                'text': {
                    'type': 'plain_text',
                    'text': 'Vote/Unvote'
                },
                'value': '11'
            }
        }]

        self.assertEqual(good_result_1, self.poll.create_poll_blocks(good_value_1))
        self.assertEqual(good_result_2, self.poll.create_poll_blocks(good_value_2))

    @patch('poll.JsonPollStorage.get_all_songs')
    def test_find_winner_song(self, mock_func):
        mock_func.return_value = [{
                'value': 1,
                'title': 'Title1',
                'artist': 'Artist1',
                'link': 'Link1',
                'voted_users': []
            },
            {
                'value': 2,
                'title': 'Title2',
                'artist': 'Artist2',
                'link': 'Link2',
                'voted_users': [1, 2, 3] # Winner
            },
            {
                'value': 3,
                'title': 'Title3',
                'artist': 'Artist3',
                'link': 'Link3',
                'voted_users': []
        }]

        correct_winner = {
            'value': 2,
            'title': 'Title2',
            'artist': 'Artist2',
            'link': 'Link2',
            'voted_users': [1, 2, 3]
        }

        winner = self.poll.find_the_winner_song()
        self.assertEqual(correct_winner, winner)