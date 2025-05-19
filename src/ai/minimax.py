"""
Minimax con poda Alpha-Beta + iterative deepening.
La función pública es get_best_move(board, color, time_limit=2.8)
"""

import time
from typing import Tuple, List

from ..game_engine.move_generator import valid_moves
from ..game_engine.othello import apply_move, game_over
from ..heuristics import evaluate
from ..game_engine import BOARD_SIZE, WHITE, BLACK

MAX_DEPTH_START = 3       # profundidad inicial
SAFETY_MARGIN   = 0.05    # colchón para cortar la búsqueda (segundos)

# Conjuntos estáticos para ordenar jugadas
CORNERS = {(0, 0), (0, 7), (7, 0), (7, 7)}
EDGES   = (
    {(0, c) for c in range(BOARD_SIZE)} |
    {(7, c) for c in range(BOARD_SIZE)} |
    {(r, 0) for r in range(BOARD_SIZE)} |
    {(r, 7) for r in range(BOARD_SIZE)}
) - CORNERS   # quitar las esquinas que ya están en CORNERS

def get_best_move(board: List[List[int]],
                  color: int,
                  time_limit: float = 2.8) -> Tuple[int, int]:
    """
    Devuelve (row, col) usando búsqueda iterativa hasta time_limit segundos.
    """
    start = time.perf_counter()
    best_move = None
    depth = MAX_DEPTH_START

    while True:
        remaining = time_limit - (time.perf_counter() - start)
        if remaining < SAFETY_MARGIN:
            break  # sin tiempo para otra iteración

        move, _ = alphabeta_root(board, color, depth, start, time_limit)
        if move is not None:
            best_move = move
        depth += 1

    return best_move

def ordering_score(board, move, color) -> int:
    """
    Heurística estática + 1-ply barata para ordenar movimientos.
    • Esquinas  → prioridad máxima
    • Bordes    → prioridad intermedia
    • Evaluación heurística tras aplicar la jugada para desempatar
    """
    if move in CORNERS:
        return 10_000

    base = 5_000 if move in EDGES else 0

    # 1-ply look-ahead: aplica la jugada y puntúa con evaluate()
    child_board = apply_move(board, color, move)
    return base + evaluate(child_board, color)

def alphabeta_root(board, color, depth, t_start, t_limit):
    """Nodo raíz con ordenamiento previo de las jugadas."""
    moves = valid_moves(board, color)
    # Ordenar de mayor a menor puntuación estática
    moves.sort(key=lambda m: ordering_score(board, m, color), reverse=True)

    best_score = float('-inf')
    best_move = None

    for move in moves:
        new_board = apply_move(board, color, move)
        score = alphabeta(new_board, -color, depth - 1,
                          float('-inf'), float('inf'),
                          t_start, t_limit, False, color)
        if score > best_score:
            best_score = score
            best_move = move

    return best_move, best_score

def alphabeta(board, color, depth, alpha, beta,
              t_start, t_limit, maximizing, root_color):
    """Versión recursiva con poda Alpha-Beta."""
    # Corte por tiempo
    if time.perf_counter() - t_start > t_limit:
        return evaluate(board, root_color)

    # Corte por profundidad o fin de juego
    if depth == 0 or game_over(board):
        return evaluate(board, root_color)

    moves = valid_moves(board, color)
    if not moves:
        # Sin movimientos válidos: pasa turno
        return alphabeta(board, -color, depth - 1,
                         alpha, beta, t_start, t_limit,
                         not maximizing, root_color)

    # ───── MAX ───────────────────────────────────────────────
    if maximizing:
        value = float('-inf')
        # Ordenar hijos (opcional, pero ayuda en ramas interiores)
        moves.sort(key=lambda m: ordering_score(board, m, color), reverse=True)

        for move in moves:
            new_board = apply_move(board, color, move)
            value = max(value,
                        alphabeta(new_board, -color, depth - 1,
                                  alpha, beta, t_start, t_limit,
                                  False, root_color))
            alpha = max(alpha, value)
            if alpha >= beta:  # poda
                break
        return value

    # ───── MIN ───────────────────────────────────────────────
    else:
        value = float('inf')
        moves.sort(key=lambda m: ordering_score(board, m, color))  # ascendente

        for move in moves:
            new_board = apply_move(board, color, move)
            value = min(value,
                        alphabeta(new_board, -color, depth - 1,
                                  alpha, beta, t_start, t_limit,
                                  True, root_color))
            beta = min(beta, value)
            if beta <= alpha:  # poda
                break
        return value