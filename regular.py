from datetime import datetime
import os
import telebot
from utils import pass_matches
from get_matches import get_matches

today = datetime.today().strftime('%Y-%m-%d')
print("Today is " + today)

matches = get_matches(today)
print("Todays matches passed: " + str(matches))

bot = telebot.TeleBot(os.getenv('UCL_BOT_KEY', '')

if len(matches) > 0:
    f = open('chats.txt', 'r')
    for line in f:
        print("Passing matches to " + line)
        try:
            _id = int(line.split('\t')[0])
            pass_matches(bot, _id, matches)
        except ValueError:
            pass
    f.close()

