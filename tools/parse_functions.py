import requests

from typing import Union, List


def parse_csv_with_songs(file_url: str, next_line='\r\n', delimiter=';') -> Union[list, List[dict]]:
    """
    Function, that will download csv file with songs.
    """
    response = requests.get(file_url)
    response.encoding = response.apparent_encoding

    header, *rows = response.text.split(next_line)

    # Check the right format fo the csv file
    header = header.split(delimiter)
    if not (header[0] == 'Title' and header[1] == 'Artist' and header[2] == 'Link'): 
        return [] 

    parsed_csv_data = []

    for index, row in enumerate(rows, start=1):
        if not row:
            continue
        
        row_as_list = row.split(delimiter)
        song = {
            'value': index,
            'title': row_as_list[0],
            'artist': row_as_list[1],
            'link': row_as_list[2] if row_as_list[2] else None,
            'voted_users': []
        }
        parsed_csv_data.append(song)

    return parsed_csv_data