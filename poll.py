from storage.json.storage import JsonPollStorage

POLL_BLOCK_BLUEPRINT = [{
    "type": "section",
    "text": {
        "type": "plain_text",
        "text": "Please, vote for the next song to play 🎶"
    }
}]

class Poll:
    """
    Class for poll in Slack messages.
    It represents the block of the message entity in the Slack.
    """

    def __init__(self, number_of_songs: int) -> None:
        self.storage = JsonPollStorage('storage/json/history/')
        self.number_of_songs = number_of_songs

    @property
    def is_started(self):
        return self.storage.data['is_started']

    @is_started.setter
    def is_started(self, value):
        if isinstance(value, bool):
            self.storage.data['is_started'] = value

    @property
    def is_music_upload(self):
        return self.storage.data['is_music_upload']
    
    @is_music_upload.setter
    def is_music_upload(self, value):
        if isinstance(value, bool):
            self.storage.data['is_music_upload'] = value
        
    def reset_settings(self) -> None:
        """
        Function, that will set default values to variables.
        """
        self.is_music_upload = False
        self.is_started = False

    def start(self, message_id: str, songs: list) -> None:
        """
        Method that start poll.
        """
        self.storage.create_storage(message_id, songs)
        self.is_started = True

    def update_votes(self, user_id: str, selected_song: str) -> None:
        """
        Method that updates votes in the storage with new one.
        """
        songs = self.storage.get_all_songs()
        message_id = self.storage.get_message_id()

        for song in songs:
            if song['value'] == int(selected_song):
                if user_id not in song['voted_users']:
                    song['voted_users'].append(user_id)
                else:
                    song['voted_users'].pop(song['voted_users'].index(user_id))
   
    def update_block(self, user_id=None) -> list:
        """
        Method that updates block of songs in the current poll.
        """
        all_songs = self.storage.get_all_songs()

        poll_block = POLL_BLOCK_BLUEPRINT[:]

        for index, song in enumerate(all_songs, start=1):
            new_section = {
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": f"{index}) {song['artist']} - {song['title']} ----- {len(song['voted_users'])} votes"
                },
                'accessory': {
                    'type': 'button',
                    'text': {
                        'type': 'plain_text',
                        'text': 'Vote'
                    },
                    'value': str(index)
                }
            }
            poll_block.append(new_section)

        return poll_block

    def find_the_winner_song(self) -> dict:
        """
        Method that parse songs in the storage and find song with max votes.
        If two songs have same number of votes, it will return the first one. 
        """
        songs = self.storage.get_all_songs()

        winner = songs[0]
        
        for song in songs[1:]:
            if len(song['voted_users']) > len(winner['voted_users']):
                winner = song

        return winner