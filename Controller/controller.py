from Game.gamestate import GameState
from Controller.player import Player
from typing import List
from queue import Queue


class Controller:
    def __init__(self, update_ui_queue: Queue, players: List[Player]):
        self.state = GameState()
        self.update_ui_queue = update_ui_queue
        self.players = players

    def run(self):
        for player in self.players:
            player.update_state(None, self.state.copy())

        while not self.state.is_game_over():
            
            valid_moves = self.state.generate_valid_moves()
            if not valid_moves:
                break

            current_player = self.state.get_current_player()
            move = self.players[current_player].get_move(valid_moves)

            self.state.move(move)
            for player in self.players:
                player.update_state(move, self.state.copy())
            
            self.update_ui_queue.put((move, self.state.copy()))
        
        print("Game over. Winner: ", self.state.get_winner())
        for player in self.players:
            player.close()
            