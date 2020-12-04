from unittest.mock import Mock
from handlers.commands.poptop import check_poptop_argument, start_poptop, DEFAULT_EXCEPTION_VALUE


def test_check_poptop_argument_with_bad_argument():
    request_form = {
        'text': 'Not int'
    }
    result = check_poptop_argument(None, request_form)
    assert result == DEFAULT_EXCEPTION_VALUE

def test_check_poptop_argument_out_of_limit():
    request_form = {
        'text': '5'
    }
    poll = Mock()
    poll.number_of_songs = 4

    result = check_poptop_argument(poll, request_form)
    assert result == DEFAULT_EXCEPTION_VALUE

    request_form = {
        'text': '-1'
    }
    result = check_poptop_argument(poll, request_form)
    assert result == DEFAULT_EXCEPTION_VALUE

def test_check_poptop_argument_good():
    request_form = {
        'text': '4'
    }
    poll = Mock()
    poll.number_of_songs = 5
    result = check_poptop_argument(poll, request_form)
    assert result == 4

def test_start_poptop_with_song_upload(mocker, mocked_started_poll):
    mocked_admin = mocker.patch('handlers.decorators.is_admin')
    mocked_check_args = mocker.patch('handlers.commands.poptop.check_poptop_argument')
    mocked_sort_songs = mocker.patch('handlers.commands.poptop.sort_songs')
    mocked_upload_songs = mocker.patch('handlers.commands.poptop.upload_song')

    request_form = Mock()
    client = Mock()

    mocked_admin.return_value = True
    mocked_check_args.return_value = 1

    mocked_sort_songs.return_value = [{
        'title': 'TestTitle',
        'artist': 'TestArtist',
        'link': None,
        'voted_users': []
    }]
    
    start_poptop(client, mocked_started_poll, request_form)
    assert mocked_upload_songs.called

def test_start_poptop_without_song_upload(mocker, mocked_started_poll):
    mocked_admin = mocker.patch('handlers.decorators.is_admin')
    mocked_check_args = mocker.patch('handlers.commands.poptop.check_poptop_argument')
    mocked_sort_songs = mocker.patch('handlers.commands.poptop.sort_songs')
    mocked_send_to_chat = mocker.patch('handlers.commands.poptop.send_msg_to_chat')

    request_form = Mock()
    client = Mock()

    mocked_admin.return_value = True
    mocked_started_poll.is_music_upload = False

    mocked_check_args.return_value = 1
    mocked_sort_songs.return_value = [{
        'title': 'TestTitle',
        'artist': 'TestArtist',
        'link': None,
        'voted_users': []
    }]
    
    start_poptop(client, mocked_started_poll, request_form)
    assert mocked_send_to_chat.called