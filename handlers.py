from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from telegram.ext import *
import logging
import requests
import telegram
import config
import yaml
from helpers import *

command_keyboard = [
    [KeyboardButton('/animatedlite'),  KeyboardButton('/animated')],
    [KeyboardButton('/satellite'), KeyboardButton('/hurricane')],
    [KeyboardButton('/sandwich'), KeyboardButton('/message')]
]

command_keyboard_sp = [
    [ KeyboardButton('/animatedlite'),  KeyboardButton('/animated')],
    [KeyboardButton('/satellite'), KeyboardButton('/huracan')],
    [KeyboardButton('/sandwich'), KeyboardButton('/mensaje')]
]

markup = ReplyKeyboardMarkup(command_keyboard, one_time_keyboard=True, selective=True)
markup_sp = ReplyKeyboardMarkup(command_keyboard_sp, one_time_keyboard=True, selective=True)

def isactive():
    file_handle = open(config.URLS,"r")
    yaml_dict = yaml.load(file_handle)

    return yaml_dict.get("active", False), yaml_dict

def start(update, context):
    logging.info(f'User {update.message.chat.first_name}, id {update.message.chat.id}, calling start command')
    update.message.reply_text(text='**Welcome Friend**\n'
                                   'I can help you to track hurricanes, mainly at the **Caribbean Sea**\n\n'
                                   
                                   'Here, the list of commands:\n\n'
                                   
                                   '`/animated` or `/satellite gif`     \- 500x500 pixels satellite clip\.\n\n'
                                   
                                   '`/animatedlite` or `/satellite lite`     \- 500x500 pixels gray satellite clip, lightweight\.\n\n'
                                   
                                   '`/sandwich`     \- 1000x1000 pixels sandwich clip\.\n\n'
                                   
                                   '`/hurricane` or `/huracan`          \- Probability cone\.\n\n'
                                   
                                   '`/satellite` or `/satellite low`    \- Low resolution satellite image\.\n\n'
                                   
                                   '`/satellite high`                   \- High resolution satellite image\.\n\n'
                                   
                                   '`/message` or `/mensaje` \(espagnol\) \- Key message\.\n'
                                    
                                    '`/help` \- Helpful to see the list of commands\.',
                              parse_mode="MarkdownV2",
                              reply_markup=markup)

def toggle_custom_keyboard(update, context):
    logging.info(f'User {update.message.chat.first_name}, id {update.message.chat.id}, calling toggle command')


def hurricane_map_command(update, context):

    logging.info(f'User {update.message.chat.first_name}, id {update.message.chat.id}, calling hurricane command')
    (proceed, yaml_dict) = isactive()
    if not proceed:
        update.message.reply_text('No cyclone activity expected in the next 48 hours.',
                                  reply_markup=markup)
        return
    r = requests.get(yaml_dict.get("hurricane").get("url"),
                     stream=True)
    if r.status_code == 200:
        context.bot.send_photo(update.message.chat.id, r.raw,
                               reply_markup=markup, caption='Cone of Uncertainty')

        update.message.reply_text('Maybe you want to check /satellite also.',
                                  reply_markup=markup)
    else:
        logging.error(f'Error in request code: {r.status_code}')


def help_command(update, context):
    logging.info(f'User {update.message.chat.first_name}, id {update.message.chat.id}, calling help command')
    update.message.reply_text(text='Use the commands\n'
                              '`/animated` or `/satellite gif` \- Satellite Clip\.\n'
                              '`/animatedlite` or `/satellite lite` \- Gray Satellite Clip lightweight\.\n'
                              '`/sandwich` \- Sandwich Clip\.\n'
                              '`/hurricane` or `/huracan` \- Probability Cone\.\n'
                              '`/satellite` or `/satellite low` \- 500x500 Satellite Image\.\n'
                              '`/satellite high` \- 1000x1000 Satellite Image\.\n'
                              '`/message` or `/mensaje` \- Key message\.\n', parse_mode="MarkdownV2",
                              reply_markup=markup)


