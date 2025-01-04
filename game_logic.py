import copy
import random

def matrix():
    return [[0 for i in range(17)] for j in range(17)]

matrix = matrix()
matrix[0][8] = 1
matrix[16][8] = 2
player1_pos = (0, 8)
player2_pos = (16, 8)

def show_board(matrix):
    for row in matrix:
        print(' '.join(str(cell) for cell in row))
    print()

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
    if move == 'down-left':
        if (x + 3 < len(matrix) and y - 3 >= 0 and
            ((matrix[x+2][y] != 0 and matrix[x+1][y] == 0 and matrix[x+3][y] != 0) or 
             (matrix[x][y-1] == 0 and matrix[x][y-2] != 0 and matrix[x][y-3] != 0)) and 
            is_valid_move_player(matrix, player_pos, 'down-to-left')):
            return True
    if move == 'up-right':
        if (x - 3 >= 0 and y + 3 < len(matrix[0]) and
            ((matrix[x-2][y] != 0 and matrix[x-1][y] == 0 and matrix[x-3][y] != 0) or 
             (matrix[x][y+1] == 0 and matrix[x][y+2] != 0 and matrix[x][y+3] != 0)) and 
            is_valid_move_player(matrix, player_pos, 'up-to-right')):
            return True
    if move == 'up-left':
        if (x - 3 >= 0 and y - 3 >= 0 and
            ((matrix[x-2][y] != 0 and matrix[x-1][y] == 0 and matrix[x-3][y] != 0) or 
             (matrix[x][y-1] == 0 and matrix[x][y-2] != 0 and matrix[x][y-3] != 0)) and 
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
    elif move == 'up-to-left' and x > 1 and y > 1:
        matrix[x][y] = 0
        matrix[x-2][y-2] = player_number
        player_pos = (x-2, y-2)
    elif move == 'up-to-right' and x > 1 and y < 15:
        matrix[x][y] = 0
        matrix[x-2][y+2] = player_number
        player_pos = (x-2, y+2)
    elif move == 'down-to-left' and x < 15 and y > 1:
        matrix[x][y] = 0
        matrix[x+2][y-2] = player_number
        player_pos = (x+2, y-2)
    elif move == 'down-to-right' and x < 15 and y < 15:
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
    if player_number == 1:
        player1_pos = player_pos
    elif player_number == 2:
        player2_pos = player_pos

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
    moves = ['up', 'down', 'left', 'right', 'down-to-left', 'down-to-right', 'up-to-left', 'up-to-right']
    for move in moves:
        if is_valid_move_player(matrix, player_pos, move):
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
    moves = ['up', 'down', 'left', 'right', 'down-to-left', 'down-to-right', 'up-to-left', 'up-to-right']
    for move in moves:
        if is_valid_move_player(matrix, player_pos, move):
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

def is_valid_move(matrix, player_pos, move, player_number):
    '''
    This function checks if the move is valid by considering all conditions
    '''
    if is_valid_move_player(matrix, player_pos, move):
        return True
    if is_special_move(matrix, player_pos, move):
        return True
    if player_number == 1:
        if dfs_1(matrix, player_pos):
            return True
    elif player_number == 2:
        if dfs_2(matrix, player_pos):
            return True
    return False

player1_walls = 10
player2_walls = 10
current_player = 1

while True:
    print(f"It is the turn of player {current_player}")
    print(f"Player 1 walls: {player1_walls} | Player 2 walls: {player2_walls}")
    action = input("Do you want to 'move' or 'place wall'? ").strip().lower()
    valid_moves = all_valid_moves(matrix, player1_pos if current_player == 1 else player2_pos)
    
    if action == 'move':
        move = input(f"Enter move {valid_moves}: ").strip()
        if current_player == 1:
            if move in valid_moves:
                player1_pos = move_player(matrix, player1_pos, move, 1)
            else:
                print("Invalid move! Try again.")
                continue
        else:
            if move in valid_moves:
                player2_pos = move_player(matrix, player2_pos, move, 2)
            else:
                print("Invalid move! Try again.")
                continue

    elif action == 'place wall':
        if (current_player == 1 and player1_walls > 0) or (current_player == 2 and player2_walls > 0):
            i = int(input("Enter wall position (row): "))
            j = int(input("Enter wall position (column): "))
            orientation = input("Enter wall orientation (e.g., 'up-right', 'down-left'): ").strip().split('-')
            if is_valid_wall(matrix, (i, j), orientation[0], orientation[1]):
                place_wall(matrix, (i, j), orientation[0], orientation[1])
                if current_player == 1:
                    player1_walls -= 1
                else:
                    player2_walls -= 1
            else:
                print("Invalid wall placement. Try again.")
        else:
            print("No walls left for this player!")
    else:
        print("Invalid action! Please choose 'move' or 'place wall'.")
        continue

    show_board(matrix)
    
    if is_winner1(player1_pos):
        print("Player 1 won!")
        break
    elif is_winner2(player2_pos):
        print("Player 2 won!")
        break

    current_player = 2 if current_player == 1 else 1