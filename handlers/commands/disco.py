from chat.messages.chat_msg_functions import send_msg_to_user, send_msg_to_chat

from typing import Union
from tools.create_test_csv import get_all_songs as download_songs

from handlers.decorators import only_admin, poll_not_started

from poll import Poll
from slack import WebClient

from storage.songs import Song


def parse_disco_args(command_arguments: str) -> Union[str, None]:
    """
    Check the argument of /disco command for csv file with songs and return the data.
    """
    args = command_arguments.split()
    
    for arg in args: 
        if arg.endswith('.csv'):
            return arg

def create_songs():
    """
    Create SQL row in database that save data about our songs
    """
    if Song.select().count() == 0:
        for idx, song in enumerate(download_songs()):
            Song.create(title=song[0], link=song[2], author=song[1], voted_users=[])
            Song.update(pos=idx + 1).where(Song.id_music == idx + 1).execute()

def prepare_songs_for_poll(client: WebClient, poll: Poll, request_form: dict, songs: list) -> None:
    """
    Function that create and save poll in storage.
    """
    # If previous steps are good, do ...
    poll.number_of_songs = len(songs)
    poll.storage.data['is_started'] = True

    # As slack message allows having only < 50 songs in the message, so next code
    # seperate all the songs on 30 songs chunks and put each chunk in its message. 
    
    if len(songs) > 30:
        chunks = poll.divide_all_songs_into_chunks([songs])
    else:
        chunks = [songs]        

    send_msg_to_chat(client, request_form, "Please, vote for the next song to play 🎶")

    for songs_chunk in chunks:
        message_blocks = poll.create_poll_blocks(songs_chunk)
        response = send_msg_to_chat(client, request_form, '', blocks=message_blocks)
        Song.update(message_id=response.get('ts')).where(Song.id_music << [song["id_music"] for song in songs_chunk]).execute()
    
    poll.storage.save()


@only_admin
@poll_not_started
def start_disco(client: WebClient, poll: Poll, request_form: dict) -> None:
    """
    Function, that is invoked when we run /disco command.
    """
    # Track unfinished polls 
    if poll.storage.check_for_unfinished_poll():
        send_msg_to_user(client, request_form, 'You have unfinished poll. Type /resume to resume your poll or /drop to drop this poll.')
        return 

    create_songs()

    songs = poll.storage.get_all_songs() # Get songs from database

    if songs:
        prepare_songs_for_poll(client, poll, request_form, songs)
    else:
        send_msg_to_user(client, request_form, "It seems like you dont't have song in your database")
