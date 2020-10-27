from chat.messages.chat_msg_functions import send_msg_to_user

from poll import Poll
from slack import WebClient


def start_poll_status(client: WebClient, poll: Poll, request_form: dict):
    """
    Main function that is invoked when we run /poll_status command.
    """
    status_msg = 'Current poll status:\n'

    if poll.is_started:
        status_msg += 'Poll is running\n'
    else: 
        status_msg += 'Poll is not running\n'

    if poll.is_music_upload:
        status_msg += 'Upload music: on\n'
    else:
        status_msg += 'Upload music: off\n'

    send_msg_to_user(client, request_form, status_msg)
