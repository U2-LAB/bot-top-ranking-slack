from slack import WebClient


def send_msg_to_user(client: WebClient, request_form: dict, msg: str, blocks=None) -> dict:
    """
    Function, that makes bot send message to user that send the request.
    """
    return client.chat_postEphemeral(
            channel=request_form.get('channel_id'),
            user=request_form.get('user_id'),
            text=msg,
            blocks=blocks
        )

def send_msg_to_chat(client: WebClient, request_form: dict, msg: str, blocks=None) -> dict:
    """
    Function, that makes bot send message to the chat.
    """
    return client.chat_postMessage(
            channel=request_form.get('channel_id'),
            text=msg,
            blocks=blocks
        )

def edit_msg_in_chat(client: WebClient, channel_id: str, msg_id: str, new_msg: str, blocks=None) -> dict:
    """
    Function, that edit selected message in the channel.
    """
    return client.chat_update(
        channel=channel_id,
        ts=msg_id,
        text=new_msg,
        blocks=blocks
    )