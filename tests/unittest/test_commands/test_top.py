import unittest
from unittest.mock import patch, Mock

from handlers.commands.top import check_top_arguments, create_final_top_msg, start_top, DEFAULT_VALUE_ERROR_VALUE


class TestTop(unittest.TestCase):
    """
    Testing command top.
    """

    def test_check_top_arguments_with_bad_args(self):
        poll = Mock()
        request_form = {
            'text': 'not int'
        }

        result = check_top_arguments(poll, request_form)
        self.assertEqual(DEFAULT_VALUE_ERROR_VALUE, result)

    def test_check_top_arguments_with_bad_arg_value(self):
        poll = Mock()
        poll.number_of_songs = 4
        
        # With value > poll.number_of_songs
        request_form = {
            'text': '5'
        }

        result = check_top_arguments(poll, request_form)
        self.assertEqual(DEFAULT_VALUE_ERROR_VALUE, result)

        # With value < 0
        request_form = {
            'text': '-1'
        }

        result = check_top_arguments(poll, request_form)
        self.assertEqual(DEFAULT_VALUE_ERROR_VALUE, result)

    def test_check_top_arguments(self):
        poll = Mock()
        poll.number_of_songs = 5
        
        request_form = {
            'text': '4'
        }

        result = check_top_arguments(poll, request_form)
        self.assertEqual(4, result)

    def test_create_final_top_msg(self):
        test_top_songs = [{
            'title': 'TestTitle',
            'artist': 'TestArtist',
            'link': None,
            'voted_users': []
        }]
        result = create_final_top_msg(test_top_songs)
        self.assertEqual(result, 'TOP 1 songs\nTestArtist - TestTitle ---- 0\n')

    @patch('handlers.decorators.is_admin')
    @patch('handlers.commands.top.check_top_arguments')
    @patch('handlers.commands.top.sort_songs')
    @patch('handlers.commands.top.create_final_top_msg')
    @patch('handlers.commands.top.send_msg_to_user')
    def test_start_top(self, mock_send_msg, mock_create_msg, mock_sort, mock_check_args, mock_admin):
        client = Mock()
        poll = Mock()
        request_form = Mock()

        mock_admin.return_value = True
        mock_check_args.return_value = 1
        mock_sort.return_value = ['TestValue']
        mock_create_msg.return_value = 'TestValue'

        start_top(client, poll, request_form)
        assert mock_send_msg.called