from datetime import datetime, date
import os

def check_exist_log(current_date):
    """
    Function to check if user exist.
    Args:
        path: path to the supposed user's folder
    """
    #checks if user exist by looking for file with user's username
    if not os.path.isfile("./logs/" + current_date + ".txt"): 
        return False
    directory, filename = os.path.split("./logs/" + current_date + ".txt")
    return filename in os.listdir(directory)

def logbook(user, task):
	"""
	Function logbook records the actions of users into a .txt file.
	Args:
		user: user who carried out the action
		task: task carried out by the user, currently only tracks registrations and code runs
	"""
	if task == "register":
		action = "[" + str(datetime.now()) + "] " + user["username"] + " has registered an account."
	if task == "run_code":
		action = "[" + str(datetime.now()) + "] " + user["username"] + " has executed /run with the following code: {" + user["code_snippet"] + "}"
	else:
		action = "Action not recorded."
	current_date = str(date.today())
	if check_exist_log(current_date):
		with open("./logs/" + current_date + ".txt", "a+") as file:
			file.write(action + "\n")
	else:
		with open("./logs/" + current_date + ".txt", "w+") as file:
			file.write(action + "\n")
	return None
