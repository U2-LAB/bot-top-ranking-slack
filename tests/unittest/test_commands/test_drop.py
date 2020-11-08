import unittest
from unittest.mock import patch

from handlers.commands import drop

from poll import Poll


class TestDrop(unittest.TestCase):
    """
    Testing drop command.
    """
    def setUp(self):
        self.poll = Poll()

    @patch('handlers.decorators.is_admin')
    @patch('handlers.commands.drop.send_msg_to_user')
    def test_start_drop_as_admin(self, mocked_send_msg, mocked_admin):
        mocked_admin.return_value = True
        drop.start_drop(None, self.poll, None)
        assert mocked_send_msg.called