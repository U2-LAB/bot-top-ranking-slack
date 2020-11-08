import unittest
from unittest.mock import patch, Mock

from handlers.commands.lightsoff import start_lightsoff


class TestLightsoff(unittest.TestCase):
    """
    Testing lightsoff command.
    """
    def setUp(self):
        self.poll = Mock()
        self.client = Mock()
        self.request_form = {}

        self.poll.is_started = True
        self.poll.storage.data = {}

    @patch('handlers.decorators.is_admin')
    @patch('handlers.commands.lightsoff.send_msg_to_chat')
    def test_start_lightsoff_without_music_upload(self, mock_chat_msg, mock_admin):
        mock_admin.return_value = True
        self.poll.find_the_winner_song.return_value = {
            'title': 'TestSong',
            'artist': 'TestArtist',
            'voted_users': []
        }
        self.poll.is_music_upload = False
        self.poll.storage.get_all_messages_id.return_value = [Mock()]
        
        start_lightsoff(self.client, self.poll, self.request_form)

        assert mock_chat_msg.called

    @patch('handlers.decorators.is_admin')
    @patch('handlers.commands.lightsoff.send_msg_to_chat')
    @patch('handlers.commands.lightsoff.upload_song')
    def test_start_lightsoff_with_music_upload(self, mock_upload_song, mock_chat_msg, mock_admin):
        mock_admin.return_value = True
        self.poll.find_the_winner_song.return_value = {
            'title': 'TestSong',
            'artist': 'TestArtist',
            'voted_users': []
        }
        self.poll.is_music_upload = True
        self.poll.storage.get_all_messages_id.return_value = [Mock()]
        
        start_lightsoff(self.client, self.poll, self.request_form)

        assert mock_upload_song.called
