from telegram.ext.dispatcher import run_async
import json, os

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