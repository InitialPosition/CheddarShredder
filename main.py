import chess
from enum import Enum
from threading import Thread

from os import system, name as os_name

from AI import Evaluation
from AI.Evaluation import get_negative_infinity, get_infinity


def clear_screen():
    system('cls' if os_name == 'nt' else 'clear')


def get_ai_move(max_depth):
    # copy the board and generate all legal moves
    moves = board.legal_moves

    # init best move variables
    current_best_score = get_infinity()
    current_best_move = None

    for move in moves:
        board.push(move)

        score = Evaluation.evaluate_board(board, max_depth, get_negative_infinity(), get_infinity())
        if score < current_best_score:
            current_best_score = score
            current_best_move = move

            print(f'New best move: {current_best_move}, Eval: {current_best_score}')

        board.pop()

    return current_best_move, current_best_score


def get_move_score(e):
    # only return the score part from the move-score object
    return e["score"]


# ENTRY POINT
board = chess.Board()

# clear terminal
clear_screen()

# get human player
print('Human player?\n(1): White\n(2): Black\n(3): None')
human_player = input('Selection: ')

if human_player not in ['1', '2', '3']:
    exit()

if human_player == '1':
    human_player = chess.WHITE
elif human_player == '2':
    human_player = chess.BLACK
elif human_player == '3':
    human_player = None

# start game loop
while board.is_game_over() is False:
    clear_screen()
    print(board)

    # get player move if its players turn
    player_move_str = None
    player_move = None
    if board.turn == human_player:
        while player_move not in board.legal_moves:
            player_move_str = input('Move: ')
            player_move_str = player_move_str.lower()
            player_move = chess.Move(from_square=chess.parse_square(player_move_str[:2]),
                                     to_square=chess.parse_square(player_move_str[2:]))

        # at this point we have a valid user move string
        board.push(player_move)
    else:
        threads = []
        best_moves = []

        for i in range(thread_count):
            thread = Thread()
            threads.append(thread)

        board.push(ai_move)

print(board)
print(board.result())
