import requests
import unittest
from unittest.mock import patch

import tools.parse_functions as csv_funcs

from tests.common_data import CustomResponse 

good_response_text = "Title;Artist;Link\r\nTitle1;Artist1;Link1\r\nTitle2;Artist2;Link2\r\nTitle3;Artist3;Link3\r\n"
bad_response_text = "Notitle;NotArtist;NotLink\r\nTitle1;Artist1;Link1\r\nTitle2;Artist2;Link2\r\nTitle3;Artist3;Link3\r\n"


class TestParseFunctions(unittest.TestCase):
    """
    Testing csv parse_functions.
    """
    @patch('tools.parse_functions.requests')
    def test_parse_csv_with_songs(self, mocked_requests):  
        mocked_requests.get.return_value = CustomResponse(good_response_text)
        valid_data = [{
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
            },
            {
            'value': 3,
            'title': 'Title3',
            'artist': 'Artist3',
            'link': 'Link3',
            'voted_users': []
        }]
        data = csv_funcs.parse_csv_with_songs('test/path')
        self.assertEqual(valid_data, data)

        # Bad CSV template
        mocked_requests.get.return_value = CustomResponse(bad_response_text)
        data = csv_funcs.parse_csv_with_songs('test/path')
        self.assertEqual([], data)