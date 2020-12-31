from handlers.decorators import only_admin

from poll import Poll
from slack import WebClient
from handlers.commands import disco
from chat.messages.chat_msg_functions import delete_msg_in_chat

@only_admin
def start_resume(client: WebClient, poll: Poll, request_form: dict) -> None:
    """
    Function, that is invoked when we run /drop command.
    /drop is valid only for channel admin.
    """
    poll.storage.data = poll.storage.check_for_unfinished_poll() # Get data from unfinished poll
    if (poll.storage.check_for_unfinished_poll()):
        channel_id = request_form.get('channel_id')
        for message_id in poll.storage.get_all_messages_id():
            delete_msg_in_chat(client, channel_id, message_id)
        
        songs = poll.storage.get_all_songs()

        if songs:
            disco.prepare_songs_for_poll(client, poll, request_form, songs)
