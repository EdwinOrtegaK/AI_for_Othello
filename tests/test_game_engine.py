import unittest
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.game_engine.board import initial_board
from src.game_engine.move_generator import valid_moves
from src.game_engine.othello import apply_move, game_over, winner
from src.ai.minimax import get_best_move

class TestGameEngine(unittest.TestCase):

    def test_initial_moves(self):
        board = initial_board()
        # En la apertura, ambos tienen 4 jugadas posibles
        self.assertEqual(len(valid_moves(board, 1)), 4)
        self.assertEqual(len(valid_moves(board, -1)), 4)

    def test_simple_play(self):
        board = initial_board()
        move = (2, 3)     # Negra juega arriba de la ficha inicial
        board = apply_move(board, -1, move)
        # Luego de la jugada, blancas tienen movimientos
        self.assertTrue(len(valid_moves(board, 1)) > 0)

    def test_end_game(self):
        board = initial_board()
        # Forzamos fin (rellenamos todo de blancas)
        board = [[1]*8 for _ in range(8)]
        self.assertTrue(game_over(board))
        self.assertEqual(winner(board), 1)

class TestMinimax(unittest.TestCase):
    def test_minimax_returns_valid_move(self):
        board = initial_board()
        move = get_best_move(board, -1, time_limit=0.2)
        self.assertIn(move, valid_moves(board, -1))

if __name__ == "__main__":
    unittest.main()
