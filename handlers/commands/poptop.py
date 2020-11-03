from chat.messages.chat_msg_functions import send_msg_to_user, send_msg_to_chat, edit_msg_in_chat
from chat.users import is_admin
from chat.files import upload_file
from poll import Poll
from songs_functionality.songs_functions import make_valid_song_name, download_song, delete_songs, sort_songs
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

def poptop_selected_song(client: WebClient, poll: Poll, request_form: dict) -> None:
    """
    Get selected song, upload it and reset votes.
    """
    channel_id = request_form.get('channel_id')
    selected_song_id = check_poptop_argument(poll, request_form)
    sorted_songs = sort_songs(poll.storage.get_all_songs())
    song = sorted_songs[selected_song_id-1]
    message = poll.storage.get_message_from_song(song)
    
    if poll.is_music_upload:
        song_title = make_valid_song_name(song)
        send_msg_to_chat(client, request_form, 'Your poptop song is downloading. Wait please')
        download_song(song_title, song['link'], './media/songs')
        upload_file(client, request_form, './media/songs/{}.mp3'.format(song_title))
        delete_songs('./media/songs')
    else:
        send_msg_to_chat(client, request_form, f'Poptop song {selected_song_id} is {song["artist"]} - {song["title"]}')
    
    # Reste selected song votes
    song['voted_users'] = []
    
    edit_msg_in_chat(client, channel_id, message.get('id'), "POPTOP SONG", poll.create_poll_blocks(message.get('songs')))
    poll.storage.save()

def start_poptop(client: WebClient, poll: Poll, request_form: dict) -> None:
    """
    Function, that is invoked when we run /poptop command.
    """
    if is_admin(client, request_form):
        if poll.is_started:
            poptop_selected_song(client, poll, request_form)
        else:
            send_msg_to_user(client, request_form, 'To invoke /poptop you need to run /disco first.')
    else:
        send_msg_to_user(client, request_form, 'You have no permission.')
        