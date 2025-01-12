import copy
import random
import os
import json 
# import login

from rich.console import Console
from rich.table import Table
from rich.text import Text
# import user_iterface

class Game:
    def __init__(self, id, user1, user2, user1_position, user2_position, user1_walls, user2_walls, game_board, current_player):
        self.id = id
        self.user1 = user1
        self.user2 = user2
        self.user1_position = user1_position
        self.user2_position = user2_position
        self.user1_walls = user1_walls
        self.user2_walls = user2_walls
        self.game_board = game_board
        self.current_player = current_player
        self.winner = 0

    

def update_item(file_path, item_id, new_value):

    with open(file_path, 'r') as file:
        games = json.load(file)
    new_game = list()    
    for item in games:
        if item['ID'] == item_id:
            new_game.append(new_value)
        else:
            new_game.append(item) 
    file2 = open(file_path, 'w') 
    i =json.dumps(new_game , indent=4)
    file2.write(i)
    file2.close()

def generate_id():
    with open('games.json', 'r') as file:
        games = json.load(file)
    new_id = len(games) + 1
    return new_id

game_id = generate_id()

def add_game(game_info):
    games = []
    if os.path.exists('games.json'):
        try:
            with open('games.json', 'r') as file:
                games = json.load(file)
        except json.JSONDecodeError:
            print("Error reading JSON file. Initializing with an empty list.")
            games = []
        except Exception as e:
            print(f"An error occurred: {e}")
            return
    games.append(game_info)
    try:
        with open('games.json', 'w') as file:
            json.dump(games, file, indent=4)
    except Exception as e:
        print(f"An error occurred while writing to the file: {e}")


def matrix():
    return [[0 for i in range(17)] for j in range(17)]



