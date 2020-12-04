from chat.messages.chat_msg_functions import send_msg_to_user
from chat.users import is_admin

from typing import Tuple

from handlers.decorators import only_admin

from poll import Poll
from slack import WebClient


def get_settings_option_and_option_argument(command_arguments: str) -> Tuple[str, str]:
    """
    Function, that parse command arguments and return:
        option - first argument
        arg - all the rest arguments.
    """
    if not command_arguments:
        return 'common', [] # 'common' is the option, when user does not use any option.
    else:
        option, *args = command_arguments.split()
        if not args:
            return option, ''
    return option, args[0]


@only_admin
def start_settings(client: WebClient, poll: Poll, request_form: dict) -> None:
    """
    Function, that is invoked when we run /settings command.
    """
    option, arg = get_settings_option_and_option_argument(request_form.get('text'))

    if option == 'common':
        send_msg_to_user(
            client,
            request_form,
            'List of valid commands:\n1. settings mp3 <on/off>'
        )
    elif option == 'mp3':
        if arg == 'on' or arg == 'off':
            if arg == 'on':
                poll.is_music_upload = True
                send_msg_to_user(client, request_form, 'Uploading music: ON')
            else:
                poll.is_music_upload = False
                send_msg_to_user(client, request_form, 'Uploading music: OFF')
            poll.storage.save()
        else:
            send_msg_to_user(
                client, 
                request_form, 
                'mp3 <on/off> - it will on/off uploading music to chat functionality.'
            )