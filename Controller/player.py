from typing import List
import random
import time
from queue import Queue, Empty
import multiprocessing as mp

from Game.gamestate import GameState
from Search.alphabeta import AlphaBetaSearcher
from Game.evaluation import open_lines_evaluation


class Player:
    def update_state(self, move: int, game_state: GameState) -> int:
        pass

    def get_move(self, available_moves: List[int]) -> int:
        pass

    def close(self):
        pass


class RandomPlayer(Player):
    def get_move(self, available_moves: List[int]) -> int:
        time.sleep(1)
        return random.choice(available_moves)


class UIPlayer(Player):
    def __init__(self, move_request_queue: Queue, move_response_queue: Queue):
        self.move_request_queue = move_request_queue
        self.move_response_queue = move_response_queue

    def get_move(self, available_moves: List[int]) -> int:
        self.move_request_queue.put(available_moves)
        return self.move_response_queue.get()




def start_worker(move_request_queue: mp.Queue, move_response_queue: mp.Queue, update_queue: mp.Queue, max_depth: int):
    _, state = update_queue.get()
    while not state.is_game_over():
        try:
            available_moves = move_request_queue.get_nowait()
            searcher = AlphaBetaSearcher(open_lines_evaluation, state)
            move, value = searcher.iterative_deepening(max_depth)
            move_response_queue.put(move)
            move, state = update_queue.get()
        except Empty:
            pass

        try:
            move, state = update_queue.get_nowait()
        except Empty:
            pass

        if state is not None:
            if state.is_game_over():
                break


class SearchPlayer(Player):
    def __init__(self, max_depth: int):
        self.move_request_queue = mp.Queue()
        self.move_response_queue = mp.Queue()
        self.update_queue = mp.Queue()
        self.worker_process = mp.Process(
            target=start_worker,
            args=(self.move_request_queue, self.move_response_queue, self.update_queue, max_depth)
            )
        self.worker_process.start()
    
    def get_move(self, available_moves: List[int]) -> int:
        self.move_request_queue.put(available_moves)
        return self.move_response_queue.get()

    def update_state(self, move: int, game_state: GameState) -> int:
        self.update_queue.put((move, game_state))
    
    def close(self):
        self.worker_process.join()