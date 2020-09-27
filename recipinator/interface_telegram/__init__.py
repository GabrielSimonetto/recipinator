import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from recipinator.interface_telegram.config import TOKEN
from recipinator.interface_telegram.commands import HANDLERS

logging.basicConfig()

def run():
    updater = Updater(TOKEN)

    handlers = HANDLERS

    for h in handlers:
        updater.dispatcher.add_handler(h)

    updater.start_polling()
    updater.idle()
