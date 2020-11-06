from chat.messages.chat_msg_functions import send_msg_to_user, send_msg_to_chat, edit_msg_in_chat
from handlers.decorators import only_admin, poll_is_started
from poll import Poll
from songs_functionality.songs_functions import upload_song, sort_songs
from slack import WebClient


def check_poptop_argument(poll: Poll, request_form: dict) -> int:
    """
    Check the argument of /poptop command and return the value of song.
    """
    args = request_form.get('text')

    try:
        song_index = int(args)
    except ValueError:
        return 1

    if 0 < song_index < poll.number_of_songs:
        return song_index
    else:
        return 1 

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
        send_msg_to_chat(client, request_form, f'Poptop song {selected_song_id} is {song["artist"]} - {song["title"]}')
    
    # Reste selected song votes
    song['voted_users'] = []
    
    edit_msg_in_chat(client, channel_id, message.get('id'), "POPTOP SONG", poll.create_poll_blocks(message.get('songs')))
    poll.storage.save()    