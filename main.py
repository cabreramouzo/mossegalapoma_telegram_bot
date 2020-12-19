import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import datetime
import logging
import os
import random
import requests
import json

INTERNAL_VERSION = '1.0.5'
G_CLOUD = True
''' If the bot is hosted in Google Cloud Function set this constant to True. If false
the bot will run using a busy waiting technique'''

bot = telegram.Bot(token=os.environ["TELEGRAM_TOKEN"])
tenor_api_key = os.environ["TENOR_API_KEY"]

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

def get_thanks_gif_url():
    # set the apikey and limit
    apikey = tenor_api_key
    lmt = 4

    # our test search
    search_term_list = ["cute cat", "kitty love", "love animal", "thank you", "cute animal", "love you" ]
    random_index_search_term = random.randint(0, len(search_term_list) -1)
    search_term = search_term_list[random_index_search_term]

    # get random results using default locale of EN_US
    r = requests.get("https://api.tenor.com/v1/search?q=%s&key=%s&limit=%s&media_filter=minimal" % (search_term, apikey, lmt))
    url='https://tenor.com/view/funny-animals-cat-love-cat-hug-gif-14233808'
    if r.status_code == 200:
        gifs = json.loads(r.content)
        #print (gifs)
        random_index = random.randint(0, len(gifs) -1)
        url = gifs['results'][random_index]['url']

    return url

