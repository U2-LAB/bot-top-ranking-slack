from chat.files import upload_file
from chat.messages.chat_msg_functions import send_msg_to_user, send_msg_to_chat, delete_msg_in_chat
from chat.users import is_admin
from poll import Poll
from songs_functionality.songs_functions import make_valid_song_name, download_song, delete_songs
from slack import WebClient


def start_lightsoff(client: WebClient, poll: Poll, request_form: dict) -> None:
    """
    Function, that is invoked when we run /lightsoff command.
    Finish the last poll and give the song.
    """
    if is_admin(client, request_form):
        if poll.is_started:
            send_msg_to_chat(client, request_form, 'The poll is finished. The winner is ...')
            winner = poll.find_the_winner_song()
            
            if poll.is_music_upload:
                song_title = make_valid_song_name(winner)
                download_song(song_title, winner['link'], './media/songs')
                upload_file(client, request_form, './media/songs/{}.mp3'.format(song_title))
                delete_songs('./media/songs')
            else:
                send_msg_to_chat(
                    client, 
                    request_form, 
                    f"{winner['artist']} - {winner['title']} with {len(winner['voted_users'])} votes !!!"
                )
            
            # Reset poll status
            poll.is_music_upload = False
            poll.is_started = False
            poll.save()
            
            # Delete message(s) from chat
            channel_id = request_form.get('channel_id')
            for message_id in poll.storage.get_all_messages_id():
                delete_msg_in_chat(client, channel_id, message_id)
        else:
            send_msg_to_user(client, request_form, 'No polls started yet. Use /disco command to run poll.')
    else:
        send_msg_to_user(client, request_form, 'You have no permission to invoke this command.')

        