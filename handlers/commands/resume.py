from chat.messages.chat_msg_functions import send_msg_to_user, send_msg_to_chat
from chat.users import is_admin

from poll import Poll
from slack import WebClient



def start_resume(client: WebClient, poll: Poll, request_form: dict):
    """
    Main function that is invoked when we run /drop command.
    /drop is valid only for channel admin.
    """

    if is_admin(client, request_form):
        poll.storage.data = poll.storage.check_for_unfinished_poll()  
        
        send_msg_to_chat(client, request_form, "Please, vote for the next song to play 🎶")

        for message in poll.storage.data['messages']:
            message_blocks = poll.create_poll_blocks(message.get('songs'))
            response = send_msg_to_chat(client, request_form, '', blocks=message_blocks)
    else:
        send_msg_to_user(client, request_form, 'You have no permission to invoke this command.')   