def get_mandalorian_gif_url():
    # set the apikey and limit
    apikey = tenor_api_key
    lmt = 4

    # our test search
    search_term_list = ["baby yoda", "baby yoda happy", "mandalorian", "thisistheway"]
    random_index_search_term = random.randint(0, len(search_term_list) -1)
    search_term = search_term_list[random_index_search_term]

    # get random results using default locale of EN_US
    r = requests.get("https://api.tenor.com/v1/search?q=%s&key=%s&limit=%s&media_filter=minimal" % (search_term, apikey, lmt))
    url='https://tenor.com/view/baby-yoda-baby-yoda-happy-laughing-smile-happy-gif-16061896'
    if r.status_code == 200:
        gifs = json.loads(r.content)
        #print (gifs)
        random_index = random.randint(0, len(gifs) -1)
        url = gifs['results'][random_index]['url']

    return url

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
        palasaca = [
            '#palasaca','#amazon', '#palasaka', '#afiliats', 'compra per afiliats', 'compra feta per afiliats'
        ]

        this_is_the_way = ['#thisistheway', '#thiswastheway', '#aquesteselcami', '#this_is_the_way', '#aquest_es_el_cami']

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
        weary_face = u'\U0001F629'
        face_blowing_a_kiss = u'\U0001F618'
        gust_of_wind = u'\U0001F4A8'
        fire = u'\U0001F525'
        water_faucet = u'\U0001F6B0'
        money_bag = u'\U0001F4B0'

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

        text_reply_palasaca = [
            f"En @tomasmanz i tot l'equip de Mossegalapoma t'estem molt agraïts! {face_blowing_a_kiss}",f"Disfruta-ho i moltes gràcies! {grinning_face_smiling_eyes} ",
            f"Gràcies! Cada dia estem més aprop del Tesla Model S... {face_tongue}", f"La targeta fot fum!!! {fire}{gust_of_wind}",
            f"De mica en mica s'omple la pica! {water_faucet}{money_bag}"
        ]

        text_rich_reply_proposal = [
            f"Tota la raó, és del milloret que he vist últimament a Netflix.",
            f"A Netflix oi? La vaig veure ahir vespre! {winking_face}",
            f"Ah, pensava que era d'HBO aquesta...{thinking_face}",
            f"Netflix té merda per un tub, però també de bones i aquesta n'és una {face_tongue}",
            f"Llàstima que em vaig passar a Disney+ fa temps {sun_glasses}",
            f"Vaja! Ara que he cancel·lat la subscripció la dius... {expression_less}",
            f"Enganxa eh!? {face_tongue}",
            f"Va, que no tot és Netflix en aquesta vida! {grinning_face_smiling_eyes}",
            f"Podeu deixar de recomanar pelis i sèries a Netflix?! No hi ha qui pugui compilar! {weary_face}",
        ]

        if user_name != "":
            text_reply_proposal.append(f"Saps @{user_name}, jo també ho anava a proposar... {grinning_face_smiling_eyes}")
            text_reply_proposal.append(f"A veure, @{user_name}. Aquesta és bona {winking_face}")

            text_reply_palasaca.append(f"@{user_name}, seguim endavant gràcies a tu {face_blowing_a_kiss}")
            text_reply_palasaca.append(f"@{user_name}, sense tu això no seria possible {face_blowing_a_kiss}")
            text_reply_palasaca.append(f"@{user_name}, necessitem mosseguis com tu per tirar això endavant. Merci! {grinning_face_smiling_eyes}")
            text_reply_palasaca.append(f"Quan tinguem el Tesla, @{user_name} seràs dels primers a provar-lo! {sun_glasses} Paraula de Bot {robot}")
            text_reply_palasaca.append(f"@{user_name}, saps que en @tomasmanz t'estima molt, oi? Jo en canvi... és complicat. {robot}")

        #Add rich response if there is 'serie' or 'sèrie' or 'Netflix' in the message
        #message_keywords = ['netflix', 'sèrie', 'serie', 'peli']
        is_rich_response = False
        message_keywords = ['netflix', 'nètflix']
        if any( keyword for keyword in message_keywords if keyword in user_text.lower() ):
            is_rich_response = True
            
        text_reply_errata = [
            "Una altra vegada!?","Deixa'm apostar: Ha estat en Ludo ¬¬",
            "Sort en tenim de vosaltres!", "Una altra!? Anoto la fe d'errates!"
        ]
        
        random_troll_text_index = random.randint(0, len(text_troll_reply) -1 )
        random_rich_proposal_text_index = random.randint(0, len(text_rich_reply_proposal) -1 )
        random_proposal_text_index = random.randint(0, len(text_reply_proposal) -1 )
        random_errata_text_index = random.randint(0, len(text_reply_errata) -1 )
        random_palasaca_text_index = random.randint(0, len(text_reply_palasaca) -1 )

        text_troll = text_troll_reply[random_troll_text_index]

        if is_rich_response:
            text_proposal = text_rich_reply_proposal[random_rich_proposal_text_index]
        else:
            text_proposal = text_reply_proposal[random_proposal_text_index]
        
        text_errata = text_reply_errata[random_errata_text_index]

        text_palasaca = text_reply_palasaca[random_palasaca_text_index]

        if any(hashtag for hashtag in hashtags if hashtag in user_text.lower()):

            if len(user_text) < 20:
                bot.send_message(chat_id=update.effective_chat.id, reply_to_message_id=update.effective_message.message_id, text=text_troll)
            else:
                bot.send_message(chat_id=update.effective_chat.id, reply_to_message_id=update.effective_message.message_id, text=text_proposal)
                bot.send_message(chat_id=-291751171, text=user_name + "("+ user_first_name + " " + user_last_name + "): " + user_text)

        if any(hashtag for hashtag in federrates if hashtag in user_text.lower()):
            bot.send_message(chat_id=update.effective_chat.id, reply_to_message_id=update.effective_message.message_id, text=text_errata)
            bot.send_message(chat_id=-291751171, text=user_name + "("+ user_first_name + " " + user_last_name + "): " + user_text)

        #afiliats
        if any(hashtag for hashtag in palasaca if hashtag in user_text.lower()):
            random_number = random.randint(0,10)
            if random_number%2 == 0:
                bot.send_message(chat_id=update.effective_chat.id, reply_to_message_id=update.effective_message.message_id, text=text_palasaca)
            else:
                url = get_thanks_gif_url()
                bot.send_animation(chat_id=update.effective_chat.id, reply_to_message_id=update.effective_message.message_id, animation=url)

        #mandalorian
        if any(hashtag for hashtag in this_is_the_way if hashtag in user_text.lower()):
            url = get_mandalorian_gif_url()
            bot.send_animation(chat_id=update.effective_chat.id, reply_to_message_id=update.effective_message.message_id, animation=url)

#based in https://github.com/python-telegram-bot/python-telegram-bot/wiki/Webhooks
def webhook(request):
    bot = telegram.Bot(token=os.environ["TELEGRAM_TOKEN"])
    if request.method == 'POST':
        update = telegram.Update.de_json(request.get_json(force=True), bot)

        filter_hashtag_messages(update, bot)
    return 'ok'

updater = Updater(token=os.environ["TELEGRAM_TOKEN"], use_context=True)
job_queue = updater.job_queue

thuesday_at_14 = datetime.time(hour=16, minute=0, second=0)
job_thuesday = job_queue.run_daily(message_for_thuesday, time=thuesday_at_14, days= (1,))
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