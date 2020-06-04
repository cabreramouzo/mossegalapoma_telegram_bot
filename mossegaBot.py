from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import datetime
import logging
from communication import get_updates_json, send_message, reply_message



logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

# defineix una funció que saluda i que s'executarà quan el bot rebi el missatge /start
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hola! Sóc un bot bàsic per a mossegalapoma!.")

def help(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Sóc un bot amb comandes /start, /help i /hora.")


def hora(update, context):
    missatge = str(datetime.datetime.now())
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=missatge)

def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, reply_to_message_id=update.message.message_id, text="Perdona però no entenc aquesta comanda 🤨")

def filter_hashtag_messages(update, context):
    #user text
    user_text = update.message.text
    telegram_user = update.message.from_user
    user_name = ""
    user_first_name = "sense_nom"
    user_last_name = ""

    if telegram_user.username:
        user_name = telegram_user.username
    if telegram_user.first_name:
        user_first_name = telegram_user.first_name
    if telegram_user.last_name:
        user_last_name = telegram_user.last_name
    

    #filter #propostamossegui or #proposta or #propostesmossegui or #propostamosseguis text messages
    hashtags = ['#propostamossegui','#proposta','#propostesmossegui','#propostamosseguis', 'proposta', 'propostes']

    if any(hashtag for hashtag in hashtags if hashtag in user_text):
        context.bot.send_message(chat_id=update.effective_chat.id, reply_to_message_id=update.message.message_id, text="Anoto la proposta!")
        context.bot.send_message(chat_id=-291751171, text=user_name + "("+ user_first_name + " " + user_last_name + "): " + user_text)

TOKEN = open("token.txt").read().strip()

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('help', help))
dispatcher.add_handler(CommandHandler('hora', hora))

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

dispatcher.add_handler(MessageHandler(Filters.entity("hashtag"), filter_hashtag_messages))

updater.start_polling()


def main():
    