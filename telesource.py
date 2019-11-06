from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from submodules import user_input as ui
import json

def main():
    print("Running...")
    with open("./token/token.json", "r") as file:
        token = json.load(file)["token"]
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("register", ui.create_user))
    dp.add_handler(CommandHandler("help", ui.guide))
    dp.add_handler(CommandHandler("code", ui.toggle_code))
    dp.add_handler(CommandHandler("run", ui.run_code))
    dp.add_handler(CommandHandler("clear", ui.clear_code))
    dp.add_handler(CommandHandler("view", ui.view_code))
    dp.add_handler(MessageHandler(Filters.text, ui.check_mode))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()