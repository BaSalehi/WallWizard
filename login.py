import os
import json
import uuid
import hashpass

users_json = 'WallWizard/users.json'

def main_menu():
    print("choose an option for the first player")
    option = input("1.Login\n2.Sign Up\n3.Exit\n")
    return option

def sign_up():
    user = input("Username: ")
    if user == "exit":
        print("Exiting the game. Goodbye")
        exit()

    pas = input("Password: ")
    if pas == "exit":
        print("Exiting the game. Goodbye")
        exit()

    email = input("Email: ")
    if email == "exit":
        print("Exiting the game. Goodbye")
        exit()
        
    user_id = str(uuid.uuid4())
    users = load_users()

    hashed_pass = hashpass.hash_password(pas)

    if user == "exit" or pas == "exit" or email == "exit":
        main_menu()
    
    email_check = check_email(email)

    while not email_check:
        print("please enter a correct email")
        email = input("Email: ")
        if email == "exit":
            print("Exiting the game. Goodbye")
            exit()
        email_check = check_email(email)

    user_info ={'ID': user_id,
                'username': user,
                'email': email,
                'password': hashed_pass}
    
    user_check = check_user(users, user, email)

    while not user_check:
        print("Username or email is already taken. Please try again.")
        user = input("Username: ")
        email = input("Email: ")
        if user == "exit":
            print("Exiting the game. Goodbye")
            exit()
        if email == "exit":
            print("Exiting the game. Goodbye")
            exit()
        user_check = check_user(users, user, email)
        
    if user_check:
        add_user(user_info)
        return user

    
def check_email(email):
    import re

    pattern = re.compile(r'[a-zA-Z0-9._+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}')

    emails = pattern.findall(email)

    if emails:
        return True
    else:
        return False

def load_users():
    if os.path.exists('WallWizard/users.json'):
        with open('WallWizard/users.json', 'r') as file:
            return json.load(file)
    return []
    

def add_user(user):
    users = []
    if os.path.exists('WallWizard/users.json'):
        try:
            with open('WallWizard/users.json', 'r') as file:
                users = json.load(file)
        except json.JSONDecodeError:
            print("Error reading JSON file. Initializing with an empty list.")
            users = []
        except Exception as e:
            print(f"An error occurred: {e}")
            return
    users.append(user)

    try:
        with open('WallWizard/users.json', 'w') as file:
            json.dump(users, file, indent=4)
    except Exception as e:
        print(f"An error occurred while writing to the file: {e}")


def check_user(users, username, email):
    if users == []:
        return True
    for user in users:
        if user['username'] == username or user['email'] == email:
            return False
    return True

def user_in_json(users, username, password):
    for user in users:
        if user['username'] == username and user['password'] == password:
            return True
    return False

def log_in():
    user = input("Username: ")
    if user == "exit":
        print("Exiting the game. Goodbye")
        exit()
    pas = input("Password: ")
    if pas == "exit":
        print("Exiting the game. Goodbye")
        exit()
    
    users = load_users()
    user_check = hashpass.check_password(user, pas)

    while not user_check:
        print("user not found. try again.")
        user = input("Username: ")
        if user == "exit":
            print("Exiting the game. Goodbye")
            exit()
        pas = input("Password: ")
        if pas == "exit":
            print("Exiting the game. Goodbye")
            exit()
        user_check = hashpass.check_password(user, pas)
    if user_check:
        print(f"successfully logged in as {user}")
        return user

