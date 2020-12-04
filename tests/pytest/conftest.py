import pytest
from unittest.mock import Mock

from poll import Poll
from storage.json.json_storage import JsonPollStorage


@pytest.fixture
def mocked_not_started_poll():
    mocked_poll = Mock()
    mocked_poll.is_started = False
    mocked_poll.is_music_upload = False 
    mocked_poll.storage.data = {}
    return mocked_poll

@pytest.fixture
def mocked_started_poll():
    mocked_poll = Mock()
    mocked_poll.is_started = True
    mocked_poll.is_music_upload = True
    mocked_poll.storage.data = {}
    return mocked_poll

@pytest.fixture
def poll_for_tests():
    poll = Poll()
    poll.storage = Mock()
    poll.storage.data = {
        'is_started': False,
        'is_music_upload': False,
        'messages': []
    }
    return poll

@pytest.fixture
def storage_for_tests():
    storage = JsonPollStorage('')
    storage.data['messages'] = [{
        'id': 1,
        'songs': [{
            'value': 1,
            'title': 'Title1',
            'artist': 'Artist1',
            'link': 'Link1'
        },
        {
            'value': 2,
            'title': 'Title2',
            'artist': 'Artist2',
            'link': 'Link2'
        }]
        },
        {
        'id': 2,
        'songs': [{
            'value': 3,
            'title': 'Title3',
            'artist': 'Artist3',
            'link': 'Link3'
        },
        {
            'value': 4,
            'title': 'Title4',
            'artist': 'Artist4',
            'link': 'Link4'
        }] 
        },
        {
        'id': 3,
        'songs': [{
            'value': 5,
            'title': 'Title5',
            'artist': 'Artist5',
            'link': 'Link5'
        },
        {
            'value': 6,
            'title': 'Title6',
            'artist': 'Artist6',
            'link': 'Link6'
        }]
    }]

    return storage