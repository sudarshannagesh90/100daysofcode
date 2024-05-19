import random
import re

def check_game_over(board):
    lines = [[(0, 0), (0, 1), (0, 2)],
             [(1, 0), (1, 1), (1, 2)],
             [(2, 0), (2, 1), (2, 2)],
             [(0, 0), (1, 0), (2, 0)],
             [(0, 1), (1, 1), (2, 1)],
             [(0, 2), (1, 2), (2, 2)],
             [(0, 0), (1, 1), (2, 2)],
             [(0, 2), (1, 1), (2, 0)]]
    for line in lines:
        if board[line[0][0]][line[0][1]] and \
            board[line[0][0]][line[0][1]] == board[line[1][0]][line[1][1]] \
                == board[line[2][0]][line[2][1]]:
            return True
    return False

def replace_elems(line):
    elems = []
    for elem in line:
        if not elem:
            elems.append(' ')
        else:
            elems.append(elem)
    return elems
def show_board(board):
    dash_line_str = ' '.join(['_', '_', '_'])
    f_str = '\n'.join(['|'.join(replace_elems(board[0])), dash_line_str,
                       '|'.join(replace_elems(board[1])), dash_line_str,
                       '|'.join(replace_elems(board[2]))])
    print(f_str)

def human_plays(ch):
    show_board(board)
    while True:
        choice = input('{0} (x,y)? '.format(ch.upper()))
        search_result = re.search(r'(\d),\s?(\d)', choice)
        if not search_result:
            continue
        choice = (search_result.group(1), search_result.group(2))
        if (int(choice[0]), int(choice[1])) in \
                choices:
            break
    board[int(choice[0])][int(choice[1])] = '{0}'.format(ch.upper())
    choices.remove((int(choice[0]), int(choice[1])))
    return check_game_over(board)

def computer_plays(ch):
    choice = random.choice(choices)
    board[choice[0]][choice[1]] = '{0}'.format(ch.upper())
    choices.remove(choice)
    return check_game_over(board)

keep_playing = 'y'
while keep_playing.lower() != 'q':
    print('Please note 0<=x,y<=2')
    toss = random.choice([0, 1])
    choices = [(x, y) for x in range(3) for y in range(3)]
    board = [['', '', ''] for _ in range(3)]
    while True:
        if toss == 0:
            if choices and computer_plays('X'): print('X wins!'); break
            if choices and human_plays('O'): print('O wins!'); break
        else:
            if choices and human_plays('X'): print('X wins!'); break
            if choices and computer_plays('O'): print('O wins!'); break
        if not choices: print('Draw!'); break
    show_board(board)
    keep_playing = input('Press q to quit.').strip()
