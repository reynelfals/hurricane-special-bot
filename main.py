from telegram.ext import *
from handlers import *
import config
# Run the programme
if __name__ == '__main__':
    updater = Updater(config.API_KEY, use_context=True)
    dp = updater.dispatcher

    # Commands
    dp.add_handler(CommandHandler('hurricane', start_command))
    dp.add_handler(CommandHandler('help', help_command))
    dp.add_handler(CommandHandler('huracan', custom_command))
    dp.add_handler(CommandHandler('mensaje', key_message_sp))
    dp.add_handler(CommandHandler('message', key_message))

    # # Messages
    # dp.add_handler(MessageHandler(Filters.text, handle_message))

    # Log all errors
    dp.add_error_handler(error)

    # Run the bot
    updater.start_polling(1.0)
    updater.idle()