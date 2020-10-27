from chat.messages.chat_msg_functions import send_msg_to_user, send_msg_to_chat
from chat.users import is_admin
from chat.files import upload_file_to_user

import glob
import json

from poll import Poll
from slack import WebClient



def parse_disco_args(command_arguments: str) -> int:
    """
    Check the argument of /disco command for csv file with songs and return the data.
    """
    args = command_arguments.split()
    
    for arg in args: 
        if arg.endswith('.csv'):
            return arg
    return None

def check_for_not_finished_poll(dir_path: str, file_format: str):
    """
    Function that check if the user has not finished polls and if True, return the first unfinished.
    """
    list_of_files = glob.glob(dir_path+'*.'+file_format)
    
    for poll_file in list_of_files:
        with open(poll_file) as f:
            data = json.load(f)
            if data['is_started']:
                return data

def start_disco(client: WebClient, poll: Poll, request_form: dict) -> None:
    """
    Main function that is invoked when we run /disco command.
    /disco is valid only for channel admin.
    """
    if is_admin(client, request_form):
        if poll.is_started:
            send_msg_to_user(client, request_form, 'Previous poll is not finished. Type /lightsoff to finish it.')
        else:
            # Track unfinished polls 
            unfinished_poll = check_for_not_finished_poll('storage/json/history/', 'json')

            if unfinished_poll:
                send_msg_to_user(client, request_form, 'You have unfinished poll. Type /resume to resume your poll or /resume_delete to avoid this poll.')
                return 

            csv_file_url = parse_disco_args(request_form.get('text'))
            if not csv_file_url:
                send_msg_to_user(client, request_form, 'Please enter valid file path')
            else:
                songs = poll.storage.parse_csv_with_songs(csv_file_url)
                if not songs:
                    send_msg_to_user(
                        client, 
                        request_form,
                        "It seems like your CSV file structure is not valid. Use my template instead.",
                    )
                    upload_file_to_user(client, request_form, 'media/csv/template.csv')
                else:
                    poll.number_of_songs = len(songs)
                    poll.start(None, songs)
                    blocks = poll.update_block()
                    poll_response = send_msg_to_chat(client, request_form, 'MUSIC POLL', blocks=blocks)
                    poll.storage.update_message_id(poll_response['ts'])
                    poll.storage.save()
    else:
        send_msg_to_user(client, request_form, 'You have no permission to invoke this command.')
