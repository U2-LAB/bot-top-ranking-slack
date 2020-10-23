from flask import Flask, Response, request
import json
import os
from threading import Thread
from poll import Poll
from slack import WebClient
from slackeventsapi import SlackEventAdapter

from handlers.handlers import handle_commands, handle_interactivity


# Start Flask app that will be produce all the requests
app = Flask(__name__)

# Get venv variables
SLACK_BOT_SIGNIN_TOKEN = os.environ.get('SLACK_BOT_SIGNIN_TOKEN')
SLACK_BOT_ACCESS_TOKEN = os.environ.get('SLACK_BOT_ACCESS_TOKEN')
SLACK_BOT_VERIFICATION_TOKEN = os.environ.get('SLACK_BOT_VERIFICATION_TOKEN')

# Get slack api client and poll object
slack_client = WebClient(SLACK_BOT_ACCESS_TOKEN)
music_poll = Poll(10)

# Enable several routes to the server
@app.route("/")
def event_hook(request):
    """
    Main hook that checks all the request with Slack token.
    """
    json_dict = json.loads(request.body.decode("utf-8"))
    if json_dict["token"] != SLACK_BOT_VERIFICATION_TOKEN:
        return {"status": 403}

    if "type" in json_dict:
        if json_dict["type"] == "url_verification":
            response_dict = {"challenge": json_dict["challenge"]}
            return response_dict
    return {"status": 500}

@app.route('/slack/commands', methods=['POST'])
def command_hook():
    """
    Function to handle all the bots commands.
    """
    handle_commands(client=slack_client, poll=music_poll, request_form=request.form)
    return Response(status=200)

@app.route('/slack/interactivity', methods=['POST'])
def interactivity_hook():
    """
    Function, that handles all the interactivity (buttons, checkboxes, slack shortcuts, etc.).
    But in that bot, it will handle only poll selection interactivity.
    """
    handle_interactivity(client=slack_client, request=request, poll=music_poll)
    return Response(status=200)

slack_events_adapter = SlackEventAdapter(
    SLACK_BOT_SIGNIN_TOKEN, "/slack/events", app
) 


if __name__ == "__main__":
  app.run(port=3000)