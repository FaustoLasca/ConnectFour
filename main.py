import threading
from queue import Queue
import multiprocessing as mp
from typing import List
from GUI.gui import GUI
from Controller.controller import Controller
from Game.gamestate import GameState


def start_controller(update_ui_queue: Queue, ui_move_request_queue: Queue, ui_move_response_queue: Queue):
    controller = Controller(update_ui_queue, ui_move_request_queue, ui_move_response_queue)
    controller.run()


if __name__ == "__main__":
    mp.set_start_method("spawn")

    update_ui_queue = Queue[(int, GameState)]()
    ui_move_request_queue = Queue[List[int]]()
    ui_move_response_queue = Queue[int]()

    controller_thread = threading.Thread(
        target=start_controller,
        args=(update_ui_queue,ui_move_request_queue, ui_move_response_queue,)
        )
    controller_thread.start()

    ui = GUI(update_ui_queue, ui_move_request_queue, ui_move_response_queue)
    ui.run()

    