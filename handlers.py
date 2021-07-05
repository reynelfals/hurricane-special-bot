from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from telegram.ext import *
import logging
import requests
import telegram
import config

command_keyboard = [
    [KeyboardButton('/animatedlite'),  KeyboardButton('/animated')],
    [KeyboardButton('/satellite'), KeyboardButton('/hurricane')],
    [KeyboardButton('/message'), KeyboardButton('/help')]
]

command_keyboard_sp = [
    [ KeyboardButton('/animatedlite'),  KeyboardButton('/animated')],
    [KeyboardButton('/satellite'), KeyboardButton('/huracan')],
    [KeyboardButton('/mensaje'), KeyboardButton('/help')]
]

markup = ReplyKeyboardMarkup(command_keyboard, one_time_keyboard=True)
markup_sp = ReplyKeyboardMarkup(command_keyboard_sp, one_time_keyboard=True)

def start(update, context):
    logging.info(f'User {update.message.chat.first_name}, id {update.message.chat.id}, calling start command')
    update.message.reply_text(text='**Welcome Friend**\n'
                                   'I can help you to track hurricanes, mainly at the **Caribbean Sea**\n\n'
                                   
                                   'Here, the list of commands:\n\n'
                                   
                                   '`/animated` or `/satellite gif`     \- 500x500 pixels satellite clip\.\n\n'
                                   
                                   '`/animatedlite` or `/satellite lite`     \- 500x500 pixels gray satellite clip, lightweight\.\n\n'
                                   
                                   '`/hurricane` or `/huracan`          \- Probability cone\.\n\n'
                                   
                                   '`/satellite` or `/satellite low`    \- Low resolution satellite image\.\n\n'
                                   
                                   '`/satellite high`                   \- High resolution satellite image\.\n\n'
                                   
                                   '`/message` or `/mensaje` \(espagnol\) \- Key message\.\n'
                                    
                                    '`/help` \- Helpful to see the list of commands\.',
                              parse_mode="MarkdownV2", reply_markup=markup)


def hurricane_map_command(update, context):

    logging.info(f'User {update.message.chat.first_name}, id {update.message.chat.id}, calling hurricane command')
    r = requests.get("https://www.nhc.noaa.gov/storm_graphics/AT05/refresh/AL052021_3day_cone_with_line_and_wind+png/", stream=True)
    if r.status_code == 200:
        context.bot.send_photo(update.message.chat.id, r.raw, reply_markup=markup)

        update.message.reply_text('The map ^. Maybe you want to check /satellite also.', reply_markup=markup)
    else:
        logging.error(f'Error in request code: {r.status_code}')


def help_command(update, context):
    logging.info(f'User {update.message.chat.first_name}, id {update.message.chat.id}, calling help command')
    update.message.reply_text(text='Use the commands\n'
                              '`/animated` or `/satellite gif` \- Satellite Clip\.\n'
                              '`/animatedlite` or `/satellite lite` \- Gray Satellite Clip lightweight\.\n'
                              '`/hurricane` or `/huracan` \- Probability Cone\.\n'
                              '`/satellite` or `/satellite low` \- 500x500 Satellite Image\.\n'
                              '`/satellite high` \- 1000x1000 Satellite Image\.\n'
                              '`/message` or `/mensaje` \- Key message\.\n', parse_mode="MarkdownV2", reply_markup=markup)


def hurricane_map_command_sp(update, context):
    logging.info(f'User {update.message.chat.first_name}, id {update.message.chat.id}, calling huracan command')
    r = requests.get("https://www.nhc.noaa.gov/storm_graphics/AT05/refresh/AL052021_3day_cone_with_line_and_wind+png/",
                     stream=True)
    if r.status_code == 200:
        context.bot.send_photo(update.message.chat.id, r.raw, reply_markup=markup_sp)

        update.message.reply_text('El mapa ^. Quizas quiera chequear /satellite', reply_markup=markup_sp)
    else:
        logging.error(f'Error in request code: {r.status_code}')

def key_message(update, context):
    logging.info(f'User {update.message.chat.first_name}, id {update.message.chat.id}, calling message command')
    r = requests.get("https://www.nhc.noaa.gov/storm_graphics/AT05/refresh/AL052021_key_messages+png/", stream=True)
    if r.status_code == 200:
        context.bot.send_photo(update.message.chat.id, r.raw)
        update.message.reply_text('Key Message ^ (Para espagnol /mensaje)', reply_markup=markup)
    else:
        logging.error(f'Error in request code: {r.status_code}')


def key_message_sp(update, context):
    logging.info(f'User {update.message.chat.first_name}, id {update.message.chat.id}, calling mensaje command')
    context.bot.send_photo(chat_id=update.message.chat.id,
                   photo="https://www.nhc.noaa.gov/storm_graphics/AT05/refresh/AL052021_spanish_key_messages+png/", reply_markup=markup_sp)
    update.message.reply_text('Mensaje clave ^ (For english /message)', reply_markup=markup_sp)

#https://cdn.star.nesdis.noaa.gov/FLOATER/data/AL052021/GEOCOLOR/latest.jpg
#https://cdn.star.nesdis.noaa.gov/FLOATER/data/AL052021/GEOCOLOR/500x500.jpg

def satellite(update: Update, context: CallbackContext):

    modes={'low':"https://cdn.star.nesdis.noaa.gov/FLOATER/data/AL052021/GEOCOLOR/500x500.jpg",
           'high': "https://cdn.star.nesdis.noaa.gov/FLOATER/data/AL052021/GEOCOLOR/latest.jpg",
           'gif': "data/resized.gif",
           'lite': "data/resized_gray.gif"}
    mode = 'low'
    args = context.args
    if len(args)>0:
        mode = args[0]
    if mode == 'gif':
        return animated(update,context)
    if mode == 'lite':
        return animatedlite(update,context)

    logging.info(f'User {update.message.chat.first_name}, id {update.message.chat.id}, calling satellite {mode} command')

    url = modes.get(mode, 'low')

    r = requests.get(url, stream=True)

    if r.status_code == 200:
        context.bot.send_photo(update.message.chat.id, r.raw, reply_markup=markup)
        update.message.reply_text(f'Satellite {mode} resolution ^ (Change resolution using arguments: /satellite low or /satellite high)', reply_markup=markup)
    else:
        logging.error(f'Error in request code: {r.status_code}')

#https://cdn.star.nesdis.noaa.gov/FLOATER/data/AL052021/GEOCOLOR/GOES16-AL052021-GEOCOLOR-1000x1000.gif
def animated(update, context):
    logging.info(f'User {update.message.chat.first_name}, id {update.message.chat.id}, calling animated command')
    context.bot.send_document(chat_id=update.message.chat.id, document=open('./data/resized500_500.gif', 'rb'), reply_markup=markup)
    update.message.reply_text('Satellite Animation^. For a lightweight alternative use /animatedlite', reply_markup=markup)

def animatedlite(update, context):
    logging.info(f'User {update.message.chat.first_name}, id {update.message.chat.id}, calling animatedlite command')
    context.bot.send_document(chat_id=update.message.chat.id, document=open('./data/resized500_500_gray.gif', 'rb'), reply_markup=markup)
    update.message.reply_text('Satellite Animation Gray Scale^. Check /animated for a colored version.', reply_markup=markup)

def error(update, context):
    logging.error(f'Update {update} with error {context.error}')
