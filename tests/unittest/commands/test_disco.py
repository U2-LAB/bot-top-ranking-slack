import unittest
from unittest.mock import patch

from handlers.commands import disco
from poll import Poll


class TestDisco(unittest.TestCase):
    """
    Testing Disco command.
    """

    def setUp(self):
        self.poll = Poll()
    
    def test_parse_disco_args(self):
        self.assertEqual('test.csv', disco.parse_disco_args('test.csv'))
        self.assertEqual('test.csv', disco.parse_disco_args('test test.csv'))
        self.assertEqual('test.csv', disco.parse_disco_args('test.csv test'))
        self.assertEqual(None, disco.parse_disco_args('test.cs'))

    @patch('handlers.commands.disco.is_admin')
    @patch('handlers.commands.disco.send_msg_to_user')
    def test_start_disco_not_admin(self, mocked_send_msg_func, mocked_is_admin):
        mocked_is_admin.return_value = False
        disco.start_disco(None, None, None)
        mocked_send_msg_func.assert_called_once()

    @patch('handlers.commands.disco.is_admin')
    @patch('handlers.commands.disco.send_msg_to_user')
    def test_start_disco_poll_is_started(self, mocked_send_msg_func, mocked_is_admin):
        mocked_is_admin.return_value = True
        self.poll.is_started = True
        disco.start_disco(None, self.poll, None)
        mocked_send_msg_func.assert_called_once()

    @patch('handlers.commands.disco.is_admin')
    @patch('handlers.commands.disco.send_msg_to_user')
    def test_start_disco_with_unfinished_polls(self, mocked_send_msg_func, mocked_is_admin):
        mocked_is_admin.return_value = True
        self.poll.storage.check_for_unfinished_poll = lambda: True
        disco.start_disco(None, self.poll, None)
        mocked_send_msg_func.assert_called_once()

    @patch('handlers.commands.disco.is_admin')
    @patch('handlers.commands.disco.send_msg_to_user')
    @patch('handlers.commands.disco.parse_disco_args')
    def test_start_disco_without_csv(self, mocked_parse_disco_args, mocked_send_msg_func, mocked_is_admin):
        mocked_is_admin.return_value = True
        self.poll.storage.check_for_unfinished_poll = lambda: False
        mocked_parse_disco_args.return_value = None
        disco.start_disco(None, self.poll, {'text': 'csv arg'})
        mocked_send_msg_func.assert_called_once()

    @patch('handlers.commands.disco.is_admin')
    @patch('handlers.commands.disco.send_msg_to_user')
    @patch('handlers.commands.disco.parse_disco_args')
    @patch('handlers.commands.disco.parse_csv_with_songs')
    @patch('handlers.commands.disco.upload_file_to_user')
    def test_start_disco_without_songs(self, mocked_upload_file, mocked_parse_csv_with_songs, mocked_parse_disco_args, mocked_send_msg_func, mocked_is_admin):
        mocked_is_admin.return_value = True
        self.poll.storage.check_for_unfinished_poll = lambda: False
        mocked_parse_disco_args.return_value = True
        mocked_parse_csv_with_songs.return_value = None
        disco.start_disco(None, self.poll, {'text': 'csv arg'})
        mocked_send_msg_func.assert_called_once()
        mocked_upload_file.assert_called_once()

    @patch('handlers.commands.disco.is_admin')
    @patch('handlers.commands.disco.send_msg_to_user')
    @patch('handlers.commands.disco.parse_disco_args')
    @patch('handlers.commands.disco.parse_csv_with_songs')
    @patch('handlers.commands.disco.prepare_songs_for_poll')
    def test_start_disco_with_songs(self, mocked_prepare_songs, mocked_parse_csv_with_songs, mocked_parse_disco_args, mocked_send_msg_func, mocked_is_admin):
        mocked_is_admin.return_value = True
        self.poll.storage.check_for_unfinished_poll = lambda: False
        mocked_parse_disco_args.return_value = True
        mocked_parse_csv_with_songs.return_value = True
        disco.start_disco(None, self.poll, {'text': 'csv arg'})
        mocked_prepare_songs.assert_called_once()

    @patch('handlers.commands.disco.Poll.divide_all_songs_into_chunks')
    @patch('handlers.commands.disco.send_msg_to_chat')
    def test_prepare_songs_for_poll_gt30_songs(self, mocked_send_func, mocked_func):
        songs = [i for i in range(50)]
        self.poll.storage.save = lambda: None
        disco.prepare_songs_for_poll(None, self.poll, None, songs)
        mocked_func.assert_called_once()
        mocked_send_func.assert_called_once()
