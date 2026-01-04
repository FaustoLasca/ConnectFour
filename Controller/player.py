from Game.gamestate import GameState
from typing import List
import random
import time
from queue import Queue

class Player:
    def update_state(self, move: int, game_state: GameState) -> int:
        pass

    def get_move(self, available_moves: List[int]) -> int:
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