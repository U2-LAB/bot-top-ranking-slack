from chat.messages.chat_msg_functions import send_msg_to_user, send_msg_to_chat, edit_msg_in_chat
from chat.users import is_admin
from chat.files import upload_file
from poll import Poll
from songs_functionality.songs_functions import make_valid_song_name, download_song, delete_songs
from slack import WebClient


def check_poptop_song(poll: Poll, request_form: dict) -> int:
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

def poptop_selected_song(client: WebClient, poll: Poll, request_form: dict) -> None:
    """
    Get selected song, upload it and reset votes.
    """
    message_id = poll.storage.get_message_id()
    channel_id = request_form.get('channel_id')

    song_id = check_poptop_song(poll, request_form)
    song = poll.storage.get_selected_song(song_id)
    song_title = make_valid_song_name(song)
    send_msg_to_chat(client, request_form, 'Your poptop song is downloading. Wait please')
    download_song(song_title, song['link'], './media')
    upload_file(client, request_form, './media/{}.mp3'.format(song_title))
    song['voted_users'] = []
    
    edit_msg_in_chat(client, channel_id, message_id, "POPTOP SONG", poll.update_block())
    
    delete_songs('./media')


def start_poptop(client: WebClient, poll: Poll, request_form: dict) -> None:
    """
    Function that is invoked when we run /poptop command.
    """
    if is_admin(client, request_form):
        if poll.is_started:
            poptop_selected_song(client, poll, request_form)
        else:
            send_msg_to_user(client, request_form, 'To invoke /poptop you need to run /disco first.')
    else:
        send_msg_to_user(client, request_form, 'You have no permission.')
        