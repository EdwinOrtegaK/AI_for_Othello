"""
Funciones básicas de creación y manipulación del tablero.
"""

from copy import deepcopy
from . import BOARD_SIZE, EMPTY, WHITE, BLACK

__all__ = ["initial_board", "copy_board", "print_board"]

def initial_board():
    """Devuelve un tablero 8×8 en el estado inicial de Othello."""
    board = [[EMPTY] * BOARD_SIZE for _ in range(BOARD_SIZE)]
    mid = BOARD_SIZE // 2
    board[mid - 1][mid - 1] = WHITE
    board[mid - 1][mid]     = BLACK
    board[mid][mid - 1]     = BLACK
    board[mid][mid]         = WHITE
    return board

def copy_board(board):
    """Retorna una copia profunda del tablero."""
    return deepcopy(board)

def print_board(board):
    """Imprime el tablero en consola (útil para debug)."""
    symbols = {WHITE: "○", BLACK: "●", EMPTY: "."}
    for row in board:
        print(" ".join(symbols[cell] for cell in row))
    print()
