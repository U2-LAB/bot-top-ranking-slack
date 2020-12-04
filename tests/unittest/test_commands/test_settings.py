import unittest
from unittest.mock import patch, Mock

from handlers.commands.settings import get_settings_option_and_option_argument, start_settings


class TestSettings(unittest.TestCase):
    """
    Testing command settings.
    """

    def test_get_settings_option_and_option_argument_with_no_option(self):
        result = get_settings_option_and_option_argument(None)
        self.assertEqual(result, ('common', []))
    
    def test_get_settings_option_and_option_argument_with_no_args(self):
        result = get_settings_option_and_option_argument('option')
        self.assertEqual(result, ('option', ''))

    def test_get_settings_option_and_option_argument_with_args(self):
        result = get_settings_option_and_option_argument('option arg')
        self.assertEqual(result, ('option', 'arg'))

    @patch('handlers.decorators.is_admin')
    @patch('handlers.commands.settings.get_settings_option_and_option_argument')
    @patch('handlers.commands.settings.send_msg_to_user')
    def test_start_settings_common(self, mock_send_msg, mock_get_option_args, mock_admin):
        client = Mock()
        poll = Mock()
        request_form = Mock()

        mock_get_option_args.return_value = ('common', '')

        start_settings(client, poll, request_form)
        assert mock_send_msg.called

    @patch('handlers.decorators.is_admin')
    @patch('handlers.commands.settings.get_settings_option_and_option_argument')
    @patch('handlers.commands.settings.send_msg_to_user')
    def test_start_settings_mp3_bad(self, mock_send_msg, mock_get_option_args, mock_admin):
        client = Mock()
        poll = Mock()
        request_form = Mock()

        mock_get_option_args.return_value = ('mp3', '')

        start_settings(client, poll, request_form)
        assert mock_send_msg.called

    @patch('handlers.decorators.is_admin')
    @patch('handlers.commands.settings.get_settings_option_and_option_argument')
    @patch('handlers.commands.settings.send_msg_to_user')
    def test_start_settings_mp3_on(self, mock_send_msg, mock_get_option_args, mock_admin):
        client = Mock()
        poll = Mock()
        request_form = Mock()

        mock_get_option_args.return_value = ('mp3', 'on')

        start_settings(client, poll, request_form)
        self.assertTrue(poll.is_music_upload)
        assert mock_send_msg.called

    @patch('handlers.decorators.is_admin')
    @patch('handlers.commands.settings.get_settings_option_and_option_argument')
    @patch('handlers.commands.settings.send_msg_to_user')
    def test_start_settings_mp3_off(self, mock_send_msg, mock_get_option_args, mock_admin):
        client = Mock()
        poll = Mock()
        request_form = Mock()

        mock_get_option_args.return_value = ('mp3', 'off')

        start_settings(client, poll, request_form)
        self.assertFalse(poll.is_music_upload)
        assert mock_send_msg.called