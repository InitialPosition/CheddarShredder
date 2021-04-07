#!/usr/bin/env python3

import sys
import chess
from AI.Evaluation import evaluate_board, get_negative_infinity, get_infinity


board = chess.Board()


def get_move_score(e):
    # only return the score part from the move-score object
    return e["score"]


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
                score = evaluate_board(temp_board, current_depth, get_negative_infinity(), get_infinity(), True)
            else:
                score = evaluate_board(temp_board, current_depth, get_negative_infinity(), get_infinity(), False)

            temp_evaluations.append({"move": legal_move, "score": score})

            # undo move
            temp_board.pop()

        # sort move list to increase alpha beta prune efficiency
        moves_evaluated.clear()
        moves_evaluated = temp_evaluations.copy()

        moves_evaluated.sort(key=get_move_score)

    return moves_evaluated


while 1:

    for line in sys.stdin:

        line = line.rstrip()

        if line == 'uci':
            sys.stdout.write('id name CheeseGrater 1.0\n')
            sys.stdout.write('id author InitialPosition\n')
            sys.stdout.flush()

            sys.stdout.write('option name Move Overhead type spin default 30 min 0 max 5000\n')
            sys.stdout.write('option name Threads type spin default 1 min 1 max 1\n')
            sys.stdout.write('option name Hash type spin default 16 min 1 max 2048\n')
            sys.stdout.write('option name Ponder type check default false\n')
            sys.stdout.flush()

            sys.stdout.write('uciok\n')
            sys.stdout.flush()

        if line == 'ucinewgame':
            board.reset_board()

        if line == 'isready':
            sys.stdout.write('readyok\n')
            sys.stdout.flush()

        if line.startswith('position'):
            options = line.split(' ')
            if options[1] == 'startpos':
                fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
            else:
                fen = options[1]

            board.set_fen(fen)

            if 'moves' in options:
                move_start_index = options.index('moves')
                for i in range(move_start_index + 1, len(options)):
                    move = options[i]
                    board.push(chess.Move.from_uci(move))

        if line.startswith('go'):

            white_time = -1
            black_time = -1
            time_check = 99999

            # parse gamestate
            if ' ' in line:
                split_line = line.split(' ')

                if 'wtime' in split_line:
                    wtime_index = split_line.index('wtime')
                    white_time = split_line[wtime_index + 1]
                if 'btime' in split_line:
                    btime_index = split_line.index('btime')
                    black_time = split_line[btime_index + 1]

            # if a time was given, choose appropriate search depth
            ai_level = 3

            white_time = int(white_time)
            black_time = int(black_time)

            if white_time != -1:
                if board.turn == chess.WHITE:
                    time_check = white_time / 1000
            if black_time != -1:
                if board.turn == chess.BLACK:
                    time_check = black_time / 1000

                # lower at...
                if time_check > 300:    # if over 5, play at top level
                    ai_level = 4
                if time_check <= 300:   # 5 minutes
                    ai_level = 3
                if time_check <= 60:    # 1 minute
                    ai_level = 2
                if time_check <= 10:    # 10 seconds
                    ai_level = 1

            move = get_ai_move(ai_level)
            if board.turn == chess.WHITE:
                sys.stdout.write(f'bestmove {move[-1]["move"]}\n')
            else:
                sys.stdout.write(f'bestmove {move[0]["move"]}\n')
            sys.stdout.flush()

        if line == 'quit':
            exit(0)
