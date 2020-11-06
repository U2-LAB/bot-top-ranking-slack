from chat.messages.chat_msg_functions import send_msg_to_user

from handlers.decorators import only_admin

from poll import Poll
from slack import WebClient


@only_admin
def start_drop(client: WebClient, poll: Poll, request_form: dict) -> None:
    """
    Function, that is invoked when we run /drop command.
    /drop is valid only for channel admin.
    """
    poll.storage.drop_all()
    send_msg_to_user(client, request_form, 'Previous polls are successfully dropped.')
