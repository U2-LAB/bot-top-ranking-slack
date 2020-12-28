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
# .env
SLACK_BOT_ACCESS_TOKEN='YOUR_CODE' # https://api.slack.com/apps/YOUR_BOT_APP_ID/oauth?
SLACK_BOT_SIGNIN_TOKEN='YOUR_CODE' # https://api.slack.com/apps/YOUR_BOT_APP_ID
SLACK_BOT_VERIFICATION_TOKEN='YOUR_CODE' # https://api.slack.com/apps/YOUR_BOT_APP_ID
USER_DB = 'USERNAME'
PASSWORD_DB = 'PASSWORD'
HOST_DB = 'LOCALHOST'
PORT_DB = PORT
NAME_DB = 'DB-NAME'
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

## Docker run

1. Build docker image from Dockerfile
```bash
docker build -t slack-bot .
```
2. Setup your web-server
```bash
sudo apt update
sudo apt install snapd
sudo snap install ngrok 
```
3. Run the code
```bash
# First terminal (If you use ngrok)
ngrok http 3000

# Second terminal
docker run -d --rm --name slack --net host slack-bot:latest 
```
## Testing Bot
If you would like to test bot functionality, you should run:
* unittest:
```bash
./start_unittests.sh
```
