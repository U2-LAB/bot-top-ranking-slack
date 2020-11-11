import pytest

from poll import Poll
from unittest.mock import Mock


@pytest.fixture
def poll_for_tests(mocker):
    poll = Poll()
    poll.storage = Mock()
    poll.storage.data = {
        'is_started': False,
        'is_music_upload': False,
        'messages': []
    }
    return poll


def test_get_is_started(poll_for_tests):

    assert not poll_for_tests.is_started

def test_set_is_started(poll_for_tests):
    poll_for_tests.is_started = True

    assert poll_for_tests.is_started

    with pytest.raises(TypeError):
        poll_for_tests.is_started = 'Not boolean'

def test_get_is_music_upload(poll_for_tests):

    assert not poll_for_tests.is_music_upload

def test_set_is_music_upload(poll_for_tests):
    poll_for_tests.is_music_upload = True

    assert poll_for_tests.is_music_upload

    with pytest.raises(TypeError):
        poll_for_tests.is_music_upload = 'Not boolean'

def test_update_votes(poll_for_tests):
    poll_for_tests.storage.get_all_songs.return_value = [{
            'value': 1,
            'title': 'Title1',
            'artist': 'Artist1',
            'link': 'Link1',
            'voted_users': []
        },
        {
            'value': 2,
            'title': 'Title2',
            'artist': 'Artist2',
            'link': 'Link2',
            'voted_users': []
    }]

    add_user_result = [{
                'value': 1,
                'title': 'Title1',
                'artist': 'Artist1',
                'link': 'Link1',
                'voted_users': ['User1']
            },
            {
                'value': 2,
                'title': 'Title2',
                'artist': 'Artist2',
                'link': 'Link2',
                'voted_users': []
        }]

    remove_user_result = [{
            'value': 1,
            'title': 'Title1',
            'artist': 'Artist1',
            'link': 'Link1',
            'voted_users': []
        },
        {
            'value': 2,
            'title': 'Title2',
            'artist': 'Artist2',
            'link': 'Link2',
            'voted_users': []
    }]

    poll_for_tests.update_votes('User1','1')
    assert poll_for_tests.storage.get_all_songs.return_value == add_user_result

    poll_for_tests.update_votes('User1','1')
    assert poll_for_tests.storage.get_all_songs.return_value == remove_user_result

def test_divide_all_songs_into_chunks(poll_for_tests):
    start_list = [[1,2,3,4,5,6]]
    good_result = [[1,2], [3,4], [5,6]]

    result = poll_for_tests.divide_all_songs_into_chunks(start_list, 2)
    assert result == good_result

    start_list = [[1,2,3,4,5]]
    good_result = [[1,2], [3,4], [5]]

    result = poll_for_tests.divide_all_songs_into_chunks(start_list, 2)
    assert result == good_result

def test_create_poll_blocks(poll_for_tests):
    good_value_1 = [
        {
            'value': 1,
            'title': 'Title1',
            'artist': 'Artist1',
            'link': 'Link1',
            'voted_users': []
        },
        {
            'value': 2,
            'title': 'Title2',
            'artist': 'Artist2',
            'link': 'Link2',
            'voted_users': [1]
        }
    ]
    good_result_1 = [{
        "type": "section",
        "text": {
            "type": "plain_text",
            "text": "#"
        } 
        },
        {
        "type": "section",
        "text": {
            "type": "plain_text",
            "text": "1) Artist1 - Title1 ----- 0 votes"
        },
        'accessory': {
            'type': 'button',
            'text': {
                'type': 'plain_text',
                'text': 'Vote/Unvote'
            },
            'value': '1'
        }
        },
        {
        "type": "section",
        "text": {
            "type": "plain_text",
            "text": "2) Artist2 - Title2 ----- 1 votes"
        },
        'accessory': {
            'type': 'button',
            'text': {
                'type': 'plain_text',
                'text': 'Vote/Unvote'
            },
            'value': '2'
        }
    }]

    # Check different indexes
    good_value_2 = [
        {
            'value': 10,
            'title': 'Title10',
            'artist': 'Artist10',
            'link': 'Link10',
            'voted_users': []
        },
        {
            'value': 11,
            'title': 'Title11',
            'artist': 'Artist11',
            'link': 'Link11',
            'voted_users': []
        }
    ]
    good_result_2 = [{
        "type": "section",
        "text": {
            "type": "plain_text",
            "text": "#"
        } 
        },
        {
        "type": "section",
        "text": {
            "type": "plain_text",
            "text": "10) Artist10 - Title10 ----- 0 votes"
        },
        'accessory': {
            'type': 'button',
            'text': {
                'type': 'plain_text',
                'text': 'Vote/Unvote'
            },
            'value': '10'
        }
        },
        {
        "type": "section",
        "text": {
            "type": "plain_text",
            "text": "11) Artist11 - Title11 ----- 0 votes"
        },
        'accessory': {
            'type': 'button',
            'text': {
                'type': 'plain_text',
                'text': 'Vote/Unvote'
            },
            'value': '11'
        }
    }]

    assert good_result_1 == poll_for_tests.create_poll_blocks(good_value_1)
    assert good_result_2 == poll_for_tests.create_poll_blocks(good_value_2)

def test_find_the_winner_song(poll_for_tests):
        poll_for_tests.storage.get_all_songs.return_value = [{
                'value': 1,
                'title': 'Title1',
                'artist': 'Artist1',
                'link': 'Link1',
                'voted_users': []
            },
            {
                'value': 2,
                'title': 'Title2',
                'artist': 'Artist2',
                'link': 'Link2',
                'voted_users': [1, 2, 3] # Winner
            },
            {
                'value': 3,
                'title': 'Title3',
                'artist': 'Artist3',
                'link': 'Link3',
                'voted_users': []
        }]

        correct_winner = {
            'value': 2,
            'title': 'Title2',
            'artist': 'Artist2',
            'link': 'Link2',
            'voted_users': [1, 2, 3]
        }

        winner = poll_for_tests.find_the_winner_song()
        assert correct_winner == winner