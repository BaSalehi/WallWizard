import os
import keyboard
import json
import uuid

users_json = 'users.json'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def display_menu(options, selected_index):
    clear_screen()
    for index, option in enumerate(options):
        if index == selected_index:
            print(f"> {option}  ")
        else:
            print(f"  {option}  ")

def main_menu():
    options = ["Login", "Sign Up", "Exit"]
    selected_index = 0

    while True:
        display_menu(options, selected_index)

        if keyboard.is_pressed('up'):
            selected_index = (selected_index - 1) % len(options)
            while keyboard.is_pressed('up'):
                pass
        elif keyboard.is_pressed('down'):
            selected_index = (selected_index + 1) % len(options)
            while keyboard.is_pressed('down'):
                pass
        elif keyboard.is_pressed('enter'):
            break

    return options[selected_index]


def sign_up():
    user = input("Username: ")
    pas = input("Password: ")
    email = input("Email: ")
    user_id = str(uuid.uuid4())
    users = load_users()


    if user == "exit" or pas == "exit" or email == "exit":
        main_menu()
    
    email_check = check_email(email)

    while not email_check:
        print("please enter a correct email")
        email = input("Email: ")
        email_check = check_email(email)

    user_info ={'ID': user_id,
                'username': user,
                'email': email,
                'password': pas}
    
    user_check = check_user(users, user, email)

    if not user_check:
        return "Username or email is already taken. Please try again."
    else:
        add_user(user_info)

def check_email(email):
    import re

    pattern = re.compile(r'[a-zA-Z0-9._+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}')

    emails = pattern.findall(email)

    if emails:
        return True
    else:
        return False

def load_users():
    if os.path.exists('users.json'):
        with open('users.json', 'r') as file:
            return json.load(file)
    return []

def add_user(user):
    try:
        with open('users.json', 'r') as file:
            users = json.load(file)
    except FileNotFoundError:
        users = []

    users.append(user)

    with open('users.json', 'w') as file:
        json.dump(users, file, indent=4)

def check_user(users, username, email):
    if users == []:
        return True
    for user in users:
        if user['username'] == username or user['email'] == email:
            return False
    return True

choice = main_menu()
if choice == "Sign Up":
    sign_up()

