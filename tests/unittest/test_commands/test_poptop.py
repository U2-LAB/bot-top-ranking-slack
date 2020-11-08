import unittest
from unittest.mock import patch, Mock

from handlers.commands.poptop import check_poptop_argument, start_poptop, DEFAULT_EXCEPTION_VALUE


class TestPoptop(unittest.TestCase):
    """
    Testing command poptop.
    """

    def test_check_poptop_argument_with_bad_argument(self):
        request_form = {
            'text': 'Not int'
        }
        result = check_poptop_argument(None, request_form)
        self.assertEqual(result, DEFAULT_EXCEPTION_VALUE)

    def test_check_poptop_argument_out_of_limit(self):
        request_form = {
            'text': '5'
        }
        poll = Mock()
        poll.number_of_songs = 4

        result = check_poptop_argument(poll, request_form)
        self.assertEqual(result, DEFAULT_EXCEPTION_VALUE)

        request_form = {
            'text': '-1'
        }
        result = check_poptop_argument(poll, request_form)
        self.assertEqual(result, DEFAULT_EXCEPTION_VALUE)

    def test_check_poptop_argument_good(self):
        request_form = {
            'text': '4'
        }
        poll = Mock()
        poll.number_of_songs = 5
        result = check_poptop_argument(poll, request_form)
        self.assertEqual(result, 4)

    @patch('handlers.decorators.is_admin')
    @patch('handlers.commands.poptop.check_poptop_argument')
    @patch('handlers.commands.poptop.sort_songs')
    @patch('handlers.commands.poptop.upload_song')
    def test_start_poptop_with_song_upload(self, mock_upload_song, mock_sort, mock_check_args, mock_admin):
        poll = Mock()
        request_form = Mock()
        client = Mock()

        mock_admin.return_value = True
        poll.is_started = True
        poll.is_music_upload = True

        mock_check_args.return_value = 1
        mock_sort.return_value = [{
            'title': 'TestTitle',
            'artist': 'TestArtist',
            'link': None,
            'voted_users': []
        }]
        
        start_poptop(client, poll, request_form)
        assert mock_upload_song.called

    @patch('handlers.decorators.is_admin')
    @patch('handlers.commands.poptop.check_poptop_argument')
    @patch('handlers.commands.poptop.sort_songs')
    @patch('handlers.commands.poptop.send_msg_to_chat')
    def test_start_poptop_without_song_upload(self, mock_send_msg, mock_sort, mock_check_args, mock_admin):
        poll = Mock()
        request_form = Mock()
        client = Mock()

        mock_admin.return_value = True
        poll.is_started = True
        poll.is_music_upload = False

        mock_check_args.return_value = 1
        mock_sort.return_value = [{
            'title': 'TestTitle',
            'artist': 'TestArtist',
            'link': None,
            'voted_users': []
        }]
        
        start_poptop(client, poll, request_form)
        assert mock_send_msg.called