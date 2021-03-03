#!/usr/bin/python
# -*- coding: utf-8 -*-
import telebot


def pass_matches(bot, _id, matches):
    if len(matches) > 0:
        print(matches)
        bot.send_message(_id,
            '\n'.join(['Сегодня будут сыграны матчи:', ''] + matches + ['[Делаем ставочки\!](http://total.pipeinpipe.info//)']),
            parse_mode='MarkdownV2')
    else:
        bot.send_message(_id, 'Сегодня матчей не запланировано. Повторяем конспекты!')


def add_to_db(_id, username):
    name = str(_id) + "\t" + username if username else str(_id) + "\t _no_name_"
    print(name + " joined")
    f = open('chats.txt', 'a')
    f.write(name + '\n')
    f.close()


def update_names():
    chat_ids = set()
    f = open('chats.txt', 'r')
    for line in f:
        chat_ids.add(line)
    f.close()
    f = open('chats.txt', 'w')
    for _id in chat_ids:
         f.write(str(_id))
    f.close()


def delete_name(_id):
    chat_ids = set()
    f = open('chats.txt', 'r')
    for line in f:
        if line.split("\t")[0] != str(_id):
            chat_ids.add(line)
        else:
            print(line + " left")
    f.close()
    f = open('chats.txt', 'w')
    for _id in chat_ids:
         f.write(str(_id))
    f.close()

