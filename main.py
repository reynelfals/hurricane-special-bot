
from handlers import *
import config

if __name__ == '__main__':
    logging.basicConfig(filename='hurricane_special_bot.log', level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    updater = Updater(config.API_KEY, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('help', help_command))

    dispatcher.add_handler(CommandHandler('hurricane', hurricane_map_command))
    dispatcher.add_handler(CommandHandler('huracan', hurricane_map_command_sp))
    dispatcher.add_handler(CommandHandler('mensaje', key_message_sp))
    dispatcher.add_handler(CommandHandler('message', key_message))
    dispatcher.add_handler(CommandHandler('satellite', satellite))
    dispatcher.add_handler(CommandHandler('animated', animated))
    dispatcher.add_handler(CommandHandler('animatedlite', animatedlite))
    dispatcher.add_handler(CommandHandler('sandwich', sandwich))
    dispatcher.add_handler(CommandHandler('winds', winds))

    dispatcher.add_handler(CommandHandler('geturls', geturls))
    dispatcher.add_handler(CommandHandler('seturl', seturl))
    dispatcher.add_handler(CommandHandler('setactive', setactive))
    dispatcher.add_handler(CommandHandler('setinactive', setinactive))


    dispatcher.add_error_handler(error)

    updater.start_polling()
    updater.idle()
