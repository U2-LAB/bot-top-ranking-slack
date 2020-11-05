from chat.messages.chat_msg_functions import edit_msg_in_chat

from handlers.commands.disco import parse_disco_args, start_disco
from handlers.commands.drop import start_drop
from handlers.commands.lightsoff import start_lightsoff
from handlers.commands.poll_status import start_poll_status
from handlers.commands.poptop import start_poptop
from handlers.commands.resume import start_resume
from handlers.commands.settings import start_settings
from handlers.commands.top import start_top

import json

from poll import Poll

from slack import WebClient


# Does this functions needs to be tested?


def handle_commands(client: WebClient, poll: Poll, request_form: dict) -> None:
    """
    Function, that will handle all the commands that is going to be sent to the bot.
    """
    command = request_form.get('command')

    if command == '/disco':
        start_disco(client, poll, request_form)
    elif command == '/lightsoff':
        start_lightsoff(client, poll, request_form)
    elif command == '/poptop':
        start_poptop(client, poll, request_form)
    elif command == '/top':
        start_top(client, poll, request_form)
    elif command == '/poll_status':
        start_poll_status(client, poll, request_form)
    elif command == '/settings':
        start_settings(client, poll, request_form)
    elif command == '/drop':
        start_drop(client, poll, request_form)
    elif command == '/resume':
        start_resume(client, poll, request_form)

def handle_interactivity(client: WebClient, request, poll: Poll) -> None:
    """
    Function, that handles all the bot interactivity.
    """
    
    payload = json.loads(request.form.get('payload'))

    if payload['type'] == 'block_actions':
        # If button was tracked
        user_id = payload['user']['id']
        selected_song_id = payload['actions'][0]['value']
        songs_chunk_with_selected_song = poll.storage.get_songs_chunk_with_selected_song_id(selected_song_id)
        
        poll.update_votes(user_id, selected_song_id)

        channel_id = payload['container']['channel_id']
        message_id = payload['container']['message_ts']

        edit_msg_in_chat(client, channel_id, message_id, '', poll.create_poll_blocks(songs_chunk_with_selected_song))
        poll.storage.save()
