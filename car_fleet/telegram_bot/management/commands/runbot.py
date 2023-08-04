from django.core.management.base import BaseCommand
from django.contrib.auth import authenticate, login
from telebot import types
import telebot


token = '5642759020:AAGYvoH8emqBdbJYLGlJUo7jKFRZjsQI-aM'
user_credentials = {}
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def menu(message):
    if user_credentials.get(message.chat.id):
        bot.send_message(message.chat.id, 'Вы уже аутентифицированы.')

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    login_button = types.KeyboardButton("Войти в систему")
    markup.add(login_button)
    bot.send_message(message.chat.id, 'Приветствую. Войдете в систему?', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def message_reply(message):
    if message.text == "Войти в систему":
        markup = telebot.types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id,
                         "Введите никнейм и пароль в формате 'username password'",
                         reply_markup=markup)
        bot.register_next_step_handler(message, handle_credentials)


def handle_credentials(message):
    nick_pass = message.text

    try:
        nick_pass = nick_pass.split()
        assert len(nick_pass) == 2
        nickname = nick_pass[0]
        password = nick_pass[1]
    except:
        bot.send_message(message.chat.id, 'Вероятно, вы передали данные в не верном формате.' +
                         ' Попробуйте еще раз.')
        bot.register_next_step_handler(message, handle_credentials)
        return

    if nickname == 'Котичка' and password == "123":
        bot.send_message(message.chat.id, "Котик тебя поцеловал, котичка милая :-*")


    user = authenticate(username=nickname, password=password)

    user_credentials[message.chat.id] = user

    print(nickname, password)

    bot.send_message(message.chat.id, "На этом все. Пока!")

    menu(message)

class Command(BaseCommand):
    help = "Starts telegram bot"

    def handle(self, *args, **options):
        bot.infinity_polling()
