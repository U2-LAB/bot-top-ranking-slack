from chat.messages.chat_msg_functions import send_msg_to_user
from chat.users import is_admin

from poll import Poll
from slack import WebClient



def start_drop(client: WebClient, poll: Poll, request_form: dict):
    """
    Main function that is invoked when we run /drop command.
    /drop is valid only for channel admin.
    """

    if is_admin(client, request_form):
        poll.storage.drop_all()
        send_msg_to_user(client, request_form, 'Previous polls are successfully dropped.')
    else:
        send_msg_to_user(client, request_form, 'You have no permission to invoke this command.')   