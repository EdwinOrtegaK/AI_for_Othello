# run_match.py
import time, random, statistics
from src.game_engine.board import initial_board, print_board
from src.game_engine.move_generator import valid_moves
from src.game_engine.othello import apply_move, game_over, winner
#from src.ai.minimaxbasic import get_move as player_white
from src.ai.minimax import get_best_move as player_white
#from src.ai.mcts import get_move as player_white
from src.ai.ai_max import get_move as player_black

TIME_LIMIT = 2.8
SAFE_FALLBACK = True

def time_move(player_func, board, color):
    """Devuelve (move, tiempo) asegurando jugada válida y dentro de tiempo."""
    start = time.perf_counter()
    move = player_func(board, color)
    elapsed = time.perf_counter() - start

    valid = valid_moves(board, color)

    if not valid:
        return None, elapsed #salto de turno por falta de movimientos 

    if SAFE_FALLBACK and (elapsed > TIME_LIMIT or move not in valid):
        move = random.choice(valid)

    return move, elapsed


def main():
    board = initial_board()
    print_board(board)
    turn = -1  # negras inician

    while not game_over(board):
        if turn == -1:
            move, t = time_move(player_black, board, turn)
            if move is None:
                print("Black skips turn.")
                turn *= -1
                continue
            print(f"Black move {move} in {t:.2f}s")
        else:
            move, t = time_move(player_white, board, turn)
            if move is None:
                print("White skips turn.")
                turn *= -1
                continue
            print(f"White move {move} in {t:.2f}s")

        board = apply_move(board, turn, move)
        print_board(board)
        turn *= -1

    result = winner(board)
    if result == -1:
        print("Black wins!")
    elif result == 1:
        print("White wins!")
    else:
        print("Draw!")

if __name__ == "__main__":
    main()
