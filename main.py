import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import datetime
import logging
import os
import random

G_CLOUD = True
''' If the bot is hosted in Google Cloud Function set this constant to True. If false
the bot will run using a busy waiting technique'''

bot = telegram.Bot(token=os.environ["TELEGRAM_TOKEN"])

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

def message_for_thuesday(context: telegram.ext.CallbackContext):
    context.bot.send_message(chat_id=-291751171, 
                            text="*Propostes d'aquesta setmana*:", 
                            parse_mode=telegram.ParseMode.MARKDOWN_V2)
                            

# defineix una funció que saluda i que s'executarà quan el bot rebi el missatge /start
def start(update, bot):
    bot.send_message(chat_id=update.effective_chat.id, text="Hola! Sóc un bot bàsic per a mossegalapoma!.")

def help(update, bot):
    bot.send_message(
        chat_id=update.effective_chat.id,
        text="Sóc un bot amb comandes /start, /help i /hora.")


def hora(update, bot):
    missatge = str(datetime.datetime.now())
    bot.send_message(
        chat_id=update.effective_chat.id,
        text=missatge)

def unknown(update, bot):
    bot.send_message(chat_id=update.effective_chat.id, reply_to_message_id=update.message.message_id, text="Perdona però no entenc aquesta comanda 🤨")

def filter_hashtag_messages(update, bot):
    #user text
    if update is not None and update.effective_message.text is not None:
        user_text = update.effective_message.text
        telegram_user = update.effective_message.from_user
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
        hashtags = [
            '#propostamossegui','#proposta','#propostesmossegui', '#propostesmosseguis',
            '#propostamosseguis', '#propostamosegui', '#propostamoseguis', '#propostesmosegui',
            '#propostesmoseguis'
        ]
        federrates = [
            '#federrates','#federrades',
            '#federates', "fe d'errates"
        ]

        # Emoji unicode codes
        rocket = u'\U0001f680'
        closed_mailbox = u'\U0001F4EB'
        postbox = u'\U0001F4EE'
        paperclip = u'\U0001F4CE'
        biceps = u'\U0001F4AA'
        grinning_face_smiling_eyes = u'\U0001F601'
        winking_face = u'\U0001F609'
        robot = u'\U0001F916'
        right_arrow = u'\U000027A1'
        writing_hand = u'\U0000270D'
        robot_arm = u'\U0001F9BE'
        thinking_face = u'\U0001F914'
        clap_hands = u'\U0001F44F'
        sun_glasses = u'\U0001F60E'
        face_tongue = u'\U0001F61C'
        unamused_face = u'\U0001F612'
        tongue_out = u'\U0001F61D'
        expression_less = u'\U0001F611'
        siren = u'\U0001F6A8'

        text_troll_reply = [
            f"Això no té pinta de proposta... {unamused_face}", f"Ets un troll!!! {tongue_out}",
            f"Ho tens clar! {expression_less}", f"Alerta...TROLL!!! {siren}{siren}{siren}"
        ]

        text_reply_proposal = [
            f"Anoto la proposta! {biceps}",f"Proposta anotada {winking_face}", f"Els hi anoto la proposta {grinning_face_smiling_eyes}", 
            f"L'apunto! {closed_mailbox}", f"Els la deixo al guió {postbox}", f"Apuntada! {paperclip}", f"Proposta que no s'escapa! {robot}{right_arrow}{writing_hand}",
            f"Viatjant cap al guió... {rocket}", f"Clar que sí! {robot} {robot_arm}", f"Vols dir que no la vas dir fa un temps? {thinking_face}", 
            f"Aquesta sí que és bona! {clap_hands}{clap_hands}{clap_hands}", f"Vamos allá, ¿No? {sun_glasses}", f"Fot-li! {face_tongue}"
        ]

        text_reply_errata = [
            "Una altra vegada!?","Deixa'm apostar: Ha estat en Ludo ¬¬",
            "Sort en tenim de vosaltres!", "Una altra!? Anoto la fe d'errates!"
        ]
        
        random_troll_text_index = random.randint(0, len(text_troll_reply) -1 )
        random_proposal_text_index = random.randint(0, len(text_reply_proposal) -1 )
        random_errata_text_index = random.randint(0, len(text_reply_errata) -1 )

        text_troll = text_troll_reply[random_troll_text_index]
        text_proposal = text_reply_proposal[random_proposal_text_index]
        text_errata = text_reply_errata[random_errata_text_index]

        if any(hashtag for hashtag in hashtags if hashtag in user_text.lower()):

            if len(user_text) < 35:
                bot.send_message(chat_id=update.effective_chat.id, reply_to_message_id=update.effective_message.message_id, text=text_troll)
            else:

                bot.send_message(chat_id=update.effective_chat.id, reply_to_message_id=update.effective_message.message_id, text=text_proposal)
                bot.send_message(chat_id=-291751171, text=user_name + "("+ user_first_name + " " + user_last_name + "): " + user_text)

        if any(hashtag for hashtag in federrates if hashtag in user_text.lower()):
            bot.send_message(chat_id=update.effective_chat.id, reply_to_message_id=update.effective_message.message_id, text=text_errata)
            bot.send_message(chat_id=-291751171, text=user_name + "("+ user_first_name + " " + user_last_name + "): " + user_text)


#based in https://github.com/python-telegram-bot/python-telegram-bot/wiki/Webhooks
def webhook(request):
    bot = telegram.Bot(token=os.environ["TELEGRAM_TOKEN"])
    if request.method == 'POST':
        update = telegram.Update.de_json(request.get_json(force=True), bot)

        filter_hashtag_messages(update, bot)
    return 'ok'

updater = Updater(token=os.environ["TELEGRAM_TOKEN"], use_context=True)
job_queue = updater.job_queue

thuesday_at_14 = datetime.time(hour=14, minute=0, second=0) #hour is in UTC
job_thuesday = job_queue.run_daily(message_for_thuesday, time=thuesday_at_14, days= (2,)) #Wednesday
job_queue.start()

if not G_CLOUD:
    dispatcher = updater.dispatcher

    #dispatcher.add_handler(CommandHandler('start', start))
    #dispatcher.add_handler(CommandHandler('help', help))
    #dispatcher.add_handler(CommandHandler('hora', hora))

    unknown_handler = MessageHandler(Filters.command, unknown)
    dispatcher.add_handler(unknown_handler)

    dispatcher.add_handler(MessageHandler(Filters.entity("hashtag"), filter_hashtag_messages))

    updater.start_polling()