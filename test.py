from Game.evaluation import open_lines_evaluation
from Game.gamestate import GameState
from Search.alphabeta import AlphaBetaSearcher
import time

game_state = GameState()

searcher = AlphaBetaSearcher(open_lines_evaluation, game_state.copy())
time_start = time.time()
print("Alpha-beta result: ", searcher.alpha_beta(5))
time_end = time.time()
print(searcher.pv_table[0])

print("Time: ", time_end - time_start)
print("Evaluations: ", searcher.count_evaluations)
print("Pruned: ", searcher.count_pruned_nodes)

print("--------------------------------")

searcher = AlphaBetaSearcher(open_lines_evaluation, game_state.copy())
time_start = time.time()
print("Iterative deepening result: ", searcher.iterative_deepening(5))
time_end = time.time()
print(searcher.pv_table[0])

print("Time: ", time_end - time_start)
print("Evaluations: ", searcher.count_evaluations)
print("Pruned: ", searcher.count_pruned_nodes)