def hurricane_map_command_sp(update, context):
    logging.info(f'User {update.message.chat.first_name}, id {update.message.chat.id}, calling huracan command')
    (proceed, yaml_dict) = isactive()
    if not proceed:
        update.message.reply_text('No cyclone activity expected in the next 48 hours.',
                                  reply_markup=markup)
        return
    r = requests.get(yaml_dict.get("huracan").get("url"),
                     stream=True)
    if r.status_code == 200:
        context.bot.send_photo(update.message.chat.id, r.raw,
                               reply_markup=markup_sp)

        update.message.reply_text('El mapa ^. Quizas quiera chequear /satellite',
                                  reply_markup=markup_sp)
    else:
        logging.error(f'Error in request code: {r.status_code}')

def key_message(update, context):
    logging.info(f'User {update.message.chat.first_name}, id {update.message.chat.id}, calling message command')
    (proceed, yaml_dict) = isactive()
    if not proceed:
        update.message.reply_text('No cyclone activity expected in the next 48 hours.',
                                  reply_markup=markup)
        return
    r = requests.get(yaml_dict.get("key_message").get("url"), stream=True)
    if r.status_code == 200:
        context.bot.send_photo(update.message.chat.id, r.raw)
        update.message.reply_text('Key Message ^ (Para espagnol /mensaje)',
                                  reply_markup=markup)
    else:
        logging.error(f'Error in request code: {r.status_code}')


def key_message_sp(update, context):
    logging.info(f'User {update.message.chat.first_name}, id {update.message.chat.id}, calling mensaje command')
    (proceed, yaml_dict) = isactive()
    if not proceed:
        update.message.reply_text('No cyclone activity expected in the next 48 hours.',
                                  reply_markup=markup)
        return
    context.bot.send_photo(chat_id=update.message.chat.id,
                   photo=yaml_dict.get("key_message_sp").get("url"),
                           reply_markup=markup_sp)
    update.message.reply_text('Mensaje clave ^ (For english /message)',
                              reply_markup=markup_sp)

#https://cdn.star.nesdis.noaa.gov/FLOATER/data/AL052021/GEOCOLOR/latest.jpg
#https://cdn.star.nesdis.noaa.gov/FLOATER/data/AL052021/GEOCOLOR/500x500.jpg

def satellite(update: Update, context: CallbackContext):


    mode = 'low'
    args = context.args
    if len(args)>0:
        mode = args[0]
    if mode == 'gif':
        return animated(update,context)
    if mode == 'lite':
        return animatedlite(update,context)

    logging.info(f'User {update.message.chat.first_name}, id {update.message.chat.id}, calling satellite {mode} command')
    (proceed, yaml_dict) = isactive()
    if not proceed:
        update.message.reply_text('No cyclone activity expected in the next 48 hours.',
                                  reply_markup=markup)
        return
    modes={'low':yaml_dict.get("satellite_low").get("url"),
           'high': yaml_dict.get("satellite_high").get("url"),
           'gif': "data/resized.gif",
           'lite': "data/resized_gray.gif"}
    url = modes.get(mode, 'low')

    r = requests.get(url, stream=True)

    if r.status_code == 200:
        context.bot.send_photo(update.message.chat.id, r.raw,
                               reply_markup=markup, caption=f'Satellite {mode} resolution')
        update.message.reply_text('Change resolution using arguments: /satellite low or /satellite high',
                                  reply_markup=markup)
    else:
        logging.error(f'Error in request code: {r.status_code}')

#https://cdn.star.nesdis.noaa.gov/FLOATER/data/AL052021/GEOCOLOR/GOES16-AL052021-GEOCOLOR-1000x1000.gif
def animated(update, context):
    logging.info(f'User {update.message.chat.first_name}, id {update.message.chat.id}, calling animated command')
    (proceed, yaml_dict) = isactive()
    if not proceed:
        update.message.reply_text('No cyclone activity expected in the next 48 hours.',
                                  reply_markup=markup)
        return
    context.bot.send_document(chat_id=update.message.chat.id, document=open('./data/resized500_500.gif', 'rb'),
                              reply_markup=markup, caption='Satellite Animation')
    update.message.reply_text('For a lightweight alternative use /animatedlite',
                              reply_markup=markup)

