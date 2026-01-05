from Game.gamestate import GameState
from typing import Callable

class AlphaBetaSearcher:
    def __init__(self, evaluation_function: Callable[[GameState], int], game_state: GameState):
        self.game_state = game_state
        self.max_depth = 6
        self.pv_table = [[None] * self.max_depth for _ in range(self.max_depth)]
        self.pv_length = [0] * (self.max_depth + 1)
        self.evaluate = evaluation_function

        self.following_pv = False

        self.count_evaluations = 0
        self.count_pruned_nodes = 0
    
    def iterative_deepening(self, max_depth: int) -> (int, int):
        self.reset_search()
        for depth in range(1, max_depth + 1):
            self.following_pv = True
            value = self.alpha_beta(depth)
        return self.pv_table[0][0], value
        

    # Negamax alpha-beta search with principal variation table
    def alpha_beta(self, depth_left: int, ply : int = 0, alpha = -float('inf'), beta = float('inf')) -> int:
        # If we have reached the maximum depth or the game is over, evaluate the state
        if depth_left == 0 or self.game_state.is_game_over():
            self.pv_length[ply] = 0
            self.following_pv = False
            self.count_evaluations += 1
            # The evaluation is from player 0's perspective
            # We need to negate the evaluation for player 1 (because we are using negamax)
            evaluation = self.evaluate(self.game_state)
            if self.game_state.get_current_player() == 0:
                return evaluation
            else:
                return -evaluation
 
        # Move ordering: check the principal variation first
        # Should increase the amount of pruned nodes
        moves = self.game_state.generate_valid_moves()
        if self.pv_table[0][ply] is not None and self.following_pv:
            previous_best = self.pv_table[0][ply]
            moves.remove(previous_best)
            moves.insert(0, previous_best)
        else:
            self.following_pv = False

        best_value = -float('inf')
        self.pv_length[ply] = 0

        for move in moves:
            self.game_state.move(move)
            value = -self.alpha_beta(depth_left - 1, ply + 1, -beta, -alpha)
            self.game_state.unmove(move)

            # Update the best value
            if value > best_value:
                best_value = value
                # Update the principal variation table
                # Best move followed by the child's best move
                # Update the length of the principal variation table
                self.pv_table[ply][0] = move
                if ply + 1 < self.max_depth:
                    for i in range(self.pv_length[ply + 1]):
                        self.pv_table[ply][i + 1] = self.pv_table[ply + 1][i]
                    self.pv_length[ply] = self.pv_length[ply + 1] + 1
                else:
                    self.pv_length[ply] = 1
                # Update the alpha value
                if value > alpha:
                    alpha = value
            # If the best value is greater than or equal to the beta value, we can prune the search
            # Fail-soft beta-pruning (keep the best value found)
            if best_value >= beta:
                self.count_pruned_nodes += 1
                break
        
        return best_value

    def reset_search(self):
        self.following_pv = False
        self.count_evaluations = 0
        self.count_pruned_nodes = 0
        self.pv_table = [[None] * self.max_depth for _ in range(self.max_depth)]
        self.pv_length = [0] * (self.max_depth + 1)
