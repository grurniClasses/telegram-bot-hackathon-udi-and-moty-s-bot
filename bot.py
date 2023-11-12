import logging

from telegram import Update
from telegram.ext import (
    CommandHandler,
    CallbackContext,
    Updater, MessageHandler, Filters,
)

import bot_settings

from storage import Storage

db = Storage("shopping_cart")

WELCOME_TEXT = "Welcome to our bot!"

logging.basicConfig(
    format="[%(levelname)s %(asctime)s %(module)s:%(lineno)d] %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    logger.info(f"> Start chat #{chat_id}")
    context.bot.send_message(chat_id=chat_id, text=WELCOME_TEXT)

def on_text(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    msg = update.message.text
    logger.info(f"+ Got #{chat_id}: {msg!r}")
    doc = db.add_item(chat_id, msg)
    response = f"Added {msg!r}, cart has {len(doc['items'])}."
    context.bot.send_message(chat_id=chat_id, text=response)


my_bot = Updater(token=bot_settings.BOT_TOKEN, use_context=True)
my_bot.dispatcher.add_handler(CommandHandler("start", start))
my_bot.dispatcher.add_handler(MessageHandler(Filters.text, on_text))

logger.info("* Start polling...")
my_bot.start_polling()  # Starts polling in a background thread.
my_bot.idle()  # Wait until Ctrl+C is pressed
logger.info("* Bye!")
