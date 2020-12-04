from unittest.mock import Mock

from handlers.commands.lightsoff import start_lightsoff


def test_start_lightsoff_without_music_upload(mocker, mocked_started_poll):
    mocked_admin = mocker.patch('handlers.decorators.is_admin')
    mocked_send_to_chat = mocker.patch('handlers.commands.lightsoff.send_msg_to_chat')

    mocked_admin.return_value = True
    mocked_started_poll.find_the_winner_song.return_value = {
        'title': 'TestSong',
        'artist': 'TestArtist',
        'voted_users': []
    }
    mocked_started_poll.is_music_upload = False
    mocked_started_poll.storage.get_all_messages_id.return_value = [Mock()]
    
    start_lightsoff(Mock(), mocked_started_poll, {})

    assert mocked_send_to_chat.called

def test_start_lightsoff_with_music_upload(mocker, mocked_started_poll):
    mocked_admin = mocker.patch('handlers.decorators.is_admin')
    mocked_send_to_chat = mocker.patch('handlers.commands.lightsoff.send_msg_to_chat')
    mocked_upload_song = mocker.patch('handlers.commands.lightsoff.upload_song')
    
    mocked_admin.return_value = True
    mocked_started_poll.find_the_winner_song.return_value = {
        'title': 'TestSong',
        'artist': 'TestArtist',
        'voted_users': []
    }
    mocked_started_poll.is_music_upload = True
    mocked_started_poll.storage.get_all_messages_id.return_value = [Mock()]
    
    start_lightsoff(Mock(), mocked_started_poll, {})

    assert mocked_upload_song.called
