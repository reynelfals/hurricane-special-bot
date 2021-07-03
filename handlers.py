
import logging
import requests
import telegram
import config


def hurricane_map_command(update, context):
    logging.info(f'User {update.message.chat.first_name}, id {update.message.chat.id}, calling hurricane command')
    r = requests.get("https://www.nhc.noaa.gov/storm_graphics/AT05/refresh/AL052021_3day_cone_with_line_and_wind+png/", stream=True)
    if r.status_code == 200:
        bot = telegram.Bot(token=config.API_KEY)
        bot.send_photo(update.message.chat.id, r.raw)

        update.message.reply_text('The map ^')
    else:
        logging.error(f'Error in request code: {r.status_code}')


def help_command(update, context):
    logging.info(f'User {update.message.chat.first_name}, id {update.message.chat.id}, calling help command')
    update.message.reply_text('Use the commands /hurricane, /message.\nUse los comandos /huracan, /mensaje.')


def hurricane_map_command_sp(update, context):
    logging.info(f'User {update.message.chat.first_name}, id {update.message.chat.id}, calling huracan command')
    r = requests.get("https://www.nhc.noaa.gov/storm_graphics/AT05/refresh/AL052021_3day_cone_with_line_and_wind+png/",
                     stream=True)
    if r.status_code == 200:
        bot = telegram.Bot(token=config.API_KEY)
        bot.send_photo(update.message.chat.id, r.raw)

        update.message.reply_text('El mapa ^')
    else:
        logging.error(f'Error in request code: {r.status_code}')

def key_message(update, context):
    logging.info(f'User {update.message.chat.first_name}, id {update.message.chat.id}, calling message command')
    r = requests.get("https://www.nhc.noaa.gov/storm_graphics/AT05/refresh/AL052021_key_messages+png/", stream=True)
    if r.status_code == 200:
        bot = telegram.Bot(token=config.API_KEY)
        bot.send_photo(update.message.chat.id, r.raw)
        update.message.reply_text('Key Message ^')
    else:
        logging.error(f'Error in request code: {r.status_code}')


def key_message_sp(update, context):
    logging.info(f'User {update.message.chat.first_name}, id {update.message.chat.id}, calling mensaje command')
    r = requests.get("https://www.nhc.noaa.gov/storm_graphics/AT05/refresh/AL052021_spanish_key_messages+png/", stream=True)
    if r.status_code == 200:
        bot = telegram.Bot(token=config.API_KEY)
        bot.send_photo(update.message.chat.id, r.raw)
        update.message.reply_text('Mensaje clave ^')
    else:
        logging.error(f'Error in request code: {r.status_code}')


def error(update, context):
    logging.error(f'Update {update} with error {context.error}')
