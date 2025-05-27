import random

DIRECTIONS = [
    (-1, -1),  # UP-LEFT
    (-1, 0),   # UP
    (-1, 1),   # UP-RIGHT
    (0, -1),   # LEFT
    (0, 1),    # RIGHT
    (1, -1),   # DOWN-LEFT
    (1, 0),    # DOWN
    (1, 1)     # DOWN-RIGHT
]

def in_bounds(x, y):
    return 0 <= x < 8 and 0 <= y < 8

def valid_movements(board, player):
    opponent = -player
    valid_moves = []

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
                    valid_moves.append((x, y))
                    break

    return valid_moves
 
def ai_move(board, player):
    import time

    MAX_DEPTH = 4
    TIME_LIMIT = 2.8

    BOARD_SIZE = 8
    CORNERS = {(0,0), (0,7), (7,0), (7,7)}
    ADJACENTS = {(0,1),(1,0),(1,1), (0,6),(1,6),(1,7), (6,0),(6,1),(7,1), (6,6),(6,7),(7,6)}
    EDGES = (
        {(0, c) for c in range(BOARD_SIZE)} |
        {(7, c) for c in range(BOARD_SIZE)} |
        {(r, 0) for r in range(BOARD_SIZE)} |
        {(r, 7) for r in range(BOARD_SIZE)}
    ) - CORNERS

    def in_bounds(x, y):
        return 0 <= x < 8 and 0 <= y < 8

    def valid_moves(board, player):
        opponent = -player
        valid = []
        for x in range(8):
            for y in range(8):
                if board[x][y] != 0:
                    continue
                for dx, dy in [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]:
                    i, j = x + dx, y + dy
                    found_opponent = False
                    while in_bounds(i, j) and board[i][j] == opponent:
                        i += dx
                        j += dy
                        found_opponent = True
                    if found_opponent and in_bounds(i, j) and board[i][j] == player:
                        valid.append((x, y))
                        break
        return valid

    def apply_move(board, player, move):
        new_board = [row[:] for row in board]
        x, y = move
        new_board[x][y] = player
        for dx, dy in [(-1,-1), (-1,0), (-1,1), (0,-1), (0,1), (1,-1), (1,0), (1,1)]:
            i, j = x + dx, y + dy
            cells_to_flip = []
            while in_bounds(i, j) and new_board[i][j] == -player:
                cells_to_flip.append((i, j))
                i += dx
                j += dy
            if in_bounds(i, j) and new_board[i][j] == player:
                for fx, fy in cells_to_flip:
                    new_board[fx][fy] = player
        return new_board
    return best_move