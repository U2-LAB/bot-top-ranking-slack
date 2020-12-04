from unittest.mock import patch
from handlers.handlers import handle_commands


class CustomResponse:
    def __init__(self, text):
        self.apparent_encoding = 'UTF-8'
        self.encoding = None
        self.text = text

class CustomTestClient:
    def conversations_info(self, channel: str):
        data = {
            'Channel1':{
                'channel': {
                    'creator': 'User1'
            }},
            'Channel2':{
                'channel': {
                    'creator': 'User2'
            }}
        }
        return data.get(channel)


def check_command_for_handle_commands_func(command: str, patch_path: str):
    """
    Side function, that check if the mocked function is called,
    if the command is invoked.
    For example: /disco invokes start_disco.
    """
    request_form = {
        'command': command
    }
    with patch(patch_path) as mock_func:
        handle_commands(None, None, request_form)
        assert mock_func.called