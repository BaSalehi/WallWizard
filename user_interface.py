import json   
import login
from rich.console import Console

console = Console()

def game_menu():
    option = input("1.Start a new game,\n2.Continue an old game,\n3.Sign out,\n4.Show game history,\n5.Show leaderboard\n")
    return option


def load_game(user1, user2, file_path):
    ids = []
    with open(file_path, 'r') as file:
        games = json.load(file)
    for i in games:
        if (i["player1"] == user1 and i["player2"] == user2) or (i["player1"] == user2 and i["player2"] == user1):
            ids.append(i['ID'])
        ids = list(set(ids))
    choice = int(input(f"choose a game id to load {ids}: "))
    if choice == "exit":
        exit()
    return choice


def second_user_choice():
    console.print("choose an option for the second player", style="cyan")
    option = input("1.login,\n2.Sign Up,\n3.Exit\n")
    if option == '1':
        user2 = login.log_in()
    elif option == '2':
        user2 = login.sign_up()
    else:
        return
    return user2

