from chat.messages.chat_msg_functions import edit_msg_in_chat

from handlers.commands.disco import parse_disco_args, start_disco
from handlers.commands.lightsoff import start_lightsoff

import json

from poll import Poll

from slack import WebClient

from handlers.interactivity.request_parse_functions import get_payload_as_dict


def handle_commands(client: WebClient, poll: Poll, request_form: dict) -> None:
    """
    Function that will handle all the commands that is going to be sent to the bot.
    """

    command = request_form.get('command')

    if command == '/disco':
        if command_args:=request_form.get('text'):
            poll.number_of_songs = parse_disco_args(poll.number_of_songs, command_args)
            start_disco(client, poll, request_form)
        else:
            start_disco(client, poll, request_form)
    elif command == '/lightsoff':
        start_lightsoff(client, poll, request_form)

def handle_interactivity(client: WebClient, request, poll: Poll) -> None:
    """
    Function, that handles all the bot interactivity.
    """
    
    payload = json.loads(request.form.get('payload'))

    if payload['type'] == 'block_actions':
        # If button was tracked
        user_id = payload['user']['id']
        selected_song = payload['actions'][0]['value']
        poll.update_votes(user_id, selected_song)
        updated_poll_blocks = poll.update_block()

        channel_id = payload['container']['channel_id']
        message_id = payload['container']['message_ts']

        edit_msg_in_chat(client, channel_id, message_id, 'MUSIC POLL', updated_poll_blocks)