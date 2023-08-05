from datetime import datetime
from json import load

from django.core.management.base import BaseCommand
from django.contrib.auth import authenticate, login
from django.db.models import Sum
from telebot import types
import telebot

from enterprise.models import Enterprise
from route.models import Route
from vehicle.models import Vehicle

with open("settings.json", "r") as settings_file:
    LOCAL_SETTINGS = load(settings_file)

try:
    token = LOCAL_SETTINGS['telegram_token']
except:
    raise Exception("Telegram bot token hasn't been provided!")

user_credentials = {}
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['debug'])
def show_debug(message):
    info = [
        str(user_credentials),
        message.chat.id
    ]
    bot.send_message(message.chat.id, str(info))


@bot.message_handler(commands=['start'])
def menu(message):
    print(user_credentials)
    if user_credentials.get(message.chat.id):
        bot.send_message(message.chat.id, 'Вы уже аутентифицированы.')
        bot.register_next_step_handler(message, manager_menu)
        return

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    login_button = types.KeyboardButton("Войти в систему")
    markup.add(login_button)
    bot.send_message(message.chat.id, 'Приветствую. Войдете в систему?', reply_markup=markup)


def manager_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Получить пробег по конкретной машине")
    button2 = types.KeyboardButton("Получить пробег машин предприятия")
    markup.add(button1, button2)
    bot.send_message(message.chat.id, 'Выберете жалаемое действие.', reply_markup=markup)


def get_car_mileage(message):
    if user_credentials.get(message.chat.id) is None:
        bot.send_message(message.chat.id, 'Вы не аутентифицированы.')
        menu(message)
        return

    format = "%d-%m-%Y"

    try:
        info = message.text.split()
        vehicle_id = int(info[0])

        try:
            vehicle = Vehicle.objects.get(id=vehicle_id)
        except:
            bot.send_message(message.chat.id, 'Автомобиля с таким ID нет.')
            manager_menu(message)
            return

        if not vehicle.enterprise.manager.filter(id=user_credentials[message.chat.id].id).exists():
            bot.send_message(message.chat.id, 'У Вас нет доступа этой компании, владеющей этим автомобилем.')
            manager_menu(message)
            return

        start_date = datetime.strptime(info[1], format)
        end_date = datetime.strptime(info[2], format)

        routes = Route.objects.filter(vehicle__id=vehicle_id)\
                              .filter(start__gte=start_date)\
                              .filter(end__lte=end_date)

        distance = routes.aggregate(Sum('distance'))['distance__sum'] or 0

        bot.send_message(message.chat.id, str(distance))
        manager_menu(message)
        return
    except:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button = types.KeyboardButton("Вернуться в меню менеджера")
        markup.add(button)
        bot.send_message(message.chat.id, 'Вы не соблюли формат.',
                         reply_markup=markup)
        return


def get_company_mileage(message):
    if user_credentials.get(message.chat.id) is None:
        bot.send_message(message.chat.id, 'Вы не аутентифицированы.')
        menu(message)
        return

    format = "%d-%m-%Y"

    try:
        info = message.text.split()
        company_id = int(info[0])

        try:
            company = Enterprise.objects.get(id=company_id)
        except:
            bot.send_message(message.chat.id, 'Компании с таким ID нет.')
            manager_menu(message)
            return

        if not company.manager.filter(id=user_credentials[message.chat.id].id).exists():
            bot.send_message(message.chat.id, 'У Вас нет доступа к этой компании.')
            manager_menu(message)
            return

        start_date = datetime.strptime(info[1], format)
        end_date = datetime.strptime(info[2], format)

        routes = Route.objects.filter(vehicle__enterprise=company) \
            .filter(start__gte=start_date) \
            .filter(end__lte=end_date)

        distance = routes.aggregate(Sum('distance'))['distance__sum'] or 0

        bot.send_message(message.chat.id, str(distance))
        manager_menu(message)
        return
    except:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button = types.KeyboardButton("Вернуться в меню менеджера")
        markup.add(button)
        bot.send_message(message.chat.id, 'Вы не соблюли формат.',
                         reply_markup=markup)
        return


@bot.message_handler(content_types=['text'])
def message_reply(message):
    if message.text == "Войти в систему":
        bot.register_next_step_handler(message, handle_credentials)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button = types.KeyboardButton("Вернуться")
        markup.add(button)

        bot.send_message(message.chat.id,
                         "Введите никнейм и пароль в формате 'username password'",
                         reply_markup=markup)
        return

    if message.text == "Получить пробег по конкретной машине":
        bot.send_message(message.chat.id,
                         "Укажите ID машины и диапазон дат в формате \"ID DD-MM-YYYY DD-MM-YYYY\"")
        bot.register_next_step_handler(message, get_car_mileage)
        return

    if message.text == "Получить пробег машин предприятия":
        bot.send_message(message.chat.id,
                         "Укажите ID компании и диапазон дат в формате \"ID DD-MM-YYYY DD-MM-YYYY\"")
        bot.register_next_step_handler(message, get_company_mileage)
        return

    if message.text == "Вернуться в меню менеджера":
        bot.register_next_step_handler(message, manager_menu)
        return


def handle_credentials(message):
    if message.text == "Вернуться":
        menu(message)
        return

    nick_pass = message.text

    try:
        nick_pass = nick_pass.split()
        assert len(nick_pass) == 2
        nickname = nick_pass[0]
        password = nick_pass[1]
    except:
        bot.send_message(message.chat.id, 'Вероятно, вы передали данные в неверном формате.' +
                         ' Попробуйте еще раз.')
        bot.register_next_step_handler(message, handle_credentials)
        return

    if nickname == 'Котичка' and password == "123":
        bot.send_message(message.chat.id, "Котичка милая, тебе поцелуй  😘")
        bot.send_message(message.chat.id, "Но все же логин или пароль не верны." +
                         " Попробуйте еще.")
        bot.register_next_step_handler(message, handle_credentials)
        return

    user = authenticate(username=nickname, password=password)

    if not user:
        bot.send_message(message.chat.id, "Неверный логин или пароль. Попробуйте еще раз.")
        bot.register_next_step_handler(message, handle_credentials)
        return

    user_credentials[message.chat.id] = user

    manager_menu(message)


class Command(BaseCommand):
    help = "Starts telegram bot"

    def handle(self, *args, **options):
        bot.infinity_polling()
