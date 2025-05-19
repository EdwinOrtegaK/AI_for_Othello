# run_match.py
import time, random, statistics
from src.game_engine.board import initial_board, print_board
from src.game_engine.move_generator import valid_moves
from src.game_engine.othello import apply_move, game_over, winner
from src.ai.minimax import get_best_move

board = initial_board()
print_board(board) 
turn = -1   # negras inician

TIME_LIMIT = 2.8         # segundos asignados a la IA
SAFE_FALLBACK = True     # si True: usa jugada aleatoria si se pasa de tiempo

# Estadísticas de tiempo
times_white, times_black = [], []

def time_move(board, color):
    """Devuelve (move, elapsed) asegurando jugada válida y dentro de tiempo."""
    start = time.perf_counter()
    move  = get_best_move(board, color, time_limit=TIME_LIMIT)
    elapsed = time.perf_counter() - start

    # Fallback si tarda demasiado o jugada inválida
    if SAFE_FALLBACK and (elapsed > TIME_LIMIT or move not in valid_moves(board, color)):
        move = random.choice(valid_moves(board, color))
    return move, elapsed

while not game_over(board):
    moves = valid_moves(board, turn)
    if moves:
        move, elapsed = time_move(board, turn)
        board = apply_move(board, turn, move)

        # Guarda tiempo y muestra info
        (times_black if turn == -1 else times_white).append(elapsed)
        color_name = "Negras" if turn == -1 else "Blancas"
        print_board(board)
        print(f"{color_name} jugaron {move} en {elapsed:.3f} s\n")

    turn = -turn  # cambia de jugador

print("Resultado final — Ganador:",
      {1: "Blancas", -1: "Negras", 0: "Empate"}[winner(board)])

def stats(label, lst):
    if lst:
        print(f"{label}: min {min(lst):.3f}s · máx {max(lst):.3f}s · prom {statistics.mean(lst):.3f}s  "
              f"en {len(lst)} jugadas")

stats("Tiempos Blancas", times_white)
stats("Tiempos Negras",  times_black)
