from datetime import datetime
import os
import telebot
from utils import pass_matches
from get_matches import get_matches

today = datetime.today().strftime('%Y-%m-%d')
print("Today is " + today)

matches = get_matches(today)
print("Todays matches passed: " + str(matches))

bot = telebot.TeleBot(os.getenv('UCL_BOT_KEY', ''))

if len(matches) > 0:
    _id = os.getenv('PERSONAL_TELEGRAM_ID', -1)
    pass_matches(bot, _id, matches)
