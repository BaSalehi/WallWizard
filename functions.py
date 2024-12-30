def matrix():
    return [ [0 for i in range(17)] for j in range(17)]


def move_player(matrix, player_pos, move, player_number):
    '''
    This function moves the player in the matrix according to the move
    '''
    x, y = player_pos
    if move == 'up' and x > 1:
        matrix[x][y] = 0
        matrix[x-2][y] = player_number
        player_pos = [x-2, y]
    elif move == 'down' and x < 15:
        matrix[x][y] = 0
        matrix[x+2][y] = player_number
        player_pos = [x+2, y]
    elif move == 'right' and y < 15:
        matrix[x][y] = 0
        matrix[x][y+2] = player_number
        player_pos = [x, y+2]
    elif move == 'left' and y > 1:
        matrix[x][y] = 0
        matrix[x][y-2] = player_number
        player_pos = [x, y-2]


def special_moves(matrix, player_pos, move, player_number):
    '''
    this funtion works when we need an especial move
    '''
    x, y = player_pos
    if move == 'up-right' and x > 0 and y < 15:
        matrix[x][y] = 0
        matrix[x-2][y+2] = player_number
        player_pos = [x-2, y+2]
    if move == 'up-left' and x > 0 and y > 0:
        matrix[x][y] = 0
        matrix[x-2][y-2] = player_number
        player_pos = [x-2, y-2]
    if move == 'down-right' and x < 15 and y < 15:
        matrix[x][y] = 0
        matrix[x+2][y+2] = player_number
        player_pos = [x+2, y+2]
    if move == 'down-left' and x < 15 and y > 0:
        matrix[x][y] = 0
        matrix[x+2][y-2] = player_number
        player_pos = [x+2, y-2]


def place_wall(matrix , wall_pos, move1 , move2):
    '''
    This function places a wall in the matrix
    '''
    x, y = wall_pos
    x = 2*x - 2
    y = 2*y - 2
    if move1 == 'up' and move2 == 'right' and x>0 and y<15:
        matrix[x-1][y] = '-'
        matrix[x-1][y+1] = '-'
    if move1 == 'up' and move2 == 'left' and x>0 and y>0:
        matrix[x-1][y] = '-'
        matrix[x-1][y-1] = '-'
    if move1 == 'down' and move2 == 'right' and x<15 and y<15:
        matrix[x+1][y] = '-'
        matrix[x+1][y+1] = '-'
    if move1 == 'down' and move2 == 'left' and x<15 and y>0:
        matrix[x+1][y] = '-'
        matrix[x+1][y-1] = '-'
    if move1 == 'right' and move2 == 'up' and x>0 and y<15:
        matrix[x][y+1] = '|'
        matrix[x-1][y+1] = '|'
    if move1 == 'right' and move2 == 'down' and x<15 and y<15:
        matrix[x][y+1] = '|'
        matrix[x+1][y+1] = '|'
    if move1 == 'left' and move2 == 'up' and x>0 and y>0:
        matrix[x][y-1] = '|'
        matrix[x-1][y-1] = '|'
    if move1 == 'left' and move2 == 'down' and x<15 and y>0:
        matrix[x][y-1] = '|'
        matrix[x+1][y-1] = '|'
