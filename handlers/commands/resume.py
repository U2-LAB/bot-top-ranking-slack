from chat.messages.chat_msg_functions import send_msg_to_user, send_msg_to_chat

from handlers.decorators import only_admin

from poll import Poll
from slack import WebClient


@only_admin
def start_resume(client: WebClient, poll: Poll, request_form: dict) -> None:
    """
    Function, that is invoked when we run /drop command.
    /drop is valid only for channel admin.
    """
    poll.storage.data = poll.storage.check_for_unfinished_poll() # Get data from unfinished poll  

    send_msg_to_chat(client, request_form, "Please, vote for the next song to play 🎶")
    for message in poll.storage.data['messages']:
        message_blocks = poll.create_poll_blocks(message.get('songs'))
        response = send_msg_to_chat(client, request_form, '', blocks=message_blocks)
        message['id'] = response.get('ts') # Update messages id