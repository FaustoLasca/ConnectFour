from Game.gamestate import GameState
import math

def evaluate_line(indices, board):
        p0_count = p1_count = 0
        for x, y in indices:
            if board[0, x, y] == 1:
                p0_count += 1
            elif board[1, x, y] == 1:
                p1_count += 1
        # Only if the line is open for one side (no adversary present)
        if p0_count > 0 and p1_count == 0:
            return p0_count
        elif p1_count > 0 and p0_count == 0:
            return -p1_count
        return 0

def open_lines_evaluation(game_state: GameState) -> int:
    if game_state.is_game_over():
        if game_state.get_winner() == 0:
            return 1000 - game_state.get_move_count()
        elif game_state.get_winner() == 1:
            return -1000 + game_state.get_move_count()
        else:
            return 0

    board = game_state.get_board()
    total_score = 0

    # Columns
    for col in range(7):
        for row_start in range(6-3):
            line = [(col, row_start+i) for i in range(4)]
            total_score += evaluate_line(line, board)

    # Rows
    for row in range(6):
        for col_start in range(7-3):
            line = [(col_start+i, row) for i in range(4)]
            total_score += evaluate_line(line, board)

    # Positive-slope diagonals (bottom-left to top-right)
    for col_start in range(7-3):
        for row_start in range(6-3):
            line = [(col_start+i, row_start+i) for i in range(4)]
            total_score += evaluate_line(line, board)

    # Negative-slope diagonals (top-left to bottom-right)
    for col_start in range(7-3):
        for row_start in range(3,6):
            line = [(col_start+i, row_start-i) for i in range(4)]
            total_score += evaluate_line(line, board)

    return total_score