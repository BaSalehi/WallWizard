import os
import json
import uuid
import hashpass
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
console = Console()

users_json = 'users.json'

def main_menu():
    title_panel = Panel("WELCOME TO QUORIDOR", title=" ", border_style="bold blue", expand=True, padding=(1, 65), style="bold white")
    console.print(title_panel)
    console.print("choose an option for the first player", style="cyan")
    option = input("1.Login\n2.Sign Up\n3.Exit\n")
    return option

def sign_up():
    user = input("Username: ")
    if user == "exit":
        print("Exiting the game. Goodbye")
        exit()
    while user == "":
        console.print("username cannot be empty.", style="red")
        user = input("Username: ")
        if user == "exit":
            print("Exiting the game. Goodbye")
            exit()

    pas = input("Password: ")
    if pas == "exit":
        print("Exiting the game. Goodbye")
        exit()

    while pas == "":
        console.print("password cannot be empty.", style="red")
        pas = input("Password: ")   
        if pas == "exit":
            print("Exiting the game. Goodbye")
            exit()

    while len(pas) < 8:
        console.print("password should be longer than or equal to 8 characters.", style="red")
        pas = input("Password: ")
        if pas == "exit":
            print("Exiting the game. Goodbye")
            exit()

    email = input("Email: ")
    if email == "exit":
        print("Exiting the game. Goodbye")
        exit()
    while email == "":
        console.print("email cannot be empty.", style="red")
        email = input("Email: ")
        if email == "exit":
            console.print("Exiting the game. Goodbye", style="green")
            exit()

    user_id = str(uuid.uuid4())
    users = load_users()

    hashed_pass = hashpass.hash_password(pas)

    if user == "exit" or pas == "exit" or email == "exit":
        main_menu()
    
    email_check = check_email(email)

    while not email_check:
        console.print("please enter a correct email", style="bold red")
        email = input("Email: ")
        while email == "":
            console.print("email cannot be empty.", style="red")
            email = input("Email: ")
            if email == "exit":
                console.print("Exiting the game. Goodbye", style="green")
                exit()
        if email == "exit":
            console.print("Exiting the game. Goodbye", style="green")
            exit()
        email_check = check_email(email)

    user_info ={'ID': user_id,
                'username': user,
                'email': email,
                'password': hashed_pass,
                'score':0,
                'wins': 0,
                'losses': 0,
                'play_time': 0}
    
    user_check = check_user(users, user, email)

    while not user_check:
        console.print("Username or email is already taken. Please try again.", style="bold red")
        user = input("Username: ")
        while user == "":
            console.print("username cannot be empty.", style="red")
            user = input("Username: ")
            if user == "exit":
                print("Exiting the game. Goodbye")
                exit()

        email = input("Email: ")
        while email == "":
            console.print("email cannot be empty.", style="red")
            email = input("Email: ")
            if email == "exit":
                console.print("Exiting the game. Goodbye", style="green")
                exit()

        if user == "exit":
            console.print("Exiting the game. Goodbye", style="green")
            exit()
        if email == "exit":
            console.print("Exiting the game. Goodbye", style="green")
            exit()
        user_check = check_user(users, user, email)
        
    if user_check:
        add_user(user_info)
        console.print(f"successfully signed-up {user}", style="bold green")
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
    if os.path.exists('users.json'):
        with open('users.json', 'r') as file:
            return json.load(file)
    return []
    

def add_user(user):
    users = []
    if os.path.exists('users.json'):
        try:
            with open('users.json', 'r') as file:
                users = json.load(file)
        except json.JSONDecodeError:
            print("Error reading JSON file. Initializing with an empty list.")
            users = []
        except Exception as e:
            print(f"An error occurred: {e}")
            return
    users.append(user)

    try:
        with open('users.json', 'w') as file:
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
    while user == "":
        console.print("username cannot be empty.", style="red")
        user = input("Username: ")
        if user == "exit":
            print("Exiting the game. Goodbye")
            exit()
    if user == "exit":
        console.print("Exiting the game. Goodbye", style="green")
        exit()

    pas = input("Password: ")

    while pas == "":
        console.print("password cannot be empty.", style="red")
        pas = input("Password: ")   
        if pas == "exit":
            print("Exiting the game. Goodbye")
            exit()

    if pas == "exit":
        console.print("Exiting the game. Goodbye", style="green")
        exit()

    users = load_users()
    user_check = hashpass.check_password(user, pas)

    while not user_check:
        console.print("user not found. try again.", style="bold red")
        user = input("Username: ")
        if user == "exit":
            console.print("Exiting the game. Goodbye", style="green")
            exit()
        pas = input("Password: ")
        if pas == "exit":
            console.print("Exiting the game. Goodbye", style="green")
            exit()
        user_check = hashpass.check_password(user, pas)
    if user_check:
        console.print(f"successfully logged in as {user}", style="bold green")
        return user