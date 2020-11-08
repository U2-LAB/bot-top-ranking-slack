import unittest
from unittest.mock import patch, Mock

from handlers.commands.poll_status import start_poll_status


class TestPollStatus(unittest.TestCase):
    """
    Testing command poll_status.
    """

    @patch('handlers.commands.poll_status.send_msg_to_user')
    def test_start_poll_status_is_started_is_music_upload(self, mocked_user_msg):
        poll = Mock()

        poll.is_started = True
        poll.is_music_upload = True

        start_poll_status(None, poll, None)
        assert mocked_user_msg.called

    @patch('handlers.commands.poll_status.send_msg_to_user')
    def test_start_poll_status_not_is_started_not_is_music_upload(self, mocked_user_msg):
        poll = Mock()

        poll.is_started = False
        poll.is_music_upload = False

        start_poll_status(None, poll, None)
        assert mocked_user_msg.called