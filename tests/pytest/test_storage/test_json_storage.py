import json
import pytest
from unittest.mock import mock_open, patch


def test_get_all_songs(storage_for_tests):
    assert len(storage_for_tests.get_all_songs()) == 6

def test_get_all_messages_id(storage_for_tests):
    assert len(storage_for_tests.get_all_messages_id()) == 3

def test_get_message_from_song(storage_for_tests):
    song_in_messages = {
        'value': 2,
        'title': 'Title2',
        'artist': 'Artist2',
        'link': 'Link2'
    }
    right_message = {
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
    }

    assert right_message == storage_for_tests.get_message_from_song(song_in_messages)

def test_get_songs_chunk_with_selected_song_id(storage_for_tests):
    song_id = '3'
    right_chunk = [{
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
    assert right_chunk == storage_for_tests.get_songs_chunk_with_selected_song_id(song_id)

    # Test last chunk
    song_id = '6'
    right_chunk = [{
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
    assert right_chunk == storage_for_tests.get_songs_chunk_with_selected_song_id(song_id)

def test_save(storage_for_tests):
    with patch('builtins.open', mock_open()) as mocked_open:
        storage_for_tests.save()
        mocked_open.assert_called_once_with(storage_for_tests.file_path, 'w')
        handler = mocked_open()
        handler.write.assert_called_once_with(json.dumps(storage_for_tests.data))

def test_drop_all(mocker, storage_for_tests):
    mocked_glob = mocker.patch('storage.json.json_storage.glob')
    mocked_json = mocker.patch('storage.json.json_storage.json')

    mocked_glob.glob.return_value = ['test.json']
    with patch('builtins.open', mock_open()) as mocked_open:
        mocked_json.load.return_value = {'is_started': True}
        storage_for_tests.drop_all()
        mocked_json.load.return_value == {'is_started': False}
        mocked_open().write(json.dumps({'is_started': False}))

def test_check_for_unfinished_poll(mocker, storage_for_tests):
    mocked_glob = mocker.patch('storage.json.json_storage.glob')
    mocked_json = mocker.patch('storage.json.json_storage.json')

    mocked_glob.glob.return_value = ['test.json']

    with patch('builtins.open', mock_open()) as mocked_open:
        mocked_json.load.return_value = {'is_started': True}
        result = storage_for_tests.check_for_unfinished_poll()
        assert result == {'is_started': True}

        mocked_json.load.return_value = {'is_started': False}
        result = storage_for_tests.check_for_unfinished_poll()
        assert result == None