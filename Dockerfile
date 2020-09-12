FROM python:latest

RUN pip install python-telegram-bot

COPY TelegramGamesBot TelegramGamesBot

WORKDIR TelegramGamesBot

CMD ["python","Main.py"]