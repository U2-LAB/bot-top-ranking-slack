import json

from storage.storage import AbstractPollStorage


class JsonPollStorage(AbstractPollStorage):
    """
    Class that represent json file as storage.
    """

    def __init__(self):
        self.data = None

    def get_message_id(self) -> str:
        """
        Method to get message id.
        """
        return self.data['message_id']

    def get_all_songs(self) -> list:
        """
        Method to get list of songs.
        """
        return self.data['songs']

    def create_storage(self, message_id: str, songs: list):
        """
        Method that will create data and the way to store it.
        """
        self.data = {
            'message_id': message_id,
            'is_started': False,
            'songs': songs,
            'voted_users': []
        }     
    
    def update_message_id(self, message_id: str):
        """
        Method that will update message id with new one
        """
        self.data['message_id'] = message_id

    def save(self):
        pass

    def delete(self):
        pass