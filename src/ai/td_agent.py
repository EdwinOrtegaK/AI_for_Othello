import random
import pickle
from collections import defaultdict
from src.game_engine.move_generator import valid_moves
from src.game_engine.othello import apply_move, game_over, winner
from src.game_engine import BLACK, WHITE

# ------------------ PARÁMETROS DE APRENDIZAJE ------------------
ALPHA = 0.1     # Tasa de aprendizaje
GAMMA = 0.99    # Factor de descuento
EPSILON = 0.1   # Exploración ε-greedy

# ------------------ TABLA DE VALORES DE ESTADO ------------------
V = defaultdict(float)

def board_to_key(board):
    """Convierte el tablero en una tupla inmutable para usar como clave."""
    return tuple(map(tuple, board))

def get_state_value(board):
    return V[board_to_key(board)]

def choose_move(board, color):
    """Política ε-greedy basada en V(s)"""
    moves = valid_moves(board, color)
    if not moves:
        return None
    if random.random() < EPSILON:
        return random.choice(moves)
    return max(moves, key=lambda m: get_state_value(apply_move(board, color, m)))

# ------------------ JUEGO Y ENTRENAMIENTO TD(0) ------------------

def play_game(learn=True, opponent_fn=None):
    """Juega una partida (vs otro bot o self-play). Si learn=True, entrena."""
    board = [[0] * 8 for _ in range(8)]
    board[3][3], board[3][4] = WHITE, BLACK
    board[4][3], board[4][4] = BLACK, WHITE
    player = BLACK
    trajectory = []

    while not game_over(board):
        if player == BLACK or opponent_fn is None:
            move = choose_move(board, player)
        else:
            move = opponent_fn(board, player)

        if move:
            if learn and player == BLACK:
                trajectory.append(board_to_key(board))
            board = apply_move(board, player, move)

        player = -player

    final_result = winner(board)

    if learn:
        for i in range(len(trajectory) - 1):
            s, s_next = trajectory[i], trajectory[i + 1]
            V[s] += ALPHA * (GAMMA * V[s_next] - V[s])
        if trajectory:
            final_state = trajectory[-1]
            reward = 1 if final_result == BLACK else -1 if final_result == WHITE else 0
            V[final_state] += ALPHA * (reward - V[final_state])

    return final_result


def save_values(filename="td_value_table.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(dict(V), f)

def load_values(filename="td_value_table.pkl"):
    global V
    with open(filename, "rb") as f:
        loaded = pickle.load(f)
        V = defaultdict(float, loaded)


def get_move(board, color):
    """Función estándar para que el bot juegue en torneos."""
    moves = valid_moves(board, color)
    if not moves:
        return None
    return choose_move(board, color)
