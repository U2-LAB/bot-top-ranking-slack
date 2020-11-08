from chat.messages.chat_msg_functions import send_msg_to_user
from chat.users import is_admin


def only_admin(func):
    def wrapper(client, poll, request_form):
        if is_admin(client, request_form):
            func(client, poll, request_form)
        else:
            send_msg_to_user(client, request_form, 'You have no permission to invoke this command.')
    return wrapper

def poll_not_started(func):
    def wrapper(client, poll, request_form):
        if poll.is_started:
            send_msg_to_user(client, request_form, 'Previous poll is not finished. Type /lightsoff to finish it.')
        else:
            func(client, poll, request_form)
    return wrapper

def poll_is_started(func):
    def wrapper(client, poll, request_form):
        if poll.is_started:
            func(client, poll, request_form)
        else:
            send_msg_to_user(client, request_form, 'No polls started yet. Use /disco command to run poll.')
    return wrapper