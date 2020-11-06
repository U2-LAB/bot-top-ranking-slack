import unittest
from unittest.mock import patch

from chat.users import is_admin

class CustomTestClient:

    def conversations_info(self, channel: str):
        data = {
            'Channel1':{
                'channel': {
                    'creator': 'User1'
            }},
            'Channel2':{
                'channel': {
                    'creator': 'User2'
            }}
        }
        return data.get(channel)


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
