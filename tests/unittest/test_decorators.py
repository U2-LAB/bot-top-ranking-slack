import unittest
from unittest.mock import patch, MagicMock

from handlers.decorators import only_admin, poll_is_started, poll_not_started

class TestDecorators(unittest.TestCase):
    """
    Testing custom decorators.
    """
    def setUp(self):
        self.mock = MagicMock()

    @patch('handlers.decorators.is_admin')
    @patch('handlers.decorators.send_msg_to_user')
    def test_only_admin(self, mock_user_msg, mock_admin):
        mock_admin.return_value = True
        only_admin(self.mock)(None, None, None)
        assert not mock_user_msg.called

        mock_admin.return_value = False
        only_admin(self.mock)(None, None, None)
        assert mock_user_msg.called

    @patch('handlers.decorators.send_msg_to_user')
    def test_poll_not_started(self, mock_user_msg):
        poll = MagicMock()

        poll.is_started = False
        poll_not_started(self.mock)(None, poll, None)
        assert not mock_user_msg.called

        poll.is_started = True
        poll_not_started(self.mock)(None, poll, None)
        assert mock_user_msg.called

    @patch('handlers.decorators.send_msg_to_user')
    def test_poll_is_started(self, mock_user_msg):
        poll = MagicMock()

        poll.is_started = True
        poll_is_started(self.mock)(None, poll, None)
        assert not mock_user_msg.called

        poll.is_started = False
        poll_is_started(self.mock)(None, poll, None)
        assert mock_user_msg.called
