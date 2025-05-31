import time
import random
from ai.ai_max import get_move as ai_max_move
from ai.mcts import get_move as mcts_move
from ai.minimax import get_best_move as minimax_move
from ai.minimaxbasic import get_move as basic_move
from ai.td_agent import get_move, play_game, save_values, V, ALPHA, GAMMA, board_to_key
from game_engine.move_generator import valid_moves
from game_engine.othello import apply_move, game_over, winner

N_GAMES = 200

black_wins = 0
white_wins = 0
draws = 0

opponents = [ai_max_move, mcts_move, minimax_move, basic_move]

print("Entrenando TD Agent contra múltiples bots (turnos alternados)...")

for i in range(1, N_GAMES + 1):
    td_color = -1 if i % 2 == 1 else 1  # impar: TD es negro, par: TD es blanco
    opponent_move = random.choice(opponents)

    def td_perspective_play():
        board = [[0]*8 for _ in range(8)]
        board[3][3], board[3][4] = 1, -1
        board[4][3], board[4][4] = -1, 1
        player = -1
        trajectory = []

        while not game_over(board):
            if player == td_color:
                move = get_move(board, player)
                trajectory.append((player, board))
            else:
                move = opponent_move(board, player)

            if move:
                board = apply_move(board, player, move)
            player = -player

        result = winner(board)

        if trajectory:
            for j in range(len(trajectory) - 1):
                _, s = trajectory[j]
                _, s_next = trajectory[j + 1]
                V[board_to_key(s)] += ALPHA * (
                    GAMMA * V[board_to_key(s_next)] - V[board_to_key(s)]
                )

            last_state = board_to_key(trajectory[-1][1])
            reward = (
                1 if result == td_color else
                -1 if result == -td_color else
                0
            )
            V[last_state] += ALPHA * (reward - V[last_state])

        return result

    result = td_perspective_play()

    if result == -1:
        black_wins += 1
    elif result == 1:
        white_wins += 1
    else:
        draws += 1

    if i % 20 == 0:
        print(f"Partida {i}/{N_GAMES} - 🟤 TD (Negro): {black_wins}, ⚪ TD (Blanco): {white_wins}, 🤝 Empates: {draws}")

save_values("td_vs_all.pkl")

print("\n✅ Entrenamiento completado.")
print(f"Totales en {N_GAMES} partidas:")
print(f"  🟤 TD Agent jugando como negro: {black_wins}")
print(f"  ⚪ TD Agent jugando como blanco: {white_wins}")
print(f"  🤝 Empates: {draws}")
