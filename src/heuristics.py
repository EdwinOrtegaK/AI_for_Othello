"""
Funciones de evaluación de tablero para Othello.
Se usan valores basados en literatura clásica.
"""

from src.game_engine import BOARD_SIZE, WHITE, BLACK
from src.game_engine.move_generator import valid_moves

# Pesos heurísticos
CORNER_WEIGHT      = 25
ADJACENT_PENALTY   = -12
EDGE_WEIGHT        = 5
MOBILITY_WEIGHT    = 10
PIECE_DIFF_WEIGHT  = 1

# Coordenadas de esquinas y adyacentes
CORNERS = {(0, 0), (0, 7), (7, 0), (7, 7)}
ADJACENTS = {
    (0, 1), (1, 0), (1, 1),
    (0, 6), (1, 6), (1, 7),
    (6, 0), (6, 1), (7, 1),
    (6, 6), (6, 7), (7, 6)
}
EDGES = (
    {(0, c) for c in range(BOARD_SIZE)} |
    {(7, c) for c in range(BOARD_SIZE)} |
    {(r, 0) for r in range(BOARD_SIZE)} |
    {(r, 7) for r in range(BOARD_SIZE)}
) - CORNERS

def evaluate(board, color):
    """Retorna score desde la perspectiva de *color* (cuanto mayor, mejor)."""
    opponent = -color
    score = 0

    # 1. Piezas en esquinas
    for pos in CORNERS:
        if board[pos[0]][pos[1]] == color:
            score += CORNER_WEIGHT
        elif board[pos[0]][pos[1]] == opponent:
            score -= CORNER_WEIGHT

    # 2. Casillas adyacentes a esquinas (penalidades)
    for pos in ADJACENTS:
        if board[pos[0]][pos[1]] == color:
            score += ADJACENT_PENALTY
        elif board[pos[0]][pos[1]] == opponent:
            score -= ADJACENT_PENALTY

    # 3. Bordes (excluyendo esquinas)
    for pos in EDGES:
        if board[pos[0]][pos[1]] == color:
            score += EDGE_WEIGHT
        elif board[pos[0]][pos[1]] == opponent:
            score -= EDGE_WEIGHT

    # 4. Movilidad
    my_moves = len(valid_moves(board, color))
    op_moves = len(valid_moves(board, opponent))
    score += MOBILITY_WEIGHT * (my_moves - op_moves)

    # 5. Diferencia de piezas (paridad)
    piece_diff = (
        sum(cell == color for row in board for cell in row)
        - sum(cell == opponent for row in board for cell in row)
    )
    score += PIECE_DIFF_WEIGHT * piece_diff

    return score
