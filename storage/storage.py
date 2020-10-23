from abc import abstractmethod


class AbstractPollStorage:
    """
    General abstract class for other storages.
    """

    # GET
    @abstractmethod
    def get_message_id(self) -> str:
        pass

    @abstractmethod
    def get_all_songs(self) -> list:
        pass

    # CREATE
    @abstractmethod
    def create_storage(self, message_id: str, songs: list):
        pass

    # UPDATE
    @abstractmethod
    def update_message_id(self, message_id: str):
        pass

    @abstractmethod
    def save(self):
        pass
    
    @abstractmethod
    def delete(self):
        pass