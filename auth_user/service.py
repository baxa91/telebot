from typing import NoReturn

import telebot

from auth_user import models, constants
from core import settings


bot = telebot.TeleBot(settings.TELEGRAM_BOT)


def send_message(user: models.User, message: str) -> NoReturn:
    bot.send_message(
        user.telegram_id, constants.MESSAGE.format(name=user.username, message=message),
        parse_mode='Markdown'
    )