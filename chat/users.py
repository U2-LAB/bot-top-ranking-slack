from slack import WebClient

def is_admin(client: WebClient, request_form: dict) -> bool:
    """
    Checks if the user that send the request is admin.
    """
    info = client.conversations_info(
            channel=request_form.get('channel_id')
        )

    if info['channel']['creator'] != request_form['user_id']:
        return False
    return True

