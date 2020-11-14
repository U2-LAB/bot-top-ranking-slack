from unittest.mock import Mock

from handlers.commands.settings import get_settings_option_and_option_argument, start_settings


def test_get_settings_option_and_option_argument_with_no_option():
    result = get_settings_option_and_option_argument(None)
    assert result == ('common', [])

def test_get_settings_option_and_option_argument_with_no_args():
    result = get_settings_option_and_option_argument('option')
    assert result == ('option', '')

def test_get_settings_option_and_option_argument_with_args():
    result = get_settings_option_and_option_argument('option arg')
    assert result == ('option', 'arg')

def test_start_settings_common(mocker):
    mocked_admin = mocker.patch('handlers.decorators.is_admin')
    mocked_get_options = mocker.patch('handlers.commands.settings.get_settings_option_and_option_argument')
    mocked_send_to_usr = mocker.patch('handlers.commands.settings.send_msg_to_user')

    mocked_get_options.return_value = ('common', '')

    start_settings(Mock(), Mock(), Mock())
    assert mocked_send_to_usr.called

def test_start_settings_mp3_bad(mocker):
    mocked_admin = mocker.patch('handlers.decorators.is_admin')
    mocked_get_options = mocker.patch('handlers.commands.settings.get_settings_option_and_option_argument')
    mocked_send_to_usr = mocker.patch('handlers.commands.settings.send_msg_to_user')

    mocked_get_options.return_value = ('mp3', '')

    start_settings(Mock(), Mock(), Mock())
    assert mocked_send_to_usr.called

def test_start_settings_mp3_on(mocker):
    mocked_admin = mocker.patch('handlers.decorators.is_admin')
    mocked_get_options = mocker.patch('handlers.commands.settings.get_settings_option_and_option_argument')
    mocked_send_to_usr = mocker.patch('handlers.commands.settings.send_msg_to_user')

    mocked_get_options.return_value = ('mp3', 'on')
    poll = Mock()

    start_settings(Mock(), poll, Mock())
    assert poll.is_music_upload
    assert mocked_send_to_usr.called

def test_start_settings_mp3_off(mocker):
    mocked_admin = mocker.patch('handlers.decorators.is_admin')
    mocked_get_options = mocker.patch('handlers.commands.settings.get_settings_option_and_option_argument')
    mocked_send_to_usr = mocker.patch('handlers.commands.settings.send_msg_to_user')

    mocked_get_options.return_value = ('mp3', 'off')
    poll = Mock()

    start_settings(Mock(), poll, Mock())
    assert not poll.is_music_upload
    assert mocked_send_to_usr.called