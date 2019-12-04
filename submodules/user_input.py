from telegram import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext.dispatcher import run_async
from submodules import code_executor as ce
from submodules import user_management as um
from submodules import logger as lg
import json, threading, jsbeautifier, os, re, requests

#------------------- User input functions -------------------#
@run_async
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
        <b>/help</b> - displays the available commands\n
Have ideas and suggestions for this mini project? Head over to the <a href="https://github.com/tjtanjin/telesourcebot">Project Repository</a>!""", parse_mode=ParseMode.HTML, disable_web_page_preview=True)
    return None

@run_async
def create_user(update, context):
    """
    Function to create a user.
    Args:
        userid: userid of the new user
    """
    #set default values and save to userinfo folder
    #The userid folder stores a mapping of userid to registered username in case a player changes username in future
    if um.check_exist_user(update.message.chat_id):
        update.message.reply_text("You are already registered!")
    else:
        new_info = {"username":update.message.from_user.username, "userid":str(update.message.chat_id), "mode":"1", "user_group":"normal", "code_snippet":""}
        lg.logbook(new_info, "register")
        with open("./userinfo/" + str(update.message.chat_id) + ".json", 'w+') as info_file:
            json.dump(new_info, info_file)
        update.message.reply_text("Registration successfully completed. <b>/code</b> to start coding!", parse_mode=ParseMode.HTML)
    return None

@run_async
def toggle_code(update, context):
    """
    Function to toggle coding mode for user.
    Args:
        update: default telegram arg
        context: default telegram arg
    """
    if not um.check_exist_user(update.message.chat_id):
        update.message.reply_text("You are not registered. Try <b>/register</b>", parse_mode=ParseMode.HTML)
    else:
        user = um.load_user_data(update.message.chat_id)
        if not user:
            return error(update)
        if user["mode"] == "0":
            user["mode"] = "1"
            update.message.reply_text("<b>Code Mode Disabled</b>", parse_mode=ParseMode.HTML)
        else:
            user["mode"] = "0"
            update.message.reply_text("<b>Code Mode Enabled</b>", parse_mode=ParseMode.HTML)
        um.save_user_data(user)
    return None

@run_async
def run_code(update, context):
    """
    Run the code snippet of the user.
    Args:
        update: default telegram arg
        context: default telegram arg
    """
    executing_code = False
    def load_animation(user, update, message):
        """
        Function that provides loading animation during code execution.
        Args:
            user: user running the code
            update: default telegram arg
            context: default telegram arg
        """
        lg.logbook(user, "run_code")
        while executing_code:
            message.edit_text(text="<b>Executing Code /</b>", parse_mode=ParseMode.HTML)
            message.edit_text(text="<b>Executing Code -</b>", parse_mode=ParseMode.HTML)
            message.edit_text(text="<b>Executing Code \\</b>", parse_mode=ParseMode.HTML)
            message.edit_text(text="<b>Executing Code |</b>", parse_mode=ParseMode.HTML)
        message.edit_text(text="<b>Execution Complete:</b>", parse_mode=ParseMode.HTML)
        return None

    if not um.check_exist_user(update.message.chat_id):
        update.message.reply_text("You are not registered. Try <b>/register</b>", parse_mode=ParseMode.HTML)
    else:
        executing_code = True
        executing = update.message.reply_text("<b>Executing Code |</b>", parse_mode=ParseMode.HTML)
        user = um.load_user_data(update.message.chat_id)
        if not user:
            return error(update)
        threading.Thread(target=load_animation, args=(user, update, executing)).start()
        with open("./config/endpoint.json", "r") as file:
            endpoint = json.load(file)["endpoint"]
        res = requests.post(endpoint, data = {"userid": user["userid"]})
        output = res.content.decode('utf-8')[1:-1]
        executing_code = False
        update.message.reply_text(output)
    return None

@run_async
def clear_code(update, context):
    """
    Clear the code snippet of the user.
    Args:
        update: default telegram arg
        context: default telegram arg
    """
    if not um.check_exist_user(update.message.chat_id):
        update.message.reply_text("You are not registered. Try <b>/register</b>", parse_mode=ParseMode.HTML)
    else:
        user = um.load_user_data(update.message.chat_id)
        if not user:
            return error(update)
        user["code_snippet"] = ""
        um.save_user_data(user)
        update.message.reply_text("<b>Code Cleared</b>", parse_mode=ParseMode.HTML)
    return None

@run_async
def view_code(update, context):
    """
    View the current code of the user.
    Args:
        update: default telegram arg
        context: default telegram arg
    """ 
    if not um.check_exist_user(update.message.chat_id):
        update.message.reply_text("You are not registered. Try <b>/register</b>", parse_mode=ParseMode.HTML)
    else:
        user = um.load_user_data(update.message.chat_id)
        if not user:
            return error(update)
        code = jsbeautifier.beautify(user["code_snippet"])
        if code == "":
            code = "<b>No Existing Code Found.</b>"
            update.message.reply_text(code, parse_mode=ParseMode.HTML)
        else:
            if len(code) > 4096: 
                for i in range(0, len(code), 4096):
                    update.message.reply_text(code[i:i+4096]) 
            else:
                update.message.reply_text(code) 
    return None

@run_async
def check_mode(update, context): 
    """
    Function to check mode of user.
    Args:
        update: default telegram arg
        context: default telegram arg
    """
    if not um.check_exist_user(update.message.chat_id):
        update.message.reply_text("You are not registered. Try <b>/register</b>", parse_mode=ParseMode.HTML)
    else:
        user = um.load_user_data(update.message.chat_id)
        if not user:
            return error(update)
        mode = user["mode"]
        if mode == "0":
            track_code(update.message.text, user)
        else:
            update.message.reply_text("Invalid input. Use /code to toggle code mode.")
    return None

@run_async
def view_logs(update, context):
    """
    View the logs of the bot (admin only).
    Args:
        update: default telegram arg
        context: default telegram arg
    """
    if not um.check_exist_user(update.message.chat_id):
        update.message.reply_text("You are not registered. Try <b>/register</b>", parse_mode=ParseMode.HTML)
    else:
        user = um.load_user_data(update.message.chat_id)
        if not user:
            return error(update)
    if not um.check_user_permission(user, "0"):
        update.message.reply_text("<b>Insufficient Permission.</b>", parse_mode=ParseMode.HTML)
    else:
        list_of_logs = os.listdir("./logs")
        retrieved_logs = show_logs(len(list_of_logs), list_of_logs, user)
        update.message.reply_text("<b>Please select a log:</b>", reply_markup=retrieved_logs, parse_mode=ParseMode.HTML)
    return None

@run_async
def broadcast(update, context):
    """
    Broadcast updates to users (admin only).
    Args:
        update: default telegram arg
        context: default telegram arg
    """
    if not um.check_exist_user(update.message.chat_id):
        update.message.reply_text("You are not registered. Try <b>/register</b>", parse_mode=ParseMode.HTML)
    else:
        user = um.load_user_data(update.message.chat_id)
        if not user:
            return error(update)
    if not um.check_user_permission(user, "0"):
        update.message.reply_text("<b>Insufficient Permission.</b>", parse_mode=ParseMode.HTML)
    else:
        for filename in os.listdir("./userinfo/"):
            context.bot.send_message(filename[:-5], text="Broadcast: " + context.arg[0])

@run_async
def retrieve_specified_log(update, context):
    """
    Function that retrieves specific log for user.
    Args:
        bot: from telegram bot
        update: from telegram update
    """
    context.bot.answer_callback_query(update.callback_query.id)
    data = update.callback_query.data
    match_file = re.match(r'get_logs_(\S+)_(\S+)', data)
    filename, userid = match_file.group(1), match_file.group(2)
    user = um.load_user_data(userid)
    if not user:
            return error(update)
    with open("./logs/" + filename, "r") as file:
        content = file.read()
    if len(content) > 4096: 
        for i in range(0, len(content), 4096): 
            context.bot.send_message(chat_id=user["userid"], text=content[i:i+4096]) 
    else: 
        context.bot.send_message(chat_id=user["userid"], text=content)
    return None

#------------------- Miscellaneous functions -------------------#

@run_async
def track_code(text, user):
    """
    Track code input of user in coding mode.
    Args:
        text: code to add
        user: user who is coding
    """
    user["code_snippet"] = user["code_snippet"] + text.replace("\n", "")
    um.save_user_data(user)
    return None

def build_menu(buttons, header_buttons=None, footer_buttons=None):
    """
    Function to build the menu buttons to show users.
    """
    menu = [buttons[i] for i in range(0, len(buttons))]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu

def show_logs(n_rows, text, user):
    """
    Function that takes in button text and callback data to generate the view.
    Args:
        n_rows: rows for button
        text: list of texts to show
        user: user to show logs to
    """
    button_list = []
    for i in range(0,n_rows):
        button_list.append([InlineKeyboardButton(text[i], callback_data="get_logs_" + text[i] + "_" + user["userid"])])
    reply_markup = InlineKeyboardMarkup(build_menu(button_list))
    return reply_markup

def error(update):
    """
    Function that handles unexpected errors.
    Args:
        update: from telegram update
    """
    update.message.reply_text("<b>An error has occurred. Please contact @FRUZNFEVER to resolve the issue.</b>", parse_mode=ParseMode.HTML)
