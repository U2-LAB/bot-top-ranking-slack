from chat.messages.chat_msg_functions import send_msg_to_user, send_msg_to_chat
from chat.users import is_admin

from songs_functionality.songs_functions import get_all_songs
from slack import WebClient

from poll import Poll


def parse_disco_args(limit: int, command_arguments: str) -> int:
    """
    Check the argument of /disco command and return the number of songs,
    that are going to be listed.
    VALID: 1 < limit <= 10
    """
    try:
        # As it is valid to have only integer as argument, then it should
        # Be possible to convert it
        limit_arg = int(command_arguments)
    except ValueError:
        return limit

    if 1 < limit_arg <= limit:
        return limit_arg
    else:
        return limit

def start_disco(client: WebClient, poll: Poll, request_form: dict) -> None:
    """
    Main function that is invoked when we run /disco command.
    /disco is valid only for channel admin.
    """
    if is_admin(client, request_form):
        if poll.is_started:
            send_msg_to_user(client, request_form, 'Previous poll is not finished. Type /lightsoff to finish it.')
        else:
            songs = get_all_songs(poll.number_of_songs)
            poll.start(None, songs)
            blocks = poll.update_block()
            poll_response = send_msg_to_chat(client, request_form, 'MUSIC POLL', blocks=blocks)
            poll.storage.update_message_id(poll_response['ts'])
    else:
        send_msg_to_user(client, request_form, 'You have no permission.')
