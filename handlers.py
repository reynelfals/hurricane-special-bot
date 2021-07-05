from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from telegram.ext import *
import logging
import requests
import telegram
import config

command_keyboard = [
    [KeyboardButton('/hurricane'), KeyboardButton('/message')],
    [KeyboardButton('/satellite'), KeyboardButton('/animated')],
    [KeyboardButton('/help')]
]

command_keyboard_sp = [
    [KeyboardButton('/huracan'), KeyboardButton('/mensaje')],
    [KeyboardButton('/satellite'), KeyboardButton('/animated')],
    [KeyboardButton('/help')]
]

markup = ReplyKeyboardMarkup(command_keyboard, one_time_keyboard=True)
markup_sp = ReplyKeyboardMarkup(command_keyboard_sp, one_time_keyboard=True)


def hurricane_map_command(update, context):

    logging.info(f'User {update.message.chat.first_name}, id {update.message.chat.id}, calling hurricane command')
    r = requests.get("https://www.nhc.noaa.gov/storm_graphics/AT05/refresh/AL052021_3day_cone_with_line_and_wind+png/", stream=True)
    if r.status_code == 200:
        bot = telegram.Bot(token=config.API_KEY)
        bot.send_photo(update.message.chat.id, r.raw, reply_markup=markup)

        update.message.reply_text('The map ^', reply_markup=markup)
    else:
        logging.error(f'Error in request code: {r.status_code}')


def help_command(update, context):
    logging.info(f'User {update.message.chat.first_name}, id {update.message.chat.id}, calling help command')
    update.message.reply_text(text='Use the commands\n'
                              '`/hurricane` or `/huracan` \- For probability cone\.\n'
                              '`/satellite` or `/satellite low` \- For 500x500 pixels static satellite image\.\n'
                              '`/satellite high` \- For 1000x1000 pixels static satellite image\.\n'
                              '`/satellite gif` or `/animated` \- For 500x500 pixels satellite clip\.\n'
                              '`/message` or `/mensaje` \- For key message in an image\.\n', parse_mode="MarkdownV2", reply_markup=markup)


def hurricane_map_command_sp(update, context):
    logging.info(f'User {update.message.chat.first_name}, id {update.message.chat.id}, calling huracan command')
    r = requests.get("https://www.nhc.noaa.gov/storm_graphics/AT05/refresh/AL052021_3day_cone_with_line_and_wind+png/",
                     stream=True)
    if r.status_code == 200:
        bot = telegram.Bot(token=config.API_KEY)
        bot.send_photo(update.message.chat.id, r.raw, reply_markup=markup_sp)

        update.message.reply_text('El mapa ^', reply_markup=markup_sp)
    else:
        logging.error(f'Error in request code: {r.status_code}')

def key_message(update, context):
    logging.info(f'User {update.message.chat.first_name}, id {update.message.chat.id}, calling message command')
    r = requests.get("https://www.nhc.noaa.gov/storm_graphics/AT05/refresh/AL052021_key_messages+png/", stream=True)
    if r.status_code == 200:
        bot = telegram.Bot(token=config.API_KEY)
        bot.send_photo(update.message.chat.id, r.raw)
        update.message.reply_text('Key Message ^', reply_markup=markup)
    else:
        logging.error(f'Error in request code: {r.status_code}')


def key_message_sp(update, context):
    logging.info(f'User {update.message.chat.first_name}, id {update.message.chat.id}, calling mensaje command')
    bot = telegram.Bot(token=config.API_KEY)
    bot.send_photo(chat_id=update.message.chat.id,
                   photo="https://www.nhc.noaa.gov/storm_graphics/AT05/refresh/AL052021_spanish_key_messages+png/", reply_markup=markup_sp)
    update.message.reply_text('Mensaje clave ^', reply_markup=markup_sp)

#https://cdn.star.nesdis.noaa.gov/FLOATER/data/AL052021/GEOCOLOR/latest.jpg
#https://cdn.star.nesdis.noaa.gov/FLOATER/data/AL052021/GEOCOLOR/500x500.jpg

def satellite(update: Update, context: CallbackContext):
    logging.info(f'User {update.message.chat.first_name}, id {update.message.chat.id}, calling satellite command')
    modes={'low':"https://cdn.star.nesdis.noaa.gov/FLOATER/data/AL052021/GEOCOLOR/500x500.jpg",
           'high': "https://cdn.star.nesdis.noaa.gov/FLOATER/data/AL052021/GEOCOLOR/latest.jpg",
           'gif': "data/resized.gif"}
    mode = 'low'
    args = context.args
    if len(args)>0:
        mode = args[0]
    if mode == 'gif':
        return animated(update,context)

    url = modes.get(mode, 'low')

    r = requests.get(url, stream=True)

    if r.status_code == 200:
        context.bot.send_photo(update.message.chat.id, r.raw, reply_markup=markup)
        update.message.reply_text(f'Satellite {mode} resolution ^', reply_markup=markup)
    else:
        logging.error(f'Error in request code: {r.status_code}')

#https://cdn.star.nesdis.noaa.gov/FLOATER/data/AL052021/GEOCOLOR/GOES16-AL052021-GEOCOLOR-1000x1000.gif
def animated(update, context):
    logging.info(f'User {update.message.chat.first_name}, id {update.message.chat.id}, calling animated command')
    context.bot.send_document(chat_id=update.message.chat.id, document=open('./data/resized500_500.gif', 'rb'), reply_markup=markup)
    update.message.reply_text('Satellite Animation^', reply_markup=markup)


def error(update, context):
    logging.error(f'Update {update} with error {context.error}')
