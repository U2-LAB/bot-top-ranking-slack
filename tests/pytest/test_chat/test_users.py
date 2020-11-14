from chat.users import is_admin
from tests.common_data import CustomTestClient


def test_is_admin():
    test_client = CustomTestClient()

    test_request_form = {
        'user_id': 'User1',
        'channel_id': 'Channel1'
    }
    result = is_admin(test_client, test_request_form)
    assert result

    test_request_form = {
        'user_id': 'User2',
        'channel_id': 'Channel1'
    }
    result = is_admin(test_client, test_request_form)
    assert not result