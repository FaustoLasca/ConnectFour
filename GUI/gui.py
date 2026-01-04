import pygame
import sys
import torch
from typing import List, Tuple
from queue import Queue, Empty

from torch.compiler import F
from Game.gamestate import GameState

class GUI:
    def __init__(self, update_queue: Queue, move_request_queue: Queue, move_response_queue: Queue):
        pygame.init()
        self.screen = pygame.display.set_mode((1400, 1400))
        pygame.display.set_caption("Connect 4")
        self.clock = pygame.time.Clock()

        self.update_queue = update_queue
        self.move_request_queue = move_request_queue
        self.move_response_queue = move_response_queue

        self.board = Board()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        move = self.board.handle_click(event.pos)
                        if move is not None:
                            self.move_response_queue.put(move)
                
            try:
                move, state = self.update_queue.get_nowait()
                self.board.update_state(state)
            except Empty:
                pass

            try:
                available_moves = self.move_request_queue.get_nowait()
                self.board.update_available_moves(available_moves)
            except Empty:
                pass

            self.screen.fill((0, 0, 0))
            self.board.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()
        sys.exit()


class GUIElement:
    def draw(self, screen):
        pass


class Pawn(GUIElement):
    def __init__(self, x, y, color, size):
        self.x = x + size / 2
        self.y = y + size / 2
        self.color = color
        self.size = size

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size / 2)


class MoveButton(GUIElement):
    def __init__(self, x, y, player_colors, size, player: int = 0):
        self.x = x + size / 2
        self.y = y + size / 2
        self.size = size
        self.player = player
        self.player_colors = player_colors
        self.collision_box = pygame.Rect(x, y, size, size)

    def draw(self, screen):
        if self.collision_box.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.circle(screen, self.player_colors[self.player], (self.x, self.y), self.size/2)
    
    def update_player(self, player: int):
        self.player = player


class Board(GUIElement):
    def __init__(self, starting_board = None, x = 0, y = 0, cell_size = 200):
        self.cell_size = cell_size
        self.x = x
        self.y = y

        self.pawn_proportion = 0.8
        self.background_color = (0, 0, 0)
        self.board_color = (200 , 200, 200)
        self.player_colors = [(180, 20, 20), (100, 100, 100)]

        self.game_state = GameState()
        self.pawn_list = []
        if starting_board is not None:
            self.update_board(starting_board)

        self.move_buttons = [
            MoveButton(
                x = self.x + column * self.cell_size + self.cell_size * (1 - self.pawn_proportion) / 2,
                y = self.y + self.cell_size * (1 - self.pawn_proportion) / 2,
                player_colors = self.player_colors,
                size = self.cell_size * self.pawn_proportion,
                player = self.game_state.get_current_player(),
            )
            for column in range(7)
        ]
        self.available_moves = []

    def update_state(self, new_state: GameState):
        self.game_state = new_state
        board = self.game_state.get_board()
        self.pawn_list = []
        for player in range(2):
            for column in range(7):
                for row in range(6):
                    if board[player, column, row] == 1:
                        pawn = Pawn(
                            x = self.x + column * self.cell_size + self.cell_size * (1 - self.pawn_proportion) / 2,
                            y = self.y + (6 - row) * self.cell_size + self.cell_size * (1 - self.pawn_proportion) / 2,
                            color = self.player_colors[player],
                            size = self.cell_size * self.pawn_proportion,
                        )
                        self.pawn_list.append(pawn)

        player = self.game_state.get_current_player()
        for button in self.move_buttons:
            button.update_player(player)

    def update_available_moves(self, available_moves: List[int]):
        self.available_moves = available_moves
    
    def handle_click(self, pos: Tuple[int, int]):
        for i in self.available_moves:
            if self.move_buttons[i].collision_box.collidepoint(pos):
                self.available_moves = []
                return i
        return None

    def draw(self, screen):
        pygame.draw.rect(
            screen,
            self.background_color,
            (self.x, self.y, self.cell_size * 7, self.cell_size)
            )
        pygame.draw.rect(
            screen,
            self.board_color,
            (self.x, self.y + self.cell_size, self.cell_size * 7, self.cell_size * 6)
            )

        for column in range(7):
            for row in range(6):
                pygame.draw.circle(
                    screen,
                    self.background_color,
                    (self.x + (column + 0.5) * self.cell_size, self.y + (row + 1.5) * self.cell_size),
                    self.cell_size * self.pawn_proportion / 2
                    )

        for pawn in self.pawn_list:
            pawn.draw(screen)

        for i in self.available_moves:
            self.move_buttons[i].draw(screen)