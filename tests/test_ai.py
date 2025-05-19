import unittest, time
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.game_engine.board import initial_board
from src.ai.minimax import get_best_move
from src.game_engine.move_generator import valid_moves
from src.heuristics import evaluate

class TestAI(unittest.TestCase):

    def test_evaluate_symmetry(self):
        board = initial_board()
        # La evaluación inicial debe ser 0 (tablero equilibrado)
        self.assertEqual(evaluate(board, 1), 0)
        self.assertEqual(evaluate(board, -1), 0)

    def test_get_best_move_time(self):
        board = initial_board()
        start = time.perf_counter()
        move = get_best_move(board, -1, time_limit=0.5)
        elapsed = time.perf_counter() - start
        # Debe terminar antes del límite y ser un movimiento válido
        self.assertLess(elapsed, 0.55)
        self.assertIn(move, valid_moves(board, -1))

if __name__ == "__main__":
    unittest.main()
