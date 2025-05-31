import time
from src.game_engine.move_generator import valid_moves
from src.game_engine.othello import apply_move, game_over
from src.game_engine import BOARD_SIZE
from src.heuristics import evaluate  # Solo si realmente estás usando `evaluate`

MAX_DEPTH = 4
TIME_LIMIT = 2.8

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

def stability_score(board, color):
    score = 0
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r][c] == color:
                if (r, c) in CORNERS:
                    score += 25
                elif (r, c) in ADJACENTS:
                    score -= 12
                elif (r, c) in EDGES:
                    score += 5
    return score

def mobility(board, color):
    return len(valid_moves(board, color))

def super_heuristic(board, color):
    opp = -color
    return (
        + stability_score(board, color) - stability_score(board, opp)
        + 10 * (mobility(board, color) - mobility(board, opp))
        + 1 * (
            sum(cell == color for row in board for cell in row)
            - sum(cell == opp for row in board for cell in row)
        )
    )

def minimax(board, color, depth, alpha, beta, maximizing, root_color, start_time):
    if depth == 0 or game_over(board) or time.perf_counter() - start_time > TIME_LIMIT:
        return super_heuristic(board, root_color)

    moves = valid_moves(board, color)
    if not moves:
        return minimax(board, -color, depth - 1, alpha, beta, not maximizing, root_color, start_time)

    if maximizing:
        value = float('-inf')
        for move in moves:
            new_board = apply_move(board, color, move)
            value = max(value, minimax(new_board, -color, depth - 1, alpha, beta, False, root_color, start_time))
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value
    else:
        value = float('inf')
        for move in moves:
            new_board = apply_move(board, color, move)
            value = min(value, minimax(new_board, -color, depth - 1, alpha, beta, True, root_color, start_time))
            beta = min(beta, value)
            if beta <= alpha:
                break
        return value

def get_move(board, color):
    start = time.perf_counter()
    best_value = float('-inf')
    best_move = None
    for move in valid_moves(board, color):
        new_board = apply_move(board, color, move)
        value = minimax(new_board, -color, MAX_DEPTH - 1, float('-inf'), float('inf'), False, color, start)
        if value > best_value:
            best_value = value
            best_move = move
    return best_move
