from unittest.mock import Mock

from handlers.commands.poll_status import start_poll_status


def test_start_poll_status_is_started_is_music_upload(mocker, mocked_started_poll):
    mocked_send_to_usr = mocker.patch('handlers.commands.poll_status.send_msg_to_user')

    start_poll_status(None, mocked_started_poll, None)

    assert mocked_send_to_usr.called

def test_start_poll_status_not_is_started_not_is_music_upload(mocker, mocked_not_started_poll):
    mocked_send_to_usr = mocker.patch('handlers.commands.poll_status.send_msg_to_user')

    start_poll_status(None, mocked_not_started_poll, None)

    assert mocked_send_to_usr.called