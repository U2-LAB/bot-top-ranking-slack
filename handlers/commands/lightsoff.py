from chat.messages.chat_msg_functions import send_msg_to_chat, delete_msg_in_chat

from handlers.decorators import only_admin, poll_is_started
from handlers.commands.disco import create_songs

from poll import Poll
from songs_functionality.songs_functions import upload_song
from slack import WebClient
from storage.songs import Song


@only_admin
@poll_is_started
def start_lightsoff(client: WebClient, poll: Poll, request_form: dict) -> None:
    """
    Function, that is invoked when we run /lightsoff command.
    Finish the last poll and give the song.
    """
    send_msg_to_chat(client, request_form, 'The poll is finished. The winner is ...')
    winner = poll.find_the_winner_song()
    
    if poll.is_music_upload:
        upload_song(client, request_form, winner)
    else:
        send_msg_to_chat(
            client, 
            request_form, 
            f"{winner['author']} - {winner['title']} with {len(winner['voted_users'])} votes !!!"
        )
    
    # Reset poll status
    poll.storage.data['is_started'] = False
    poll.storage.save()
    
    # Delete message(s) from chat
    channel_id = request_form.get('channel_id')
    for message_id in poll.storage.get_all_messages_id():
        delete_msg_in_chat(client, channel_id, message_id)
    
    Song.truncate_table(restart_identity=True)
    create_songs()
