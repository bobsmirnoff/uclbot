#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime
import os
import telebot
from get_matches import get_matches
from utils import pass_matches, add_to_db, update_names, delete_name

bot = telebot.TeleBot(os.getenv('UCL_BOT_KEY', ''))

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Добро пожаловать, эксперт! Ты подписался на уведомления о матчах Лиги Чемпионов.')

    add_to_db(message.chat.id, message.chat.username)

    update_names()

    today = datetime.today().strftime('%Y-%m-%d')
    matches = get_matches(today)
    pass_matches(bot, message.chat.id, matches)


@bot.message_handler(commands=['stop'])
def stop_message(message):
    bot.send_message(message.chat.id, 'Хорошо, больше не буду присылать тебе напоминания.')
    delete_name(message.chat.id)


@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, 'Ты можешь отписаться от уведомлений командой /stop или подписаться обратно командой /start')


bot.polling()

