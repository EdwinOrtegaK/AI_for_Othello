import itertools
import time
from src.game_engine.board import initial_board
from src.game_engine.move_generator import valid_moves
from src.game_engine.othello import apply_move, game_over, winner

from src.ai.minimaxbasic import get_move as minimaxbasic_move
from src.ai.minimax import get_best_move as minimax_move
from src.ai.mcts import get_move as mcts_move
from src.ai.ai_max import get_move as aimax_move

# Diccionario: nombre → función de movimiento
IA_MOVES = {
    "MinimaxBasic": minimaxbasic_move,
    "Minimax": minimax_move,
    "MCTS": mcts_move,
    "AI_Max": aimax_move
}

def run_game(black_func, white_func):
    board = initial_board()
    current_player = -1  # -1 = negras, 1 = blancas

    while not game_over(board):
        move_func = black_func if current_player == -1 else white_func
        moves = valid_moves(board, current_player)

        if moves:
            move = move_func(board, current_player)
            if move in moves:
                board = apply_move(board, current_player, move)
            else:
                # Movimiento inválido → pierde
                return 1 if current_player == -1 else -1
        # Sin movimientos → pasa turno
        current_player *= -1

    return winner(board)  # -1 = negras, 1 = blancas, 0 = empate

def main():
    results = []
    ia_names = list(IA_MOVES.keys())
    matches = list(itertools.combinations_with_replacement(ia_names, 2))  # IA1 == IA2 incluido

    for idx, (ia1, ia2) in enumerate(matches, start=1):
        black_wins = 0
        white_wins = 0
        draws = 0

        # IA1 como negras
        for _ in range(2):
            result = run_game(IA_MOVES[ia1], IA_MOVES[ia2])
            if result == -1:
                black_wins += 1
            elif result == 1:
                white_wins += 1
            else:
                draws += 1

        # IA2 como negras
        for _ in range(2):
            result = run_game(IA_MOVES[ia2], IA_MOVES[ia1])
            if result == -1:
                white_wins += 1  # IA1 ahora es blanca
            elif result == 1:
                black_wins += 1  # IA1 ahora es blanca
            else:
                draws += 1

        results.append({
            "Partida": f"{ia1} vs {ia2}",
            "Ganó Negras": black_wins,
            "Ganó Blancas": white_wins,
            "Empates": draws
        })

        # Mostrar progreso
        print(f"✔ Enfrentamiento {idx}/{len(matches)} finalizado: {ia1} vs {ia2}")

    # Imprimir tabla
    print(f"\n{'Partida':30} | {'Ganó Negras':13} | {'Ganó Blancas':14} | {'Empates':7}")
    print("-" * 75)
    for r in results:
        print(f"{r['Partida']:30} | {r['Ganó Negras']:13} | {r['Ganó Blancas']:14} | {r['Empates']:7}")
    print(f"\nTotal de partidas jugadas: {len(matches) * 4}")


if __name__ == "__main__":
    main()