def animatedlite(update, context):
    logging.info(f'User {update.message.chat.first_name}, id {update.message.chat.id}, calling animatedlite command')
    (proceed, yaml_dict) = isactive()
    if not proceed:
        update.message.reply_text('No cyclone activity expected in the next 48 hours.',
                                  reply_markup=markup)
        return
    context.bot.send_document(chat_id=update.message.chat.id, document=open('./data/resized500_500_gray.gif', 'rb'),
                              reply_markup=markup, caption='Satellite Animation Gray Scale')
    update.message.reply_text('Check /animated for a colored version.',
                              reply_markup=markup)

def sandwich(update, context):
    logging.info(f'User {update.message.chat.first_name}, id {update.message.chat.id}, calling sandwich command')
    (proceed, yaml_dict) = isactive()
    if not proceed:
        update.message.reply_text('No cyclone activity expected in the next 48 hours.',
                                  reply_markup=markup)
        return
    r = requests.get(yaml_dict.get("sandwich").get("url"), stream=True)
    context.bot.send_document(chat_id=update.message.chat.id,
                              document=r.raw,
                              reply_markup=markup)


def geturls(update, context):
    logging.info(f'User {update.message.chat.first_name}, id {update.message.chat.id}, calling geturls command')
    if update.message.chat.id != config.OWNER_ID:
        logging.info(f'User {update.message.chat.first_name}, id {update.message.chat.id}, cant call geturl command')
        update.message.reply_text('No permissions to geturl',
                                  reply_markup=markup)
        return

    file_handle = open(config.URLS,"r")
    yaml_dict = yaml.load(file_handle)
    mystr="List of urls:\n"
    for k, v in yaml_dict.items():
        if  isinstance(v, dict):
            url = v.get('url', "")
            if len(url)>0:
                mystr += f'{k} - {url}\n'
    update.message.reply_text(mystr,
                              reply_markup=markup)

def seturl(update, context):
    logging.info(f'User {update.message.chat.first_name}, id {update.message.chat.id}, calling seturl command')
    if update.message.chat.id != config.OWNER_ID:
        logging.info(f'User {update.message.chat.first_name}, id {update.message.chat.id}, cant call seturl command')
        update.message.reply_text('No permissions to seturl',
                                  reply_markup=markup)
        return
    if len(context.args)<2:
        update.message.reply_text('Need to specify command and url: /seturl <command> <url address>',
                                  reply_markup=markup)
        return

    command=context.args[0]
    url=context.args[1]

    file_handle_r = open(config.URLS, "r")
    yaml_dict = yaml.load(file_handle_r)
    yaml_dict[command]={'url': f'{url}'}
    file_handle_r.close()
    file_handle_w = open(config.URLS, "w+")
    yaml.dump(yaml_dict, file_handle_w)

    update.message.reply_text('URL added',
                                  reply_markup=markup)


def active(update, value):
    if update.message.chat.id != config.OWNER_ID:
        logging.info(f'User {update.message.chat.first_name}, id {update.message.chat.id}, cant call active command')
        update.message.reply_text('No permissions to set active',
                                  reply_markup=markup)
        return
    file_handle_r = open(config.URLS,"r")
    parsed_yaml_file = yaml.load(file_handle_r)
    file_handle_r.close()
    parsed_yaml_file['active']=value
    file_handle_w = open(config.URLS,"w")
    yaml.dump(parsed_yaml_file,file_handle_w )
    file_handle_w.close()
    update.message.reply_text(f'Set active to {value}',
                              reply_markup=markup)

def setactive(update, context):
    logging.info(f'User {update.message.chat.first_name}, id {update.message.chat.id}, calling setactive command')
    active(update, True)

def setinactive(update, context):
    logging.info(f'User {update.message.chat.first_name}, id {update.message.chat.id}, calling setinactive command')
    active(update, False)

def error(update, context):
    logging.error(f'Update {update} with error {context.error}')
