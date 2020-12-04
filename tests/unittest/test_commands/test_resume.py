import unittest
from unittest.mock import patch, Mock

from handlers.commands.resume import start_resume


class TestResume(unittest.TestCase):
    """
    Testing command resume.
    """

    @patch('handlers.decorators.is_admin')
    def test_start_resume(self, mock_admin):
        client = Mock()
        poll = Mock()
        request_form = Mock()

        mock_admin.return_value = True
        # Test message value
        poll.storage.check_for_unfinished_poll.return_value = {
            'messages': [{
                'songs': [] 
            }]
        }
        start_resume(client, poll, request_form)