from chat.messages.chat_msg_functions import send_msg_to_chat, edit_msg_in_chat
from handlers.decorators import only_admin, poll_is_started
from poll import Poll
from songs_functionality.songs_functions import upload_song, sort_songs
from slack import WebClient
from storage.songs import Song


# If the error is occured during check_poptop_argument,
# this value is going to be used instead.
DEFAULT_EXCEPTION_VALUE = 1 

def check_poptop_argument(poll: Poll, request_form: dict) -> int:
    """
    Check the argument of /poptop command and return the value of song.
    """
    args = request_form.get('text')

    try:
        song_index = int(args)
    except ValueError:
        return DEFAULT_EXCEPTION_VALUE

    if 0 < song_index < poll.number_of_songs:
        return song_index
    else:
        return DEFAULT_EXCEPTION_VALUE

@only_admin
@poll_is_started
def start_poptop(client: WebClient, poll: Poll, request_form: dict) -> None:
    """
    Function, that is invoked when we run /poptop command.
    """
    channel_id = request_form.get('channel_id')
    selected_song_id = check_poptop_argument(poll, request_form)
    sorted_songs = sort_songs(poll.storage.get_all_songs())
    song = sorted_songs[selected_song_id-1]
    message = poll.storage.get_message_from_song(song)
    
    if poll.is_music_upload:
        upload_song(client, request_form, song)
    else:
        send_msg_to_chat(client, request_form, f'Poptop song {selected_song_id} is {song["author"]} - {song["title"]}')
    
    # Reste selected song votes
    Song.update(voted_users=[], mark=0).where(Song.id_music == song["id_music"]).execute()
    
    edit_msg_in_chat(client, channel_id, message.get('id'), "POPTOP SONG", poll.create_poll_blocks(poll.storage.get_all_songs()))
    poll.storage.save()
