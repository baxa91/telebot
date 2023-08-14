import os
import django
import telebot
from telebot import types


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from django.contrib.auth.hashers import check_password
from core import settings
from auth_user.models import User


bot = telebot.TeleBot(settings.TELEGRAM_BOT)


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, selective=True)
    markup.add(types.KeyboardButton('Отправить логин и пароль', request_location=False,
                                    request_contact=False))
    bot.send_message(
        message.chat.id,
        "Пожалуйста, введите логин и пароль в следующем формате:\n\n*Логин* - *Пароль*",
        parse_mode='Markdown', reply_markup=markup
    )
    bot.register_next_step_handler(message, process_login_password)


def process_login_password(message):
    login_password = message.text
    parts = login_password.split('-')

    if len(parts) == 2:
        login = parts[0].strip()
        password = parts[1].strip()

        user = User.objects.filter(username=login).first()
        if not user:
            bot.send_message(
                message.chat.id,
                "Нет такого пользователя, сперва зарегистрируйтесь на нашем сайте",
                parse_mode='Markdown'
            )
            return start(message)

        password_correct = check_password(password, user.password)

        if not password_correct:
            bot.send_message(
                message.chat.id,
                "Неверный пароль, пожалуйста введите корректный пароль",
                parse_mode='Markdown'
            )
            return start(message)
        else:
            user.telegram_id = message.chat.id
            user.save()
            bot.send_message(
                message.chat.id,
                "Поздравляю, теперь я могу отправлять вам сообщение",
                parse_mode='Markdown'
            )
    else:
        bot.send_message(message.chat.id,
                         "Пожалуйста, введите логин и пароль в корректном формате.",
                         parse_mode='Markdown')
        return start(message)


if __name__ == '__main__':
    bot.infinity_polling()
