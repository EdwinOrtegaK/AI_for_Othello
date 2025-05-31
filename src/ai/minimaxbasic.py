"""
Minimax básico sin poda.
Interfaz: get_move(board, color)
"""

from game_engine.move_generator import valid_moves
from game_engine.othello import apply_move, game_over
from heuristics import evaluate
from typing import List, Tuple

MAX_DEPTH = 3  # Profundidad fija para limitar tiempo (ajustable)

def get_move(board: List[List[int]], color: int) -> Tuple[int, int]:
    """
    Selecciona la mejor jugada usando Minimax sin poda.
    """
    best_score = float('-inf')
    best_move = None

    for move in valid_moves(board, color):
        new_board = apply_move(board, color, move)
        score = minimax(new_board, -color, MAX_DEPTH - 1, False, color)
        if score > best_score:
            best_score = score
            best_move = move

    return best_move


def minimax(board: List[List[int]], color: int, depth: int, maximizing: bool, root_color: int) -> float:
    """
    Evaluación recursiva básica de minimax sin poda.
    """
    if depth == 0 or game_over(board):
        return evaluate(board, root_color)

    moves = valid_moves(board, color)

    if not moves:
        # Sin movimientos válidos: pasa turno
        return minimax(board, -color, depth - 1, not maximizing, root_color)

    if maximizing:
        best = float('-inf')
        for move in moves:
            new_board = apply_move(board, color, move)
            best = max(best, minimax(new_board, -color, depth - 1, False, root_color))
        return best
    else:
        best = float('inf')
        for move in moves:
            new_board = apply_move(board, color, move)
            best = min(best, minimax(new_board, -color, depth - 1, True, root_color))
        return best
