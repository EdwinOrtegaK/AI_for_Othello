"""
game_engine package
Centraliza constantes y utilidades comunes.
"""

BOARD_SIZE = 8          # 8×8
EMPTY, WHITE, BLACK = 0, 1, -1

# Direcciones (fila, col) en las 8 orientaciones posibles
DIRECTIONS = [
    (-1,  0),  # N
    (-1,  1),  # NE
    ( 0,  1),  # E
    ( 1,  1),  # SE
    ( 1,  0),  # S
    ( 1, -1),  # SW
    ( 0, -1),  # W
    (-1, -1),  # NW
]
