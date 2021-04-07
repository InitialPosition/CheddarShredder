import chess


def get_infinity():
    return 99999999


def get_negative_infinity():
    return -99999999


def evaluate_board(board: chess.Board, depth: int, alpha: int, beta: int, maximizing: bool):
    # return if max depth reached
    if depth == 0:
        node_eval = evaluate_position(board, maximizing)
        return node_eval

    moves = board.legal_moves

    if board.is_repetition(2):
        return 0

    if board.is_checkmate():
        if board.turn == chess.WHITE:
            return get_negative_infinity()
        return get_infinity()

    if moves.count() == 0:
        return 0

    if maximizing:
        value = get_negative_infinity()
        for move in moves:

            board.push(move)
            value = max(value, evaluate_board(board, depth - 1, alpha, beta, False))
            board.pop()

            alpha = max(alpha, value)

            if alpha >= beta:
                break

        return value
    else:
        value = get_infinity()
        for move in moves:

            board.push(move)
            value = min(value, evaluate_board(board, depth - 1, alpha, beta, True))
            board.pop()

            beta = min(beta, value)

            if beta <= alpha:
                break

        return value


def get_positional_value_for_piece(piece: str, square: chess.Square, player_color: chess.COLOR_NAMES,
                                   board: chess.Board = None):
    # all values from https://www.chessprogramming.org/Simplified_Evaluation_Function
    # (arrays have been flipped to fit the board implementation)
    pawn = [[0, 0, 0, 0, 0, 0, 0, 0],
            [5, 10, 10, -20, -20, 10, 10, 5],
            [5, -5, -10, 0, 0, -10, -5, 5],
            [0, 0, 0, 20, 20, 0, 0, 0],
            [5, 5, 10, 25, 25, 10, 5, 5],
            [10, 10, 20, 30, 30, 20, 10, 10],
            [50, 50, 50, 50, 50, 50, 50, 50],
            [0, 0, 0, 0, 0, 0, 0, 0]]

    knight = [[-50, -40, -30, -30, -30, -30, -40, -50],
              [-40, -20, 0, 5, 5, 0, -20, -40],
              [-30, 5, 10, 15, 15, 10, 5, -30],
              [-30, 0, 15, 20, 20, 15, 0, -30],
              [-30, 5, 15, 20, 20, 15, 5, -30],
              [-30, 0, 10, 15, 15, 10, 0, -30],
              [-40, -20, 0, 0, 0, 0, -20, -40],
              [-50, -40, -30, -30, -30, -30, -40, -50]]

    bishop = [[-20, -10, -10, -10, -10, -10, -10, -20],
              [-10, 5, 0, 0, 0, 0, 5, -10],
              [-10, 10, 10, 10, 10, 10, 10, -10],
              [-10, 0, 10, 10, 10, 10, 0, -10],
              [-10, 5, 5, 10, 10, 5, 5, -10],
              [-10, 0, 5, 10, 10, 5, 0, -10],
              [-10, 0, 0, 0, 0, 0, 0, -10],
              [-20, -10, -10, -10, -10, -10, -10, -20]]

    rook = [[0, 0, 0, 5, 5, 0, 0, 0],
            [-5, 0, 0, 0, 0, 0, 0, -5],
            [-5, 0, 0, 0, 0, 0, 0, -5],
            [-5, 0, 0, 0, 0, 0, 0, -5],
            [-5, 0, 0, 0, 0, 0, 0, -5],
            [-5, 0, 0, 0, 0, 0, 0, -5],
            [5, 10, 10, 10, 10, 10, 10, 5],
            [0, 0, 0, 0, 0, 0, 0, 0]]

    queen = [[-20, -10, -10, -5, -5, -10, -10, -20],
             [-10, 0, 5, 0, 0, 0, 0, -10],
             [-10, 5, 5, 5, 5, 5, 0, -10],
             [0, 0, 5, 5, 5, 5, 0, -5],
             [-5, 0, 5, 5, 5, 5, 0, -5],
             [-10, 0, 5, 5, 5, 5, 0, -10],
             [-10, 0, 0, 0, 0, 0, 0, -10],
             [-20, -10, -10, -5, -5, -10, -10, -20]]

    king_mg = [[20, 30, 10, 0, 0, 10, 30, 20],
               [20, 20, 0, 0, 0, 0, 20, 20],
               [-10, -20, -20, -20, -20, -20, -20, -10],
               [-20, -30, -30, -40, -40, -30, -30, -20],
               [-30, -40, -40, -50, -50, -40, -40, -30],
               [-30, -40, -40, -50, -50, -40, -40, -30],
               [-30, -40, -40, -50, -50, -40, -40, -30],
               [-30, -40, -40, -50, -50, -40, -40, -30]]

    king_eg = [[-50, -30, -30, -30, -30, -30, -30, -50],
               [-30, -30, 0, 0, 0, 0, -30, -30],
               [-30, -10, 20, 30, 30, 20, -10, -30],
               [-30, -10, 30, 40, 40, 30, -10, -30],
               [-30, -10, 30, 40, 40, 30, -10, -30],
               [-30, -10, 20, 30, 30, 20, -10, -30],
               [-30, -20, -10, 0, 0, -10, -20, -30],
               [-50, -40, -30, -20, -20, -30, -40, -50]]

    if piece == 'pawn':
        if player_color == chess.WHITE:
            return pawn[square // 8][square % 8]
        return pawn[7 - (square // 8)][7 - (square % 8)]

    if piece == 'knight':
        if player_color == chess.WHITE:
            return knight[square // 8][square % 8]
        return knight[7 - (square // 8)][7 - (square % 8)]

    if piece == 'bishop':
        if player_color == chess.WHITE:
            return bishop[square // 8][square % 8]
        return bishop[7 - (square // 8)][7 - (square % 8)]

    if piece == 'rook':
        if player_color == chess.WHITE:
            return rook[square // 8][square % 8]
        return rook[7 - (square // 8)][7 - (square % 8)]

    if piece == 'queen':
        if player_color == chess.WHITE:
            return queen[square // 8][square % 8]
        return queen[7 - (square // 8)][7 - (square % 8)]

    if piece == 'king':
        if player_color == chess.WHITE:
            if is_endgame(board):
                return king_eg[square // 8][square % 8]
            return king_mg[square // 8][square % 8]

        if is_endgame(board):
            return king_eg[7 - (square // 8)][7 - (square % 8)]
        return king_mg[7 - (square // 8)][7 - (square % 8)]


piece_values = {
    chess.KING: 20000,
    chess.QUEEN: 900,
    chess.ROOK: 500,
    chess.BISHOP: 330,
    chess.KNIGHT: 320,
    chess.PAWN: 100
}


def is_endgame(board):
    # endgame is (very oversimplified) defined as less than 10 pieces on the board
    white_pawns = board.pieces(chess.PAWN, chess.WHITE)
    white_knights = board.pieces(chess.KNIGHT, chess.WHITE)
    white_bishops = board.pieces(chess.BISHOP, chess.WHITE)
    white_rooks = board.pieces(chess.ROOK, chess.WHITE)
    white_queen = board.pieces(chess.QUEEN, chess.WHITE)

    black_pawns = board.pieces(chess.PAWN, chess.BLACK)
    black_knights = board.pieces(chess.KNIGHT, chess.BLACK)
    black_bishops = board.pieces(chess.BISHOP, chess.BLACK)
    black_rooks = board.pieces(chess.ROOK, chess.BLACK)
    black_queen = board.pieces(chess.QUEEN, chess.BLACK)

    piece_count = len(white_pawns) + len(white_knights) + len(white_bishops) + len(white_rooks) + len(white_queen) + \
                  len(black_pawns) + len(black_knights) + len(black_bishops) + len(black_rooks) + len(black_queen)

    return piece_count < 10


def evaluate_position(board: chess.Board, maximizing: bool):
    # collect material of players
    white_material = 0
    black_material = 0

    white_pawns = board.pieces(chess.PAWN, chess.WHITE)
    white_knights = board.pieces(chess.KNIGHT, chess.WHITE)
    white_bishops = board.pieces(chess.BISHOP, chess.WHITE)
    white_rooks = board.pieces(chess.ROOK, chess.WHITE)
    white_queen = board.pieces(chess.QUEEN, chess.WHITE)

    for square in white_pawns:
        square_value = get_positional_value_for_piece('pawn', square, chess.WHITE)
        white_material += piece_values[chess.PAWN] + square_value
    for square in white_knights:
        square_value = get_positional_value_for_piece('knight', square, chess.WHITE)
        white_material += piece_values[chess.KNIGHT] + square_value
    for square in white_bishops:
        square_value = get_positional_value_for_piece('bishop', square, chess.WHITE)
        white_material += piece_values[chess.BISHOP] + square_value
    for square in white_rooks:
        square_value = get_positional_value_for_piece('rook', square, chess.WHITE)
        white_material += piece_values[chess.ROOK] + square_value
    for square in white_queen:
        square_value = get_positional_value_for_piece('queen', square, chess.WHITE)
        white_material += piece_values[chess.QUEEN] + square_value

    black_pawns = board.pieces(chess.PAWN, chess.BLACK)
    black_knights = board.pieces(chess.KNIGHT, chess.BLACK)
    black_bishops = board.pieces(chess.BISHOP, chess.BLACK)
    black_rooks = board.pieces(chess.ROOK, chess.BLACK)
    black_queen = board.pieces(chess.QUEEN, chess.BLACK)

    for square in black_pawns:
        square_value = get_positional_value_for_piece('pawn', square, chess.BLACK)
        black_material += piece_values[chess.PAWN] + square_value
    for square in black_knights:
        square_value = get_positional_value_for_piece('knight', square, chess.BLACK)
        black_material += piece_values[chess.KNIGHT] + square_value
    for square in black_bishops:
        square_value = get_positional_value_for_piece('bishop', square, chess.BLACK)
        black_material += piece_values[chess.BISHOP] + square_value
    for square in black_rooks:
        square_value = get_positional_value_for_piece('rook', square, chess.BLACK)
        black_material += piece_values[chess.ROOK] + square_value
    for square in black_queen:
        square_value = get_positional_value_for_piece('queen', square, chess.BLACK)
        black_material += piece_values[chess.QUEEN] + square_value

    # add kings
    white_material += piece_values[chess.KING] + get_positional_value_for_piece('king', board.king(chess.WHITE),
                                                                                chess.WHITE, board)
    black_material += piece_values[chess.KING] + get_positional_value_for_piece('king', board.king(chess.BLACK),
                                                                                chess.BLACK, board)

    evaluation = white_material - black_material

    return evaluation
