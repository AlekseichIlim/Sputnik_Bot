from datetime import datetime

import openpyxl
import telebot
from telebot import types

from DataMonth import DataMonthNow
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
    menu_1(message)


# @bot.message_handler()
def menu_1(message):

    bot.send_message(message.chat.id, "Какой месяц тебя интересует?", reply_markup=markup_1)
    bot.register_next_step_handler(message, on_click_1)


@bot.message_handler()
def on_click_1(message):
    if message.text == "Текущий месяц":
        data_month_now(message)
    elif message.text == "Прошедший месяц":
        data_month_previous(message)


################
# @bot.message_handler(func=lambda message: message.text == 'Текущий месяц')
# def data_month_now(message):
#
#     bot.send_message(message.from_user.id, "Какую информацию предоставить?", reply_markup=markup_2)


# @bot.message_handler(func=lambda message: message.text == 'Объем заготовки с начала месяца')
# @bot.message_handler(func=lambda message: message.text == 'Посуточная заготовка')
def data_month_now(message):
    bot.send_message(message.from_user.id, "...\U000023F3")

    obj = DataMonthNow(daily_report, report)
    data = obj.get_actual_volume()

    bot.send_message(message.from_user.id, "Какую информацию предоставить?", reply_markup=markup_2)
    bot.register_next_step_handler(message, data_beginning_month, data)


def data_beginning_month(message, data):

    # if message.text == "Объем заготовки с начала месяца":
    #     bot.send_message(message.from_user.id,
    #                  f"Данные на 20:00 {date_update}\nОбъем заготовки:{actual_volumes['actual']}/Объем по графику:{actual_volumes['plan']}")
    #     bot.register_next_step_handler(message, data_beginning_month, date_update, actual_volumes)
    # elif message.text == 'План на месяц':
    #     bot.send_message(message.from_user.id, f"План большой")
    #     bot.register_next_step_handler(message, data_beginning_month, date_update, actual_volumes)
    # elif message.text == 'Назад':
    #     menu_1()

    if message.text == "Объем заготовки с начала месяца":
        bot.send_message(message.from_user.id,
                     f"Данные на 20:00 {data['update_time']}\nОбъем заготовки:{data['actual']}/Объем по графику:{data['plan']}")
        deviation = data['actual'] - data['plan']
        if deviation > 0:
            bot.send_message(message.from_user.id, f'Перевыполнение {deviation} м³')
        else:
            bot.send_message(message.from_user.id, f'Отставание {abs(deviation)} м³')
        bot.register_next_step_handler(message, data_beginning_month, data)
    elif message.text == 'План на месяц':
        bot.send_message(message.from_user.id, f'{data['plan_month']} м³')
        bot.register_next_step_handler(message, data_beginning_month, data)
    elif message.text == 'Посуточная заготовка':
        bot.send_message(message.from_user.id, 'Данных нет')
        bot.register_next_step_handler(message, data_beginning_month, data)
    elif message.text == 'Посменная заготовка':
        bot.send_message(message.from_user.id, 'Данных нет')
        bot.register_next_step_handler(message, data_beginning_month, data)
    elif message.text == 'Назад':
        menu_1(message)


# @bot.message_handler(func=lambda message: message.text == 'Посуточная заготовка')
# def data_dys_now(message):
#     bot.send_message(message.from_user.id, "Суточная заготовка")
#
# @bot.message_handler(func=lambda message: message.text == 'Назад')
# def data_dys_now(message):
#     bot.register_next_step_handler(message, menu)

@bot.message_handler()
def data_month_previous(message):
    bot.send_message(message.from_user.id, 'Данных пока нет')
    menu_1(message)


bot.polling(none_stop=True)
