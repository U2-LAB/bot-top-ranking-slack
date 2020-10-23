from chat.files import upload_file
from chat.messages.chat_msg_functions import send_msg_to_user, send_msg_to_chat
from poll import Poll
from songs_functionality.songs_functions import make_valid_song_name, download_song, delete_songs
from slack import WebClient


def start_lightsoff(client: WebClient, poll: Poll, request_form: dict):
    """
    Function that is invoked when we run /lightsoff command.
    Finish the last poll and give the song.
    """
    if poll.is_started:
        send_msg_to_chat(client, request_form, 'The poll is finished. The winner is ...')
        winner = poll.find_the_winner_song()
        song_title = make_valid_song_name(winner)
        download_song(song_title, winner['link'], './media')
        upload_file(client, request_form, './media/{}.mp3'.format(song_title))
        poll.is_started = False
        delete_songs('./media')
    else:
        send_msg_to_user(client, request_form, 'No polls started yet. Use /disco command to run poll.')


        