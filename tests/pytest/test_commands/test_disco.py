from unittest.mock import Mock
from handlers.commands import disco



def test_parse_disco_args():
    assert 'test.csv' == disco.parse_disco_args('test.csv')
    assert 'test.csv' == disco.parse_disco_args('test test.csv')
    assert 'test.csv' == disco.parse_disco_args('test.csv test')
    assert None == disco.parse_disco_args('test.cs')

def test_prepare_songs_for_poll_with_songs(mocked_not_started_poll):
    songs = [1 for i in range(10)]
    mocked_not_started_poll.divide_all_songs_into_chunks.return_value = []
    disco.prepare_songs_for_poll(Mock(), mocked_not_started_poll, {}, songs)
    assert not mocked_not_started_poll.divide_all_songs_into_chunks.called

    songs = [1 for i in range(50)]
    mocked_not_started_poll.divide_all_songs_into_chunks.return_value = []
    disco.prepare_songs_for_poll(Mock(), mocked_not_started_poll, {}, songs)
    assert mocked_not_started_poll.divide_all_songs_into_chunks.called

def test_start_disco(mocker, mocked_not_started_poll):
    mocked_admin = mocker.patch('handlers.decorators.is_admin')
    mocked_send_to_usr = mocker.patch('handlers.commands.disco.send_msg_to_user')

    mocked_admin.return_value = True
    mocked_not_started_poll.storage.check_for_unfinished_poll.return_value = True

    disco.start_disco(Mock(), mocked_not_started_poll, {})
    assert mocked_send_to_usr.called

def test_start_disco_without_csv(mocker, mocked_not_started_poll):
    mocked_admin = mocker.patch('handlers.decorators.is_admin')
    mocked_send_to_usr = mocker.patch('handlers.commands.disco.send_msg_to_user')
    mocked_parse_disco = mocker.patch('handlers.commands.disco.parse_disco_args')

    # Default settings to pass trough decorators.
    mocked_admin.return_value = True
    mocked_not_started_poll.storage.check_for_unfinished_poll.return_value = False
    mocked_parse_disco.return_value = False
    disco.start_disco(Mock(), mocked_not_started_poll, {})
    assert mocked_send_to_usr.called

def test_start_disco_without_songs(mocker, mocked_not_started_poll):
    mocked_admin = mocker.patch('handlers.decorators.is_admin')
    mocked_send_to_usr = mocker.patch('handlers.commands.disco.send_msg_to_user')
    mocked_parse_disco = mocker.patch('handlers.commands.disco.parse_disco_args')
    mocked_parse_csv = mocker.patch('handlers.commands.disco.parse_csv_with_songs')

    # Default settings to pass trough decorators.
    mocked_admin.return_value = True
    mocked_not_started_poll.storage.check_for_unfinished_poll.return_value = False
    mocked_parse_disco.return_value = True
    mocked_parse_csv.return_value = False
    disco.start_disco(Mock(), mocked_not_started_poll, {})
    assert mocked_send_to_usr.called

def test_start_disco_with_songs(mocker, mocked_not_started_poll):
    mocked_admin = mocker.patch('handlers.decorators.is_admin')
    mocked_parse_disco = mocker.patch('handlers.commands.disco.parse_disco_args')
    mocked_parse_csv = mocker.patch('handlers.commands.disco.parse_csv_with_songs')
    mocked_prepare_songs = mocker.patch('handlers.commands.disco.prepare_songs_for_poll')

    # Default settings to pass trough decorators.
    mocked_admin.return_value = True
    mocked_not_started_poll.storage.check_for_unfinished_poll.return_value = False
    mocked_parse_disco.return_value = True
    mocked_parse_csv.return_value = True
    disco.start_disco(Mock(), mocked_not_started_poll, {})
    assert mocked_prepare_songs.called