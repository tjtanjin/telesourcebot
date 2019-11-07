from telegram import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext.dispatcher import run_async
from submodules import code_executor as ce
from submodules import user_management as um
from submodules import logger as lg
import json, threading, jsbeautifier, os
global executing_code
execute_code = False

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
    if not um.check_exist_user(update.message.chat_id):
        update.message.reply_text("You are not registered. Try <b>/register</b>", parse_mode=ParseMode.HTML)
    else:
        global executing_code
        executing_code = True
        executing = update.message.reply_text("<b>Executing Code |</b>", parse_mode=ParseMode.HTML)
        user = um.load_user_data(update.message.chat_id)
        threading.Thread(target=load_animation, args=(user, update, executing)).start()
        prep = ce.Launch(user["code_snippet"].replace("\n", ""))
        output = prep.action()
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
        code = jsbeautifier.beautify(user["code_snippet"])
        if code == "":
            code = "<b>No Existing Code Found.</b>"
        update.message.reply_text(code, parse_mode=ParseMode.HTML)
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
        mode = user["mode"]
        if mode == "0":
            track_code(update.message.text, user)
        else:
            update.message.reply_text("Invalid input. Use /code to toggle code mode.")
    return None

@run_async
def view_logs(update, context):
    """
    View the logs of the bot (admin only)
    Args:
        update: default telegram arg
        context: default telegram arg
    """
    try:
        if not um.check_exist_user(update.message.chat_id):
            update.message.reply_text("You are not registered. Try <b>/register</b>", parse_mode=ParseMode.HTML)
        else:
            user = um.load_user_data(update.message.chat_id)
        if not um.check_user_permission(user, "0"):
            update.message.reply_text("<b>Insufficient Permission.</b>", parse_mode=ParseMode.HTML)
        else:
            list_of_logs = os.listdir()
            retrieved_logs = show_logs(len(list_of_logs), list_of_logs, user)
            update.message.reply_text("<b>Please select a log:</b>", reply_markup=retrieved_logs, parse_mode=ParseMode.HTML)
        return None
    except Exception as ex:
        print("view_logs")
        print(ex)

@run_async
def retrieve_specified_log(bot, update):
    """
    Function that retrieves specific log for user.
    Args:
        bot: from telegram bot
        update: from telegram update
    """
    try:
        bot.answer_callback_query(update.callback_query.id)
        data = update.callback_query.data
        match_file = re.match(r'get_logs_(\S+)_(\S+)', data)
        filename, userid = match_file.group(1)
        user = load_user_data(userid)
        with open(filename, "r") as file:
            content = file.read()
        bot.send_message(chat_id=user["userid"], text=content)
        return None
    except Exception as ex:
        print("retrieve_specified_log")
        print(ex)

#------------------- Miscellaneous functions -------------------#

@run_async
def load_animation(user, update, message):
    """
    Function that provides loading animation during code execution.
    Args:
        user: user running the code
        update: default telegram arg
        context: default telegram arg
    """
    try:
        lg.logbook(user, "run_code")
    except Exception as ex:
        print(ex)
    while executing_code:
        message.edit_text(text="<b>Executing Code /</b>", parse_mode=ParseMode.HTML)
        message.edit_text(text="<b>Executing Code -</b>", parse_mode=ParseMode.HTML)
        message.edit_text(text="<b>Executing Code \\</b>", parse_mode=ParseMode.HTML)
        message.edit_text(text="<b>Executing Code |</b>", parse_mode=ParseMode.HTML)
    message.edit_text(text="<b>Execution Complete:</b>", parse_mode=ParseMode.HTML)
    return None

@run_async
def track_code(text, user):
    """
    Track code input of user in coding mode.
    Args:
        text: code to add
        user: user who is coding
    """
    user["code_snippet"] = user["code_snippet"] + text
    um.save_user_data(user)
    return None

@run_async
def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    """
    Function to build the menu buttons to show users.
    """
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu

@run_async
def show_logs(n_cols, text, user):
    """
    Function that takes in button text and callback data to generate the view.
    Args:
        n_cols: cols for button
        text: list of texts to show
        user: user to show logs to
    """
    try:
        button_list = []
        for i in range(0,n_cols):
            button_list.append(InlineKeyboardButton(text[i], callback_data="get_logs_" + text[i] + "_" + user["userid"]))
        reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=n_cols))
        return reply_markup
    except Exception as ex:
        print("show_logs")
        print(ex)