import time
import math
import random
from collections import defaultdict
from ..game_engine.move_generator import valid_moves
from ..game_engine.othello import apply_move, game_over, winner
from ..game_engine import BLACK, WHITE

TIME_LIMIT = 2.8
UCT_C = 1.41  # Parámetro de exploración (sqrt(2) por defecto)


class MCTSNode:
    def __init__(self, board, player, parent=None, move=None):
        self.board = board
        self.player = player
        self.parent = parent
        self.move = move
        self.children = []
        self.visits = 0
        self.wins = 0
        self.untried_moves = valid_moves(board, player)

    def is_fully_expanded(self):
        return len(self.untried_moves) == 0

    def best_child(self, c_param=UCT_C):
        choices = [
            (child.wins / child.visits) + c_param * math.sqrt(math.log(self.visits) / child.visits)
            for child in self.children
        ]
        return self.children[choices.index(max(choices))]

    def expand(self):
        move = self.untried_moves.pop()
        next_board = apply_move(self.board, self.player, move)
        next_player = -self.player
        child_node = MCTSNode(next_board, next_player, parent=self, move=move)
        self.children.append(child_node)
        return child_node

    def backpropagate(self, result):
        self.visits += 1
        if result == self.player:
            self.wins += 1
        elif result == 0:
            self.wins += 0.5  # empate
        if self.parent:
            self.parent.backpropagate(result)


def simulate_random_game(board, player):
    current_player = player
    while not game_over(board):
        moves = valid_moves(board, current_player)
        if moves:
            move = random.choice(moves)
            board = apply_move(board, current_player, move)
        current_player = -current_player
    return winner(board)


def get_move(board, color):
    root = MCTSNode(board, color)
    start_time = time.perf_counter()

    while time.perf_counter() - start_time < TIME_LIMIT:
        node = root

        # 1. Selección
        while node.is_fully_expanded() and node.children:
            node = node.best_child()

        # 2. Expansión
        if not game_over(node.board) and node.untried_moves:
            node = node.expand()

        # 3. Simulación
        result = simulate_random_game(node.board, node.player)

        # 4. Retropropagación
        node.backpropagate(result)

    # Elegimos la jugada más visitada
    if root.children:
        return max(root.children, key=lambda c: c.visits).move
    else:
        return None
