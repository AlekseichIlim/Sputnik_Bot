from datetime import datetime

import openpyxl
import telebot
from telebot import types

from config import TELEGRAM_TOKEN, daily_report, report
from functions import get_name_month_now, get_paths_to_file, get_count_day_month, get_plan_volume, get_actual_volume, \
    get_date_update_file

bot = telebot.TeleBot(TELEGRAM_TOKEN)

markup_1 = types.ReplyKeyboardMarkup()
btn1_1 = types.KeyboardButton(text="Текущий месяц")
btn1_2 = types.KeyboardButton(text="Прошедший месяц")
markup_1.row(btn1_1, btn1_2)

markup_2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn2_1 = types.KeyboardButton(text="План на месяц")
btn2_2 = types.KeyboardButton(text="Объем заготовки с начала месяца")
btn2_3 = types.KeyboardButton(text="Посуточная заготовка")
btn2_4 = types.KeyboardButton(text="Посменная заготовка")
btn2_5 = types.KeyboardButton(text="Назад")
markup_2.add(btn2_1, btn2_2)
markup_2.add(btn2_3, btn2_4)
markup_2.add(btn2_5)


@bot.message_handler(commands=['start'])
def start(message):

    bot.send_message(message.chat.id,
                     f"Привет, {message.from_user.first_name}! Этот бот предоставляет информацию о заготовке бригады Спутник-1 \U0001F916"
                     )

    # bot.send_message(message.chat.id, "Какой месяц тебя интересует?", reply_markup=markup_1)
    # bot.register_next_step_handler(message, on_click_1)
    # bot.register_next_step_handler(message, menu_1)
    print(message.text)
    menu_1(message)


# @bot.message_handler()
def menu_1(message):

    bot.send_message(message.chat.id, "Какой месяц тебя интересует?", reply_markup=markup_1)
    bot.register_next_step_handler(message, on_click_1)
    # on_click_1(message)
    print(message.text)


@bot.message_handler()
def on_click_1(message):
    print(message.text)
    if message.text == "Текущий месяц":
        # bot.register_next_step_handler(message, data_month_now)
        data_month_now(message)
    elif message.text == "Прошедший месяц":
        bot.register_next_step_handler(message, data_month_previous)

# def on_click_1(message):
#     if message.text == "Текущий месяц":
#         data_month_now(message)
#     elif message.text == "Прошедший месяц":
#         data_month_previous(message)


################
# @bot.message_handler(func=lambda message: message.text == 'Текущий месяц')
# def data_month_now(message):
#
#     bot.send_message(message.from_user.id, "Какую информацию предоставить?", reply_markup=markup_2)


# @bot.message_handler(func=lambda message: message.text == 'Объем заготовки с начала месяца')
# @bot.message_handler(func=lambda message: message.text == 'Посуточная заготовка')
def data_month_now(message):
    bot.send_message(message.from_user.id, "...\U000023F3")

    month = datetime.now().month
    count_days = get_count_day_month(month)
    name_month = get_name_month_now(month)
    paths = get_paths_to_file(name_month, daily_report, report)
    data_daily_file = openpyxl.load_workbook(paths['daily_report'], data_only=True)
    date_update = get_date_update_file(paths['report'])
    plan_volume = get_plan_volume(data_daily_file, count_days)
    actual_volumes = get_actual_volume(data_daily_file, paths['report'])

    bot.send_message(message.from_user.id, "Какую информацию предоставить?", reply_markup=markup_2)
    bot.register_next_step_handler(message, data_beginning_month, date_update, actual_volumes)
    print(message.text)


def data_beginning_month(message, date_update, actual_volumes):
    print(message.text)
    if message.text == "Объем заготовки с начала месяца":
        bot.send_message(message.from_user.id,
                     f"Данные на 20:00 {date_update}\nОбъем заготовки:{actual_volumes['actual']}/Объем по графику:{actual_volumes['plan']}")
        bot.register_next_step_handler(message, data_beginning_month, date_update, actual_volumes)
    elif message.text == 'План на месяц':
        bot.send_message(message.from_user.id, f"План большой")
        bot.register_next_step_handler(message, data_beginning_month, date_update, actual_volumes)
    elif message.text == 'Назад':
        menu_1()



# @bot.message_handler(func=lambda message: message.text == 'Посуточная заготовка')
# def data_dys_now(message):
#     bot.send_message(message.from_user.id, "Суточная заготовка")
#
# @bot.message_handler(func=lambda message: message.text == 'Назад')
# def data_dys_now(message):
#     bot.register_next_step_handler(message, menu)

@bot.message_handler()
def data_month_previous(message):
    pass
# @bot.message_handler(content_types=['text'])
# def after_text_2(message):
#
#     bot.send_message(message.from_user.id,
#                      "Введите сложность из предложенных вариантов:")
#     bot.send_message(message.chat.id, f'Сложность:{get_rating_list(session)}')
#     theme = message.text.lower()
#     bot.register_next_step_handler(message, compilation, theme)


# @bot.message_handler()
# def compilation(message, theme):
#
#     if message.text.isdigit() is False:
#         bot.send_message(message.chat.id, "Проверьте введенные данные")
#         after_text_1(message)
#
#     else:
#         rating = int(message.text)
#         bot.send_message(message.chat.id, "Получение подборки...")
#         problems = get_compilation_problems(session, theme, rating)
#         count = len(problems)
#         num = 0
#         if count != 0:
#             if count < 10:
#                 bot.send_message(message.chat.id, f"Всего найдено задач по данному запросу: {count}")
#             for i in problems:
#                 markup_2 = types.InlineKeyboardMarkup()
#                 markup_2.add(types.InlineKeyboardButton('Перейти к задаче:',
#                                                         url=f'https://codeforces.com/problemset/problem/{i.contest_id}/{i.index}'))
#                 num += 1
#                 bot.send_message(message.chat.id, f'{num}# {str(i)}', reply_markup=markup_2)
#             bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)
#         else:
#             bot.send_message(message.chat.id, f"По вашему запросу ничего не найдено.")
#             after_text_1(message)
#         bot.register_next_step_handler(message, on_click)


bot.polling(none_stop=True)
