"""
Generación y validación de movimientos.
"""

from . import BOARD_SIZE, DIRECTIONS, EMPTY
from . import WHITE, BLACK   # Para legibilidad

__all__ = [
    "is_on_board",
    "valid_moves",
    "flips_for_move",
]

def is_on_board(r: int, c: int) -> bool:
    return 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE

def flips_for_move(board, color, row, col):
    """
    Devuelve la lista de fichas a voltear si (row,col) se juega con 'color'.
    Si la jugada NO es válida, devuelve lista vacía.
    """
    if board[row][col] != EMPTY:
        return []

    opponent = -color
    flips = []

    for dr, dc in DIRECTIONS:
        r, c = row + dr, col + dc
        line = []
        while is_on_board(r, c) and board[r][c] == opponent:
            line.append((r, c))
            r += dr
            c += dc
        if is_on_board(r, c) and board[r][c] == color and line:
            flips.extend(line)

    return flips

def valid_moves(board, color):
    """
    Retorna todas las jugadas válidas como lista de tuplas (row,col)
    para el jugador 'color'.
    """
    moves = []
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if flips_for_move(board, color, r, c):
                moves.append((r, c))
    return moves
