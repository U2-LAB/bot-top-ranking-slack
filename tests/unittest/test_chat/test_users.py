import unittest

from chat.users import is_admin
from tests.common_data import CustomTestClient


class TestUsers(unittest.TestCase):
    """
    Testing Users.
    """

    def test_is_admin(self):
        test_client = CustomTestClient()  
        test_request_form = {
            'user_id': 'User1',
            'channel_id': 'Channel1'
        }
        result = is_admin(test_client, test_request_form)
        self.assertTrue(result)

        test_request_form = {
            'user_id': 'User2',
            'channel_id': 'Channel1'
        }
        result = is_admin(test_client, test_request_form)
        self.assertFalse(result)
