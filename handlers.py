
import logging
import requests
import telegram
import config


def start_command(update, context):
    r = requests.get("https://www.nhc.noaa.gov/storm_graphics/AT05/refresh/AL052021_3day_cone_with_line_and_wind+png/", stream=True)
    if r.status_code == 200:
        bot = telegram.Bot(token=config.API_KEY)
        bot.send_photo(update.message.chat.id, r.raw)

        update.message.reply_text('The map ^')


def help_command(update, context):
    update.message.reply_text('Use the commands /hurricane, /message.\nUse los comandos /huracan, /mensaje.')


def custom_command(update, context):
    r = requests.get("https://www.nhc.noaa.gov/storm_graphics/AT05/refresh/AL052021_3day_cone_with_line_and_wind+png/",
                     stream=True)
    if r.status_code == 200:
        bot = telegram.Bot(token=config.API_KEY)
        bot.send_photo(update.message.chat.id, r.raw)

        update.message.reply_text('El mapa ^')

def key_message(update, context):
    r = requests.get("https://www.nhc.noaa.gov/storm_graphics/AT05/refresh/AL052021_key_messages+png/", stream=True)
    if r.status_code == 200:
        bot = telegram.Bot(token=config.API_KEY)
        bot.send_photo(update.message.chat.id, r.raw)
        update.message.reply_text('Key Message ^')


def key_message_sp(update, context):
    r = requests.get("https://www.nhc.noaa.gov/storm_graphics/AT05/refresh/AL052021_spanish_key_messages+png/", stream=True)
    if r.status_code == 200:
        bot = telegram.Bot(token=config.API_KEY)
        bot.send_photo(update.message.chat.id, r.raw)
        update.message.reply_text('Mensaje clave ^')


def error(update, context):
    # Logs errors
    logging.error(f'Update {update} caused error {context.error}')
