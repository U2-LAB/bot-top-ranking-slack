# Musical Slack Bot
Little musical bot for slack that have following features:
* Channel owner:
	* Invoke */disco* **optional:int** command to run music poll for all members of chat.
	* Invoke */lightsoff* to finish the poll and upload music file to the chat.
	* Invoke */poptop* **int** command to upload specific file, not a winner.
	* Invoke */settings* **option** **args** command to setup your bot settings.
		* List of options:
			* mp3 **on/off** to enable/disable uploading music.
	* **If your bot crashed during the survey, you can use following commands:**
		* */resume* to continue your unfinished poll.
		* */drop* to finish all the previous polls and have an ability to start new one.
* All members of the chat:
	* Invoke */top* **int** to show the list of **int** number of winners.
	* Invoke */poll_status* to show the status of the bot:
		* If it is running.
		* If it is enabled to upload music.

## Bot setup
1. Create new bot-app using [SlackApi](https://api.slack.com/apps)
2. Clone the repo
```bash
git clone https://github.com/Stashchen/bot-top-ranking-slack.git slack-bot
cd slack-bot 
```
3. Setup env
```bash
python -m venv env
```
4. Create env variables
```bash
# env/bin/activate
deactivate(){
	...
	unset SLACK_BOT_ACCESS_TOKEN
    unset SLACK_BOT_SIGNIN_TOKEN
    unset SLACK_BOT_VERIFICATION_TOKEN
}

export SLACK_BOT_ACCESS_TOKEN='YOUR_CODE' # https://api.slack.com/apps/YOUR_BOT_APP_ID/oauth?
export SLACK_BOT_SIGNIN_TOKEN='YOUR_CODE' # https://api.slack.com/apps/YOUR_BOT_APP_ID
export SLACK_BOT_VERIFICATION_TOKEN='YOUR_CODE' # https://api.slack.com/apps/YOUR_BOT_APP_ID
```
5. Setup your web-server(For testing - ngrok)
```bash
sudo apt update
sudo apt install snapd
sudo snap install ngrok 
```
6. Update your bot URLs (commands, interactivity, events)(this settings can be found in your bot-app):
	* commands URLs: **http://your_server_ip_or_domain/slack/commands**
	* interactivity URL: **http://your_server_ip_or_domain/slack/interactivity**
	* events URL: **http://your_server_ip_or_domain/slack/events**
7. Run the code
```bash
# First terminal
source ./env/bin/activate
python bot.py

# Second terminal (If you use ngok)
ngrok http 3000
```
**If you do not use ngrok, you need to run your own webserver with 3000 port!!!** 
