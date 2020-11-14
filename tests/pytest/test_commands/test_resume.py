from unittest.mock import Mock
from handlers.commands.resume import start_resume


def test_start_resume(mocker):
    mocked_admin = mocker.patch('handlers.decorators.is_admin')

    client = Mock()
    poll = Mock()
    request_form = Mock()

    mocked_admin.return_value = True
    # Test message value
    poll.storage.check_for_unfinished_poll.return_value = {
        'messages': [{
            'songs': [] 
        }]
    }
    start_resume(client, poll, request_form)