from storage.json.storage import JsonPollStorage


POLL_BLOCK_BLUEPRINT = [{
    "type": "section",
    "text": {
        "type": "plain_text",
        "text": "##########"
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
        self.is_started = False
        self.is_music_upload = False

    def update_votes(self, user_id: str, selected_song_id: str) -> None:
        """
        Method that updates votes in the storage with new one.
        """
        songs = self.storage.get_all_songs()

        for song in songs:
            if song['value'] == int(selected_song_id):
                if user_id not in song['voted_users']:
                    song['voted_users'].append(user_id)
                else:
                    song['voted_users'].pop(song['voted_users'].index(user_id))
   
    def divide_all_songs_into_chunks(self, songs_in_list: list, songs_in_chunk=30) -> list:
        """
        As it is allowed to use <= 50 units in slack messages,
        So here is the function that check to seperate messages.
        """
        latest_chunk_of_songs = songs_in_list[-1]
        if len(latest_chunk_of_songs) > songs_in_chunk:
            updated_chunk = latest_chunk_of_songs[:songs_in_chunk]
            new_chunk = latest_chunk_of_songs[songs_in_chunk:]
            songs_in_list[-1] = updated_chunk
            songs_in_list.append(new_chunk)
            return self.divide_all_songs_into_chunks(songs_in_list)
        else:
            return songs_in_list

    def add_songs_chunks_to_messages(self, chunks: list) -> None:
        """
        Update storage.data dict with messages.
        """
        messages = []
        for chunk in chunks:
            message = {
                'songs': chunk
            }
            messages.append(message)

        self.storage.create_storage(messages)

    def create_poll_blocks(self, songs_chunk: list) -> list:
        """
        Method that creates block of songs in the current poll.
        """
        poll_block = POLL_BLOCK_BLUEPRINT[:]
        
        start_index = songs_chunk[0].get('value')

        for index, song in enumerate(songs_chunk, start=start_index):
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
                        'text': 'Vote/Unvote'
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

    def save(self):
        """
        Save poll data to storage.
        """
        self.storage.save(self.is_started, self.is_music_upload)