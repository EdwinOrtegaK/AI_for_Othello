"""
Funciones de evaluación de tablero para Othello.
Se usan valores basados en literatura clásica.
"""

from .game_engine import BOARD_SIZE, WHITE, BLACK
from .game_engine.move_generator import valid_moves

# Pesos heurísticos
CORNER_WEIGHT      = 25
CORNER_ADJ_WEIGHT  = -12   # casillas junto a la esquina son malas
EDGE_WEIGHT        = 5
MOBILITY_WEIGHT    = 8
PIECE_DIFF_WEIGHT  = 1

# Coordenadas de esquinas y adyacentes
CORNERS = [(0,0), (0,7), (7,0), (7,7)]
CORNER_ADJ = [
    (0,1),(1,0),(1,1), (0,6),(1,6),(1,7),
    (6,0),(6,1),(7,1), (6,6),(6,7),(7,6)
]

def evaluate(board, color):
    """Retorna score desde la perspectiva de *color* (cuanto mayor, mejor)."""
    opponent = -color
    score = 0

    # 1. Piezas en esquinas
    for r, c in CORNERS:
        if board[r][c] == color:
            score += CORNER_WEIGHT
        elif board[r][c] == opponent:
            score -= CORNER_WEIGHT

    # 2. Casillas adyacentes a esquinas
    for r, c in CORNER_ADJ:
        if board[r][c] == color:
            score += CORNER_ADJ_WEIGHT
        elif board[r][c] == opponent:
            score -= CORNER_ADJ_WEIGHT

    # 3. Fichas en los bordes (no esquinas)
    for i in range(BOARD_SIZE):
        for (r, c) in [(0, i), (7, i), (i, 0), (i, 7)]:
            if (r, c) in CORNERS or (r, c) in CORNER_ADJ:
                continue
            if board[r][c] == color:
                score += EDGE_WEIGHT
            elif board[r][c] == opponent:
                score -= EDGE_WEIGHT

    # 4. Movilidad
    my_moves  = len(valid_moves(board, color))
    op_moves  = len(valid_moves(board, opponent))
    score += MOBILITY_WEIGHT * (my_moves - op_moves)

    # 5. Diferencia de piezas
    piece_diff = sum(cell == color for row in board for cell in row) - \
                 sum(cell == opponent for row in board for cell in row)
    score += PIECE_DIFF_WEIGHT * piece_diff

    return score
