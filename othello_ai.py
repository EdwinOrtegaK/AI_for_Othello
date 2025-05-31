import random
from src.ai.td_agent import get_move, load_values
from src.game_engine.move_generator import valid_moves

# Cargamos el aprendizaje entrenado
load_values("td_vs_ai_max.pkl")

DIRECTIONS = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),          (0, 1),
    (1, -1),  (1, 0), (1, 1)
]

def in_bounds(x, y):
    return 0 <= x < 8 and 0 <= y < 8

def valid_movements(board, player):
    opponent = -player
    valid_moves_list = []

    for x in range(8):
        for y in range(8):
            if board[x][y] != 0:
                continue

            for dx, dy in DIRECTIONS:
                i, j = x + dx, y + dy
                found_opponent = False

                while in_bounds(i, j) and board[i][j] == opponent:
                    i += dx
                    j += dy
                    found_opponent = True

                if found_opponent and in_bounds(i, j) and board[i][j] == player:
                    valid_moves_list.append((x, y))
                    break

    return valid_moves_list

def ai_move(board, color):
    moves = valid_moves(board, color)
    if not moves:
        return None

    move = get_move(board, color)

    if move not in moves:
        return random.choice(moves)

    return move