def show_board(matrix):
    console = Console()
    table = Table(show_header=False, box=None)  

    headers = [" "]
    headers.extend([str(i//2 + 1) if i % 2 == 0 else " " for i in range(17)])
    table.add_row(*headers)
    
    for i in range(17):
        row = [str(i//2 + 1) if i % 2 == 0 else " "]  
        for j in range(17):
            if i % 2 == 0:
                if j % 2 == 0 and matrix[i][j] == 0:
                    cell = Text("+", style="bold green")  
                elif j % 2 == 0 and matrix[i][j] != 0:
                    cell = Text(str(matrix[i][j]), style="bold blue")
                elif j % 2 != 0 and matrix[i][j] == 0:
                    cell = " "
                elif j % 2 != 0 and matrix[i][j] != 0:
                    cell = Text(str(matrix[i][j]), style="bold blue")
            else:
                if j % 2 == 0 and matrix[i][j] != 0:
                    cell = Text(str(matrix[i][j]), style="bold blue")
                elif j % 2 == 0 and matrix[i][j] == 0:
                    cell = " "
                elif j % 2 != 0:
                    cell = " "
            row.append(cell)
        table.add_row(*row)

    console.print(table)


def is_valid_move_player(matrix, player_pos, move):
    '''
    This function checks if the move is valid
    '''
    x, y = player_pos
    if move == 'up':
        return x > 1 and matrix[x-1][y] == 0 and matrix[x-2][y] == 0
    elif move == 'down':
        return x < 15 and matrix[x+1][y] == 0 and matrix[x+2][y] == 0
    elif move == 'right':
        return y < 15 and matrix[x][y+1] == 0 and matrix[x][y+2] == 0
    elif move == 'left':
        return y > 1 and matrix[x][y-1] == 0 and matrix[x][y-2] == 0
    elif move == 'down-to-left':
        return x < 15 and y > 0 and matrix[x+1][y-1] == 0
    elif move == 'down-to-right':
        return x < 15 and y < 15 and matrix[x+1][y+1] == 0
    elif move == 'up-to-right':
        return x > 0 and y < 15 and matrix[x-1][y+1] == 0
    elif move == 'up-to-left':
        return x > 0 and y > 0 and matrix[x-1][y-1] == 0
    return False

def is_special_move(matrix, player_pos, move):
    x, y = player_pos
    if move == 'down-right':
        if (x + 3 < len(matrix) and y + 3 < len(matrix[0]) and
            ((matrix[x+2][y] != 0 and matrix[x+1][y] == 0 and matrix[x+3][y] != 0) or 
             (matrix[x][y+1] == 0 and matrix[x][y+2] != 0 and matrix[x][y+3] != 0)) and
            is_valid_move_player(matrix, player_pos, 'down-to-right')):
            return True
        elif(((x+2 == 16 and matrix[x+1][y]==0 and matrix[x+2][y]!=0)or
             (y==2 and matrix[x][1]==0 and matrix[x][0] != 0) and
             is_valid_move_player(matrix, player_pos, 'down-to-right'))):
            return True

    if move == 'down-left':
        if (x + 3 < len(matrix) and y - 3 >= 0 and
            ((matrix[x+2][y] != 0 and matrix[x+1][y] == 0 and matrix[x+3][y] != 0) or 
             (matrix[x][y-1] == 0 and matrix[x][y-2] != 0 and matrix[x][y-3] != 0)) and
            is_valid_move_player(matrix, player_pos, 'down-to-left')):
            return True
        elif (((x+2 == 16 and matrix[x+1][y]==0 and matrix[x+2][y]!=0) or
             (y==2 and matrix[x][1]==0 and matrix[x][0] != 0)) and 
              is_valid_move_player(matrix, player_pos, 'down-to-left')):
            return True
    if move == 'up-right':
        if (x - 3 >= 0 and y + 3 < len(matrix[0]) and
            ((matrix[x-2][y] != 0 and matrix[x-1][y] == 0 and matrix[x-3][y] != 0) or 
             (matrix[x][y+1] == 0 and matrix[x][y+2] != 0 and matrix[x][y+3] != 0))and
            is_valid_move_player(matrix, player_pos, 'up-to-right')):
            return True
        elif(((x-2 == 0 and matrix[x-1][y]==0 and matrix[x-2][y] !=0)or
             (y==14 and matrix[x][15]==0 and matrix[x][16]!=0)) and
             is_valid_move_player(matrix, player_pos, 'up-to-right')):
            return True

    if move == 'up-left':
        if (x - 3 >= 0 and y - 3 >= 0 and
            ((matrix[x-2][y] != 0 and matrix[x-1][y] == 0 and matrix[x-3][y] != 0) or 
             (matrix[x][y-1] == 0 and matrix[x][y-2] != 0 and matrix[x][y-3] != 0)) and
            is_valid_move_player(matrix, player_pos, 'up-to-left')):
            return True
        elif(((x-2 == 0 and matrix[x-1][y]==0 and matrix[x-2][y]!=0)or
              (y==14 and matrix[x][15]==0 and matrix[x][16]!=0)) and
              is_valid_move_player(matrix, player_pos, 'up-to-left')):
            return True

    if move == 'double_up':
        if x > 2 and matrix[x-1][y]==0 and matrix[x-2][y]!=0 and matrix[x-3][y]==0:
            return True
    if move == 'double_down':
        if x < 14 and matrix[x+1][y]==0 and matrix[x+2][y]!=0 and matrix[x+3][y]==0:
            return True
    if move == 'double_left':
        if y > 2 and matrix[x][y-1]==0 and matrix[x][y-2]!=0 and matrix[x][y-3]==0:
            return True 
    if move == 'double_right':
        if y < 14 and matrix[x][y+1]==0 and matrix[x][y+2]!=0 and matrix[x][y+3]==0:
            return True 
    return False
def special_moves(matrix, player_pos):
    possible_moves = []
    special_moves = ['down-right', 'down-left', 'up-right', 'up-left','double_up','double_down','double_left','double_right']
    for move in special_moves:
        if is_special_move(matrix, player_pos, move):
            possible_moves.append(move)
    return possible_moves

def all_valid_moves(matrix, player_pos):
    lst_special = special_moves(matrix, player_pos)
    result = []
    moves = ['up', 'down', 'right', 'left']
    for move in moves:
        if is_valid_move_player(matrix, player_pos, move):
            result.append(move)
    if lst_special:
        result += lst_special
    return result

def is_valid_wall(matrix, wall_pos, move1, move2):
    x, y = wall_pos
    x = 2 * x - 2
    y = 2 * y - 2

            
    if move1 == 'up' and move2 == 'right':
        return x > 0 and y < 15 and matrix[x-1][y] == 0 and matrix[x-1][y+1] == 0 and matrix[x-1][y+2] == 0
    elif move1 == 'up' and move2 == 'left':
        return x > 0 and y > 0 and matrix[x-1][y] == 0 and matrix[x-1][y-1] == 0 and matrix[x-1][y-2] == 0
    elif move1 == 'down' and move2 == 'right':
        return x < 15 and y < 15 and matrix[x+1][y] == 0 and matrix[x+1][y+1] == 0 and matrix[x+1][y+2] == 0
    elif move1 == 'down' and move2 == 'left':
        return x < 15 and y > 0 and matrix[x+1][y] == 0 and matrix[x+1][y-1] == 0 and matrix[x+1][y-2] == 0
    elif move1 == 'right' and move2 == 'up':
        return x > 0 and y < 15 and matrix[x][y+1] == 0 and matrix[x-1][y+1] == 0 and matrix[x-2][y+1] == 0
    elif move1 == 'right' and move2 == 'down':
        return x < 15 and y < 15 and matrix[x][y+1] == 0 and matrix[x+1][y+1] == 0 and matrix[x+2][y+1] == 0
    elif move1 == 'left' and move2 == 'up':
        return x > 0 and y > 0 and matrix[x][y-1] == 0 and matrix[x-1][y-1] == 0 and matrix[x-2][y-1] == 0
    elif move1 == 'left' and move2 == 'down':
        return x < 15 and y > 0 and matrix[x][y-1] == 0 and matrix[x+1][y-1] == 0 and matrix[x+2][y-1] == 0
    return False

def move_player(matrix, player_pos, move, player_number):
    '''
    This function moves the player in the matrix according to the move
    '''
    global player1_pos, player2_pos
    x, y = player_pos
    if move == 'up' and x > 1:
        matrix[x][y] = 0
        matrix[x-2][y] = player_number
        player_pos = (x-2, y)
    elif move == 'down' and x < 15:
        matrix[x][y] = 0
        matrix[x+2][y] = player_number
        player_pos = (x+2, y)
    elif move == 'left' and y > 1:
        matrix[x][y] = 0
        matrix[x][y-2] = player_number
        player_pos = (x, y-2)
    elif move == 'right' and y < 15:
        matrix[x][y] = 0
        matrix[x][y+2] = player_number
        player_pos = (x, y+2)
    elif move == 'up-left' and x > 1 and y > 1:
        matrix[x][y] = 0
        matrix[x-2][y-2] = player_number
        player_pos = (x-2, y-2)
    elif move == 'up-right' and x > 1 and y < 15:
        matrix[x][y] = 0
        matrix[x-2][y+2] = player_number
        player_pos = (x-2, y+2)
    elif move == 'down-left' and x < 15 and y > 1:
        matrix[x][y] = 0
        matrix[x+2][y-2] = player_number
        player_pos = (x+2, y-2)
    elif move == 'down-right' and x < 15 and y < 15:
        matrix[x][y] = 0
        matrix[x+2][y+2] = player_number
        player_pos = (x+2, y+2)
    elif move == 'double_up':
        matrix[x][y] = 0
        matrix[x-4][y]= player_number
        player_pos = (x-4, y)
    elif move == 'double_down':
        matrix[x][y] = 0
        matrix[x+4][y]=player_number
        player_pos = (x+4, y) 
    elif move == 'double_left':
        matrix[x][y] = 0
        matrix[x][y-4]=player_number
        player_pos = (x, y-4)   
    elif move == 'double_right':
        matrix[x][y] = 0
        matrix[x][y+4]=player_number
        player_pos = (x, y+4)

    return player_pos  


def place_wall(matrix, wall_pos, move1, move2):
    '''
    This function places a wall in the matrix
    '''
    x, y = wall_pos
    x = 2 * x - 2
    y = 2 * y - 2
    if move1 == 'up' and move2 == 'right' and x > 0 and y < 15:
        matrix[x-1][y] = '-'
        matrix[x-1][y+1] = '-'
        matrix[x-1][y+2] = '-'
    if move1 == 'up' and move2 == 'left' and x > 0 and y > 0:
        matrix[x-1][y] = '-'
        matrix[x-1][y-1] = '-'
        matrix[x-1][y-2] = '-'
    if move1 == 'down' and move2 == 'right' and x < 15 and y < 15:
        matrix[x+1][y] = '-'
        matrix[x+1][y+1] = '-'
        matrix[x+1][y+2] = '-'
    if move1 == 'down' and move2 == 'left' and x < 15 and y > 0:
        matrix[x+1][y] = '-'
        matrix[x+1][y-1] = '-'
        matrix[x+1][y-2] = '-'
    if move1 == 'right' and move2 == 'up' and x > 0 and y < 15:
        matrix[x][y+1] = '|'
        matrix[x-1][y+1] = '|'
        matrix[x-2][y+1] = '|'
    if move1 == 'right' and move2 == 'down' and x < 15 and y < 15:
        matrix[x][y+1] = '|'
        matrix[x+1][y+1] = '|'
        matrix[x+2][y+1] = '|'
    if move1 == 'left' and move2 == 'up' and x > 0 and y > 0:
        matrix[x][y-1] = '|'
        matrix[x-1][y-1] = '|'
        matrix[x-2][y-1] = '|'
    if move1 == 'left' and move2 == 'down' and x < 15 and y > 0:
        matrix[x][y-1] = '|'
        matrix[x+1][y-1] = '|'
        matrix[x+2][y-1] = '|'

def dfs_1(matrix, player_pos, visited=None):
    if visited is None:
        visited = set()
    x, y = player_pos
    if x == 16:
        return True
    visited.add((x, y))

    for move in all_valid_moves(matrix, player_pos):
            matrix_copy = copy.deepcopy(matrix)
            new_pos = move_player(matrix_copy, player_pos, move, 1)
            if new_pos not in visited:
                if dfs_1(matrix_copy, new_pos, visited):
                    return True
    return False

def dfs_2(matrix, player_pos, visited=None):
    if visited is None:
        visited = set()
    x, y = player_pos
    if x == 0:
        return True
    visited.add((x, y))
    for move in all_valid_moves(matrix, player_pos):
            matrix_copy = copy.deepcopy(matrix)
            new_pos = move_player(matrix_copy, player_pos, move, 2)
            if new_pos not in visited:
                if dfs_2(matrix_copy, new_pos, visited):
                    return True
    return False

def is_winner1(player_pos):
    '''
    This function checks if player1 has won
    '''
    x, y = player_pos
    if x == 16:
        return True
    return False

def is_winner2(player_pos):
    '''
    This function checks if player2 has won
    '''
    x, y = player_pos
    if x == 0:
        return True
    return False

def main_game(matrix , player1_pos , player2_pos , player1_walls , player2_walls , current_player , game_id , user1,user2):
    while True:
        if is_winner1(player1_pos):
            print("Player 1 won!")
            break
        elif is_winner2(player2_pos):
            print("Player 2 won!")
            break
        print('game id:',game_id)
        print(f'player1:{user1} | player2:{user2}')
        print(f"It is the turn of {user1 if current_player == 1 else user2}")
        print(f"Player 1 walls: {player1_walls} | Player 2 walls: {player2_walls}")
        action = input("Do you want to 'move' or 'place wall'? ").strip().lower()
        valid_moves = all_valid_moves(matrix, player1_pos if current_player == 1 else player2_pos)
        if action == 'move':
            move = input(f"Enter move {valid_moves}: ").strip()
            if current_player == 1:
                if move in valid_moves:
                    player1_pos = move_player(matrix, player1_pos, move, 1)
                elif move == 'exit':
                    break
                else:
                    print("Invalid move! Try again.")
                    continue
            else:
                if move in valid_moves:
                    player2_pos = move_player(matrix, player2_pos, move, 2)
                elif move == 'exit':
                    break
                else:
                    print("Invalid move! Try again.")
                    continue
        elif action == 'place wall':
            if (current_player == 1 and player1_walls > 0) or (current_player == 2 and player2_walls > 0):
                i = int(input("Enter wall position (row): "))
                if i == 'exit':
                    break
                else:
                    j = int(input("Enter wall position (column): "))
                    if j == 'exit':
                        break
                    orientation = input("Enter wall orientation (e.g. 'up-right', 'down-left'): ").strip().split('-')
                    if is_valid_wall(matrix, (i, j), orientation[0], orientation[1]):
                        new_matrix = copy.deepcopy(matrix)
                        place_wall(new_matrix, (i, j), orientation[0], orientation[1])
                        if dfs_1(new_matrix, player1_pos) and dfs_2(new_matrix, player2_pos):
                            place_wall(matrix, (i, j), orientation[0], orientation[1])
                            if current_player == 1:
                                player1_walls -= 1
                            else:
                                player2_walls -= 1
                    else:
                        print("Invalid wall placement. Try again.")
                        continue
            else:
                print("No walls left for this player!")
                continue
        elif action == 'exit':
            break
        else:
            print("Invalid action! Please choose 'move' or 'place wall'.")
            continue
        show_board(matrix)
        current_player = 2 if current_player == 1 else 1
        game_info = {
            "ID": game_id,
            "player1": user1,
            "player2": user2,
            "user1_position": player1_pos,
            "user2_position": player2_pos,
            "user1_walls": player1_walls,
            "user2_walls": player2_walls,
            "game_board": matrix,
            "current_player": current_player,
            "winner": 0
        }
        if os.path.exists('./games.json'):
            with open('games.json', 'r') as file:
                games = json.load(file)
            ids = []
            for i in games:
                ids.append(i['ID'])
            if game_id in ids:
                update_item('games.json', game_id, game_info)
            else:
                add_game(game_info)

while True:
    inp = input('new game or load game? ')
    if inp == 'new game':
        new_id = generate_id()
        matrix = matrix()
        matrix[0][8] = 1
        matrix[16][8] = 2
        player1_pos = (0, 8)
        player2_pos = (16, 8)
        player1_walls = 10
        player2_walls = 10
        current_player = random.choice([1, 2])
        user1 = 'user1'
        user2 = 'user2'
        main_game(matrix , player1_pos , player2_pos , player1_walls , player2_walls , current_player , new_id , user1 , user2)
    elif inp == 'load game':
        id = int(input('Enter the game id: '))
        with open('games.json', 'r') as file:
            games = json.load(file)
            ids = []
            for game in games:
                ids.append(game['ID'])
            if id not in ids:
                print('this id does not exist')
                continue
            for game in games:
                if game['ID'] == id:
                    id = game['ID']
                    matrix = game['game_board']
                    player1_pos = game['user1_position']
                    player2_pos = game['user2_position']
                    player1_walls = game['user1_walls']
                    player2_walls = game['user2_walls']
                    current_player = game['current_player']
                    user1 = game['player1']
                    user2 = game['player2']
                    main_game(matrix , player1_pos , player2_pos , player1_walls , player2_walls , current_player,id,user1,user2)

# user_iterface.main()
# print(user_iterface.user1)