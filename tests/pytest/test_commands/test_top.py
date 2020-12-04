from unittest.mock import Mock

from handlers.commands.top import check_top_arguments, create_final_top_msg, start_top, DEFAULT_VALUE_ERROR_VALUE


def test_check_top_arguments_with_bad_args():
    poll = Mock()
    request_form = {
        'text': 'not int'
    }

    result = check_top_arguments(poll, request_form)
    assert DEFAULT_VALUE_ERROR_VALUE == result

def test_check_top_arguments_with_bad_arg_value():
    poll = Mock()
    poll.number_of_songs = 4
    
    # With value > poll.number_of_songs
    request_form = {
        'text': '5'
    }

    result = check_top_arguments(poll, request_form)
    assert DEFAULT_VALUE_ERROR_VALUE == result

    # With value < 0
    request_form = {
        'text': '-1'
    }

    result = check_top_arguments(poll, request_form)
    assert DEFAULT_VALUE_ERROR_VALUE == result

def test_check_top_arguments():
    poll = Mock()
    poll.number_of_songs = 5
    
    request_form = {
        'text': '4'
    }

    result = check_top_arguments(poll, request_form)
    assert 4 == result

def test_create_final_top_msg():
    test_top_songs = [{
        'title': 'TestTitle',
        'artist': 'TestArtist',
        'link': None,
        'voted_users': []
    }]
    result = create_final_top_msg(test_top_songs)
    assert result == 'TOP 1 songs\nTestArtist - TestTitle ---- 0\n'

def test_start_top(mocker):
    mocked_admin = mocker.patch('handlers.decorators.is_admin')
    mocked_check_top_args = mocker.patch('handlers.commands.top.check_top_arguments')
    mocked_sort_songs = mocker.patch('handlers.commands.top.sort_songs')
    mocked_create_top_msg = mocker.patch('handlers.commands.top.create_final_top_msg')
    mocked_send_to_usr = mocker.patch('handlers.commands.top.send_msg_to_user')

    mocked_admin.return_value = True
    mocked_check_top_args.return_value = 1
    mocked_sort_songs.return_value = ['TestValue']
    mocked_create_top_msg.return_value = 'TestValue'

    start_top(Mock(), Mock(), Mock())
    assert mocked_send_to_usr.called