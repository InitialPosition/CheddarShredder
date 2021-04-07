import chess
from enum import Enum

from os import system, name as os_name

from AI import Evaluation
from AI.Evaluation import get_negative_infinity, get_infinity, get_positional_value_for_piece, order_moves


def clear_screen():
    system('cls' if os_name == 'nt' else 'clear')


def get_ai_move(max_depth):
    # copy the board and generate all legal moves
    temp_board = board.copy()
    moves = temp_board.legal_moves

    # create an array to hold move-score objects
    moves_evaluated = []
    for legal_move in moves:
        moves_evaluated.append({"move": legal_move, "score": 0})

    # init array to hold the next iterations scores
    temp_evaluations = []

    # iterative deepening start
    for current_depth in range(max_depth):

        # remove scored moves from temp array
        temp_evaluations.clear()

        # go through ordered legal moves and evaluate with increasing depth
        for current_move in moves_evaluated:

            # get actual move from list
            legal_move = current_move["move"]
            # make test move
            temp_board.push(legal_move)

            # calculate move evaluation and save result
            if temp_board.turn == chess.WHITE:
                score = Evaluation.evaluate_board(temp_board, current_depth, get_negative_infinity(), get_infinity(), True)
            else:
                score = Evaluation.evaluate_board(temp_board, current_depth, get_negative_infinity(), get_infinity(), False)

            temp_evaluations.append({"move": legal_move, "score": score})

            # undo move
            temp_board.pop()

        # sort move list to increase alpha beta prune efficiency
        moves_evaluated.clear()
        moves_evaluated = temp_evaluations.copy()

        moves_evaluated.sort(key=get_move_score)

    print(f'Suggested move: {moves_evaluated[-1]["move"]} (Evaluation: {moves_evaluated[-1]["score"]})')
    return moves_evaluated


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
        while player_move not in board.pseudo_legal_moves:
            player_move_str = input('Move: ')
            player_move_str = player_move_str.lower()
            player_move = chess.Move(from_square=chess.parse_square(player_move_str[:2]),
                                     to_square=chess.parse_square(player_move_str[2:]))

        # at this point we have a valid user move string
        board.push(player_move)
    else:
        ai_move = get_ai_move(5)
        if board.turn == chess.WHITE:
            board.push(ai_move[-1]["move"])
        else:
            board.push(ai_move[0]["move"])

clear_screen()
print(board)
print(board.result())
