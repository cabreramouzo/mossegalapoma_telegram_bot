from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import datetime
import logging


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

# defineix una funció que saluda i que s'executarà quan el bot rebi el missatge /start
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hola! Soc un bot bàsic per a mossegalapoma!.")

def help(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Soc un bot amb comandes /start, /help i /hora.")


def hora(update, context):
    missatge = str(datetime.datetime.now())
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=missatge)

def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Perdona però no entenc aquesta comanda TT.")

def filter_hashtag_messages(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="per aqui he vist un hastag")
    #user text
    print(update.message.text)

def echo_all_messages(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

TOKEN = open("token.txt").read().strip()

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('help', help))
dispatcher.add_handler(CommandHandler('hora', hora))

unknown_handler = MessageHandler(Filters.command, unknown)
dispatcher.add_handler(unknown_handler)

#echo all messages
#echo_handler = MessageHandler(Filters.text & (~Filters.command), echo_all_messages)
#dispatcher.add_handler(echo_handler)

dispatcher.add_handler(MessageHandler(Filters.entity("hashtag"), filter_hashtag_messages))

updater.start_polling()