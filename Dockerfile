FROM python:3.8

RUN mkdir -p /slack-bot/
WORKDIR /slack-bot/

COPY ./requirements.txt /slack-bot/

RUN pip3 install -r requirements.txt

COPY . /slack-bot/

EXPOSE 3000

CMD ["python3", "bot.py"]