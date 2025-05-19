"""
Minimax con poda Alpha-Beta + iterative deepening.
La función pública es get_best_move(board, color, time_limit=2.8)
"""

import time
from typing import Tuple, List
from ..game_engine.move_generator import valid_moves
from ..game_engine.othello import apply_move, game_over
from ..heuristics import evaluate
from ..game_engine import WHITE, BLACK

MAX_DEPTH_START = 2   # profundidad inicial

def get_best_move(board: List[List[int]], color: int, time_limit: float = 2.8) -> Tuple[int,int]:
    """
    Devuelve (row,col) usando búsq. iterativa hasta time_limit segundos.
    """
    start = time.perf_counter()
    best_move = None
    depth = MAX_DEPTH_START

    while True:
        remaining = time_limit - (time.perf_counter() - start)
        if remaining < 0.05:  # colchón de seguridad
            break
        move, _ = alphabeta_root(board, color, depth, start, time_limit)
        if move is not None:
            best_move = move
        depth += 1
    return best_move

# ---------------------------------------------------------------------

def alphabeta_root(board, color, depth, t_start, t_limit):
    best_score = float('-inf')
    best_move  = None
    for move in valid_moves(board, color):
        new_board = apply_move(board, color, move)
        score = alphabeta(new_board, -color, depth-1,
                          float('-inf'), float('inf'),
                          t_start, t_limit, False, color)
        if score > best_score:
            best_score = score
            best_move  = move
    return best_move, best_score

def alphabeta(board, color, depth, alpha, beta,
              t_start, t_limit, maximizing, root_color):
    # Timeout check
    if time.perf_counter() - t_start > t_limit:
        return evaluate(board, root_color)

    if depth == 0 or game_over(board):
        return evaluate(board, root_color)

    moves = valid_moves(board, color)
    if not moves:
        # Sin movimientos: pasa turno
        return alphabeta(board, -color, depth-1, alpha, beta,
                         t_start, t_limit, not maximizing, root_color)

    if maximizing:
        value = float('-inf')
        for move in moves:
            new_board = apply_move(board, color, move)
            value = max(value,
                        alphabeta(new_board, -color, depth-1,
                                  alpha, beta, t_start, t_limit,
                                  False, root_color))
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value
    else:
        value = float('inf')
        for move in moves:
            new_board = apply_move(board, color, move)
            value = min(value,
                        alphabeta(new_board, -color, depth-1,
                                  alpha, beta, t_start, t_limit,
                                  True, root_color))
            beta = min(beta, value)
            if beta <= alpha:
                break
        return value
