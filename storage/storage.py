from abc import abstractmethod


class AbstractPollStorage:
    """
    General abstract class for other storages.
    """

    @abstractmethod
    def save(self):
        pass

    # CREATE
    @abstractmethod
    def create_storage(self, messages: list):
        pass

    # GET
    @abstractmethod
    def get_all_songs(self):
        pass

    @abstractmethod
    def get_all_messages_id(self):
        pass

    @abstractmethod
    def get_message_from_song(self, song: dict):
        pass

    @abstractmethod
    def get_songs_chunk_with_selected_song(self, song_id: str):
        pass
    
    # For CSV
    @abstractmethod
    def parse_csv_with_songs(self, file_url: str, next_line: str, delimiter: str):
        pass
    
    # For unfinished polls
    @abstractmethod
    def drop_all(self):
        pass

    @abstractmethod
    def check_for_unfinished_poll(self):
        pass