import threading
from queue import Queue
import multiprocessing as mp
from typing import List
from GUI.gui import GUI
from Controller.controller import Controller
from Controller.player import Player, RandomPlayer, SearchPlayer, UIPlayer
from Game.gamestate import GameState


def start_controller(update_ui_queue: Queue, players: List[Player]):
    controller = Controller(update_ui_queue, players)
    controller.run()


if __name__ == "__main__":
    mp.set_start_method("spawn")

    update_ui_queue = Queue[(int, GameState)]()
    ui_move_request_queue = Queue[List[int]]()
    ui_move_response_queue = Queue[int]()

    players = [
        UIPlayer(ui_move_request_queue, ui_move_response_queue),
        SearchPlayer(max_depth=4),
    ]

    controller_thread = threading.Thread(
        target=start_controller,
        args=(update_ui_queue, players)
        )
    controller_thread.start()

    ui = GUI(update_ui_queue, ui_move_request_queue, ui_move_response_queue)
    ui.run()

    controller_thread.join()

    