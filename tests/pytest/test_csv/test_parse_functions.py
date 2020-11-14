from tools.parse_functions import parse_csv_with_songs

from tests.common_data import CustomResponse


def test_parse_csv_with_songs(mocker):
    mocked_request = mocker.patch('tools.parse_functions.requests')

    good_response_text = "Title;Artist;Link\r\nTitle1;Artist1;Link1\r\nTitle2;Artist2;Link2\r\nTitle3;Artist3;Link3\r\n"
    bad_response_text = "Notitle;NotArtist;NotLink\r\nTitle1;Artist1;Link1\r\nTitle2;Artist2;Link2\r\nTitle3;Artist3;Link3\r\n"

    mocked_request.get.return_value = CustomResponse(good_response_text)

    valid_data = [{
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
        },
        {
        'value': 3,
        'title': 'Title3',
        'artist': 'Artist3',
        'link': 'Link3',
        'voted_users': []
    }]
    data = parse_csv_with_songs('test/path')
    assert valid_data == data

    # Bad CSV template
    mocked_request.get.return_value = CustomResponse(bad_response_text)
    data = parse_csv_with_songs('test/path')
    assert [] == data