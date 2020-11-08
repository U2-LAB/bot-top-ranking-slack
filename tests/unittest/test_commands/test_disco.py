import unittest
from unittest.mock import patch, Mock

from handlers.commands import disco
from poll import Poll


class TestDisco(unittest.TestCase):
    """
    Testing Disco command.
    """
    def setUp(self):
        self.poll = Mock()
        self.client = Mock()
        self.request_form = {}

        self.poll.is_started = False
        self.poll.storage.data = {}

    def test_parse_disco_args(self):
        self.assertEqual('test.csv', disco.parse_disco_args('test.csv'))
        self.assertEqual('test.csv', disco.parse_disco_args('test test.csv'))
        self.assertEqual('test.csv', disco.parse_disco_args('test.csv test'))
        self.assertEqual(None, disco.parse_disco_args('test.cs'))

    def test_prepare_songs_for_poll_with_30plus_songs(self):
        songs = [1 for i in range(50)]
        self.poll.divide_all_songs_into_chunks.return_value = []
        disco.prepare_songs_for_poll(self.client, self.poll, self.request_form, songs)
        assert self.poll.divide_all_songs_into_chunks.called
    
    def test_prepare_songs_for_poll_with_30less_songs(self):
        songs = []
        self.poll.divide_all_songs_into_chunks.return_value = []
        disco.prepare_songs_for_poll(self.client, self.poll, self.request_form, songs)
        assert not self.poll.divide_all_songs_into_chunks.called

    def test_prepare_songs_for_poll_with(self):
        songs = []
        self.poll.divide_all_songs_into_chunks.return_value = ['test_data']
        self.poll.create_poll_blocks.return_value = []
        disco.prepare_songs_for_poll(self.client, self.poll, self.request_form, songs)
        assert self.poll.create_poll_blocks.called

    @patch('handlers.decorators.is_admin')
    @patch('handlers.commands.disco.send_msg_to_user')
    def test_start_disco_with_unfinished_poll(self, mock_user_msg, mock_admin):
        # Default settings to pass trough decorators.
        mock_admin.return_value = True
        self.poll.storage.check_for_unfinished_poll.return_value = True
        disco.start_disco(self.client, self.poll, self.request_form)
        assert mock_user_msg.called

    @patch('handlers.decorators.is_admin')
    @patch('handlers.commands.disco.send_msg_to_user')
    @patch('handlers.commands.disco.parse_disco_args')
    def test_start_disco_without_csv(self, mock_parse_url, mock_user_msg, mock_admin):
        # Default settings to pass trough decorators.
        mock_admin.return_value = True
        self.poll.storage.check_for_unfinished_poll.return_value = False
        mock_parse_url.return_value = False
        disco.start_disco(self.client, self.poll, self.request_form)
        assert mock_user_msg.called

    @patch('handlers.decorators.is_admin')
    @patch('handlers.commands.disco.send_msg_to_user')
    @patch('handlers.commands.disco.parse_disco_args')
    @patch('handlers.commands.disco.parse_csv_with_songs')
    def test_start_disco_without_songs(self, mock_parse_songs, mock_parse_url, mock_user_msg, mock_admin):
        # Default settings to pass trough decorators.
        mock_admin.return_value = True
        self.poll.storage.check_for_unfinished_poll.return_value = False
        mock_parse_url.return_value = True
        mock_parse_songs.return_value = False
        disco.start_disco(self.client, self.poll, self.request_form)
        assert mock_user_msg.called

    @patch('handlers.decorators.is_admin')
    @patch('handlers.commands.disco.parse_disco_args')
    @patch('handlers.commands.disco.parse_csv_with_songs')
    @patch('handlers.commands.disco.prepare_songs_for_poll')
    def test_start_disco_with_songs(self, mock_prepare_songs, mock_parse_songs, mock_parse_url, mock_admin):
        # Default settings to pass trough decorators.
        mock_admin.return_value = True
        self.poll.storage.check_for_unfinished_poll.return_value = False
        mock_parse_url.return_value = True
        mock_parse_songs.return_value = True
        disco.start_disco(self.client, self.poll, self.request_form)
        assert mock_prepare_songs.called
