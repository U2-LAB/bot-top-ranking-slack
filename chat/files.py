from slack import WebClient


def upload_file(client: WebClient, request_form: dict, file_to_upload) -> None:
    client.files_upload(
        channels=request_form.get('channel_id'),
        file=file_to_upload
    )

def upload_file_to_user(client: WebClient, request_form: dict, file_to_upload) -> None:
    client.files_upload(
        channels=request_form.get('user_id'),
        file=file_to_upload
    )