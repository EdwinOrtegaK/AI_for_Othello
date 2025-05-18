"""
Aplicar jugadas y determinar estado de la partida.
"""

from . import EMPTY, WHITE, BLACK, BOARD_SIZE
from .move_generator import flips_for_move, valid_moves
from .board import copy_board

__all__ = [
    "apply_move",
    "count_pieces",
    "game_over",
    "winner",
]

def apply_move(board, color, move):
    """
    Aplica 'move' (row,col) sobre 'board' con el jugador 'color'
    y devuelve un nuevo tablero resultante. Si el movimiento no es válido
    lanza ValueError.
    """
    row, col = move
    flips = flips_for_move(board, color, row, col)
    if not flips:
        raise ValueError(f"Movimiento inválido: {move}")

    new_board = copy_board(board)
    new_board[row][col] = color
    for r, c in flips:
        new_board[r][c] = color
    return new_board

def count_pieces(board):
    """Cuenta fichas blancas y negras."""
    whites = sum(cell == WHITE for row in board for cell in row)
    blacks = sum(cell == BLACK for row in board for cell in row)
    return whites, blacks

def game_over(board):
    """
    Devuelve True si:
      - No hay casillas vacías, o
      - Ninguno de los dos jugadores tiene movimientos válidos
    """
    if all(cell != EMPTY for row in board for cell in row):
        return True
    return not valid_moves(board, WHITE) and not valid_moves(board, BLACK)

def winner(board):
    """Devuelve 1 si gana WHITE, -1 si gana BLACK, 0 en empate."""
    whites, blacks = count_pieces(board)
    if whites > blacks:
        return WHITE
    if blacks > whites:
        return BLACK
    return 0
