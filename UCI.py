#!/usr/bin/env python3

import sys
import chess
from AI.Evaluation import evaluate_board, get_negative_infinity, get_infinity
from random import choice
import multiprocessing


board = chess.Board()


def get_move_score(e):
    # only return the score part from the move-score object
    return e["score"]


def get_ai_move(max_depth):
    # copy the board and generate all legal moves
    local_board = board.copy()
    moves = local_board.legal_moves

    # init best move variables
    current_best_score = get_infinity()
    current_best_move = None
    
    scored_moves = {}

    for current_move in moves:
        local_board.push(current_move)

        score = evaluate_board(local_board, max_depth, get_negative_infinity(), get_infinity())
        if score < current_best_score:
            current_best_score = score

        local_board.pop()
        
        scored_moves.update({current_move: score})
    
    best_moves = []
    
    for move in scored_moves:
        if scored_moves[move] == current_best_score:
            best_moves.append(move)

    return choice(best_moves)


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
            board.reset()

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
            time_check = 99999999

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

            if time_check != 99999999:
                # lower at...
                if time_check > 480:    # if over 4 minutes, play at top level
                    ai_level = 5
                if time_check <= 240:   # 4 minutes
                    ai_level = 4
                if time_check <= 120:   # 2 minutes
                    ai_level = 3
                if time_check <= 60:    # 1 minute
                    ai_level = 2
                if time_check <= 20:    # 20 seconds
                    ai_level = 1

            moves_depth_one = len(list(board.legal_moves))
            move_reduction = 0

            if moves_depth_one > 30:
                move_reduction = 1
            elif moves_depth_one > 40:
                move_reduction = 2
            elif moves_depth_one > 60:
                move_reduction = 3

            ai_level = max(1, ai_level - move_reduction)

            move = get_ai_move(ai_level)

            sys.stdout.write(f'bestmove {move}\n')
            sys.stdout.flush()

        if line == 'quit':
            exit(0)
