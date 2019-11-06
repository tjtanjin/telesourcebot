from telegram import ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from test_code import Launch
import requests, json, os, threading, jsbeautifier
global executing_code
execute_code = False

def load_animation(update, message):
    while executing_code:
        message.edit_text(text="<b>Executing Code /</b>", parse_mode=ParseMode.HTML)
        message.edit_text(text="<b>Executing Code -</b>", parse_mode=ParseMode.HTML)
        message.edit_text(text="<b>Executing Code \\</b>", parse_mode=ParseMode.HTML)
        message.edit_text(text="<b>Executing Code |</b>", parse_mode=ParseMode.HTML)
    message.edit_text(text="<b>Execution Complete:</b>", parse_mode=ParseMode.HTML)
    return None

def guide(update, context):
    """
    Function to list help commands.
    Args:
        update: default telegram arg
        context: default telegram arg
    """
    update.message.reply_text("""Here are the currently available commands:\n
        <b>/register</b> - registers your account\n
        <b>/code</b> - toggles coding mode\n
        <b>/run</b> - runs your code\n
        <b>/clear</b> - clears your code\n
        <b>/view</b> - shows your current code\n
        <b>/help</b> - displays the available commands""", parse_mode=ParseMode.HTML)
    return None

def check_exist_user(userid):
    """
    Function to check if user exist.
    Args:
        path: path to the supposed user's folder
    """
    #checks if user exist by looking for file with user's username
    if not os.path.isfile("./userinfo/" + str(userid) + ".json"): 
        return False
    directory, filename = os.path.split("./userinfo/" + str(userid) + ".json")
    return filename in os.listdir(directory)

def create_user(update, context):
    """
    Function to create a user.
    Args:
        userid: userid of the new user
    """
    #set default values and save to userinfo folder
    #The userid folder stores a mapping of userid to registered username in case a player changes username in future
    if check_exist_user(update.message.chat_id):
        update.message.reply_text("You are already registered!")
    else:
        new_info = {"username":update.message.from_user.username, "userid":str(update.message.chat_id), "mode":"1", "user_group":"normal", "code_snippet":""}
        with open("./userinfo/" + str(update.message.chat_id) + ".json", 'w+') as info_file:
            json.dump(new_info, info_file)
        update.message.reply_text("Registration successfully completed. <b>/code</b> to start coding!", parse_mode=ParseMode.HTML)
    return None


def load_user_data(userid):
    """
    Function to load user data.
    Args:
        userid: user to be loaded
    """
    with open("./userinfo/" + str(userid) + ".json", 'r') as file:
        user = json.load(file)
    return user

def save_user_data(user):
    """
    Function to save user data.
    Args:
        user: user to be saved
    """
    with open("./userinfo/" + str(user["userid"]) + ".json", 'w+') as file:
        json.dump(user, file)
    return None

def toggle_code(update, context):
    """
    Function to toggle coding mode for user.
    Args:
        update: default telegram arg
        context: default telegram arg
    """
    if not check_exist_user(update.message.chat_id):
        update.message.reply_text("You are not registered. Try <b>/register</b>", parse_mode=ParseMode.HTML)
    else:
        user = load_user_data(update.message.chat_id)
        if user["mode"] == "0":
            user["mode"] = "1"
            update.message.reply_text("<b>Code Mode Disabled</b>", parse_mode=ParseMode.HTML)
        else:
            user["mode"] = "0"
            update.message.reply_text("<b>Code Mode Enabled</b>", parse_mode=ParseMode.HTML)
        save_user_data(user)
    return None

def track_code(text, user):
    """
    Track code input of user in coding mode.
    Args:
        text: code to add
        user: user who is coding
    """
    user["code_snippet"] = user["code_snippet"] + text
    save_user_data(user)
    return None

def run_code(update, context):
    """
    Run the code snippet of the user.
    Args:
        update: default telegram arg
        context: default telegram arg
    """
    if not check_exist_user(update.message.chat_id):
        update.message.reply_text("You are not registered. Try <b>/register</b>", parse_mode=ParseMode.HTML)
    else:
        global executing_code
        executing_code = True
        executing = update.message.reply_text("<b>Executing Code |</b>", parse_mode=ParseMode.HTML)
        threading.Thread(target=load_animation, args=(update, executing)).start()
        user = load_user_data(update.message.chat_id)
        prep = Launch(user["code_snippet"].replace("\n", ""))
        output = prep.action()
        executing_code = False
        update.message.reply_text(output)
    return None

def clear_code(update, context):
    """
    Clear the code snippet of the user.
    Args:
        update: default telegram arg
        context: default telegram arg
    """
    if not check_exist_user(update.message.chat_id):
        update.message.reply_text("You are not registered. Try <b>/register</b>", parse_mode=ParseMode.HTML)
    else:
        user = load_user_data(update.message.chat_id)
        user["code_snippet"] = ""
        save_user_data(user)
        update.message.reply_text("<b>Code Cleared</b>", parse_mode=ParseMode.HTML)
    return None

def view_code(update, context):
    """
    View the current code of the user.
    Args:
        update: default telegram arg
        context: default telegram arg
    """
    if not check_exist_user(update.message.chat_id):
        update.message.reply_text("You are not registered. Try <b>/register</b>", parse_mode=ParseMode.HTML)
    else:
        user = load_user_data(update.message.chat_id)
        code = jsbeautifier.beautify(user["code_snippet"])
        if code == "":
            code = "<b>No Existing Code Found.</b>"
        update.message.reply_text(code, parse_mode=ParseMode.HTML)
    return None

def check_mode(update, context): 
    """
    Function to check mode of user.
    Args:
        update: default telegram arg
        context: default telegram arg
    """
    if not check_exist_user(update.message.chat_id):
        update.message.reply_text("You are not registered. Try <b>/register</b>", parse_mode=ParseMode.HTML)
    else:
        user = load_user_data(update.message.chat_id)
        mode = user["mode"]
        if mode == "0":
            track_code(update.message.text, user)
        else:
            update.message.reply_text("Invalid input. Use /code to toggle code mode.")
    return None

def main():
    print("Running...")
    with open("./token/token.json", "r") as file:
        token = json.load(file)["token"]
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("register", create_user))
    dp.add_handler(CommandHandler("help", guide))
    dp.add_handler(CommandHandler("code", toggle_code))
    dp.add_handler(CommandHandler("run", run_code))
    dp.add_handler(CommandHandler("clear", clear_code))
    dp.add_handler(CommandHandler("view", view_code))
    dp.add_handler(MessageHandler(Filters.text, check_mode))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()