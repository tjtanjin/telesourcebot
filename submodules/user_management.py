import json, os

def check_user_permission(user, perms):
    """
    Function to check user permissions.
    Args
        userid: user to be checked for perms
        perms: perms to check against
    """
    with open("./config/permissions.json", "r") as file:
        permission = json.load(file)
    return user["user_group"] == permission[perms]

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
    try:
        with open("./userinfo/" + str(userid) + ".json", 'r') as file:
            user = json.load(file)
        return user
    except:
        return False


def save_user_data(user):
    """
    Function to save user data.
    Args:
        user: user to be saved
    """
    with open("./userinfo/" + str(user["userid"]) + ".json", 'w+') as file:
        json.dump(user, file)
    return None

def verify_username(user, current_name):
    if user["username"] != current_name:
        user["username"] = current_name
        save_user_data(user)
    return None
