import json   
import login

def game_menu():
    option = input("1.Start a new game,\n2.Continue an old game,\n3.Sign out,\n4.Show game history,\n5.Show leaderboard\n")
    return option


def load_game(user1, user2, file_path):
    ids = []
    with open(file_path, 'r') as file:
        games = json.load(file)
    for i in games:
        if i["player1"] == user1 and i["player2"] == user2:
            ids.append(i['ID'])
    choice = int(input(f"choose a game id to load {ids}: "))
    return choice


def second_user_choice():
    print("choose an option for the second player")
    option = input("1.login,\n2.Sign Up,\n3.Exit\n")
    if option == '1':
        user2 = login.log_in()
    elif option == '2':
        user2 = login.sign_up()
    else:
        return
    return user2


outer_loop = True 

while outer_loop:
    choice1= login.main_menu()
    if choice1 == '1':
        user1 = login.log_in()
    elif choice1 == '2':
        user1 = login.sign_up()
    else:
        print("Exiting the game. Goodbye")
        exit()
    
    while True:
        choice2 = game_menu()
        if choice2 == '1':
            user2 = second_user_choice()
            if user2 == None:
                continue
            else:
                outer_loop = False
                break
        elif choice2 == '2':
            user2 = second_user_choice()
            if user2 == None:
                continue
            else: 
                game_id = load_game(user1, user2, "WallWizard/games.json")
                break
        elif choice2 == '3':
            break