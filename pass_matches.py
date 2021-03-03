#!/usr/bin/python
# -*- coding: utf-8 -*-
import telebot


def pass_matches(bot, _id, matches):
    if len(matches) > 0:
        print(matches)
        bot.send_message(_id,
            '\n'.join(['Сегодня будут сыграны матчи:', ''] + matches + ['[Делаем ставочки!](http://total.pipeinpipe.info//)']),
            parse_mode='MarkdownV2')
    else:
        bot.send_message(_id, 'Сегодня матчей не запланировано. Повторяем конспекты!')
