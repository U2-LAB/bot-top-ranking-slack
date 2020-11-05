from chat.messages.chat_msg_functions import send_msg_to_user, send_msg_to_chat
from chat.users import is_admin
from chat.files import upload_file_to_user

from csv.parse_functions import parse_csv_with_songs

import glob
import json

from poll import Poll
from slack import WebClient


def parse_disco_args(command_arguments: str) -> str:
    """
    Check the argument of /disco command for csv file with songs and return the data.
    """
    args = command_arguments.split()
    
    for arg in args: 
        if arg.endswith('.csv'):
            return arg
    return None

def prepare_songs_for_poll(client: WebClient, poll: Poll, request_form: dict, songs: list) -> None:
    """
    Function that create and save poll in storage.
    """
    # If previous steps are good, do ...
    poll.number_of_songs = len(songs)
    poll.storage.data['is_started'] = True

    # As slack message allows having only < 50 songs in the message, so next code
    # seperate all the songs on 30 songs chunks and put each chunk in its message. 
    messages = []
    
    if len(songs) > 30:
        chunks = poll.divide_all_songs_into_chunks([songs])
    else:
        chunks = [songs]        

    send_msg_to_chat(client, request_form, "Please, vote for the next song to play 🎶")

    for songs_chunk in chunks:
        message_blocks = poll.create_poll_blocks(songs_chunk)
        response = send_msg_to_chat(client, request_form, '', blocks=message_blocks)
        messages.append({
            'id': response.get('ts'),
            'songs': songs_chunk
        })

    poll.storage.create_storage(messages)
    poll.storage.save() 


def start_disco(client: WebClient, poll: Poll, request_form: dict) -> None:
    """
    Function, that is invoked when we run /disco command.
    /disco is valid only for channel admin.
    """
    if is_admin(client, request_form):
        if poll.is_started:
            send_msg_to_user(client, request_form, 'Previous poll is not finished. Type /lightsoff to finish it.')
        else:
            # Track unfinished polls 
            unfinished_poll = poll.storage.check_for_unfinished_poll()

            if unfinished_poll:
                send_msg_to_user(client, request_form, 'You have unfinished poll. Type /resume to resume your poll or /drop to drop this poll.')
                return 

            # Preparing csv file with songs
            csv_file_url = parse_disco_args(request_form.get('text'))
            if not csv_file_url:
                send_msg_to_user(client, request_form, 'Please enter valid file path')
            else:
                songs = parse_csv_with_songs(csv_file_url)
                if not songs:
                    send_msg_to_user(client, request_form, "It seems like your CSV file structure is not valid. Use my template instead.")
                    upload_file_to_user(client, request_form, 'media/csv/template.csv') # Send user a csv template.
                else:
                    prepare_songs_for_poll(client, poll, request_form, songs)
    else:
        send_msg_to_user(client, request_form, 'You have no permission to invoke this command.')
