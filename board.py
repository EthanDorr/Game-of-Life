from typing import Tuple

import numpy as np
import pygame

import config as cg

class Board():
    def __init__(self, screen_dimensions) -> None:
        tile_dimensions, border_dimensions = self._calculate_tile_and_border_dimensions(screen_dimensions)
        self.board_width, self.board_height = tile_dimensions
        self.border_width, self.border_height = border_dimensions
        self.board = np.zeros((self.board_height, self.board_width), dtype=int)
        self.tile_colors = (cg.DEAD_TILE_COLOR, cg.LIVING_TILE_COLOR, cg.DYING_TILE_COLOR, cg.LIVE_TILE_COLOR)
    
    def evolve(self) -> None:
        num_living_neighbors = self._get_num_living_neighboring_cells()

        self.board[num_living_neighbors == 3] |= 0b01
        self.board[num_living_neighbors != 3] &= ~0b01
        self.board[num_living_neighbors == 4] |= (self.board[num_living_neighbors == 4] >> 1) & 0b01
        
    def tick(self) -> None:
        self.board &= ~0b10
        self.board |= (self.board & 0b01) << 1

    def draw(self, surface: pygame.surface.Surface) -> None:
        for row in range(self.board_height):
            for col in range(self.board_width):
                surface.fill(self.tile_colors[self.board[row, col]], self.get_rect(row, col))

    def clear(self) -> None:
        self.board = np.zeros((self.board_height, self.board_width), dtype=int)

    def terminate(self, row: int, col: int) -> None:
        self.board[row, col] &= ~0b11
    
    def resurrect(self, row: int, col: int) -> None:
        self.board[row, col] |= 0b11

    def get_rect(self, row: int, col: int) -> pygame.Rect:
        return pygame.Rect(
            col*(cg.TILE_SIZE.width + cg.GRID_LINE_THICKNESS) + cg.GRID_LINE_THICKNESS + self.border_width // 2,
            row*(cg.TILE_SIZE.height + cg.GRID_LINE_THICKNESS) + cg.GRID_LINE_THICKNESS + self.border_height // 2,
            *cg.TILE_SIZE)

    def adjust_board_with_screen(self, screen_dimensions: Tuple[int, int]) -> None:
        old_board_width, old_board_height = self.board_width, self.board_height
        tile_dimensions, border_dimensions = self._calculate_tile_and_border_dimensions(screen_dimensions)
        self.board_width, self.board_height = tile_dimensions
        self.border_width, self.border_height = border_dimensions
        self.board = np.asarray([[self.board[row, col] if row < old_board_height and col < old_board_width else 0 for col in range(self.board_width)] for row in range(self.board_height)], dtype=int)

    def _get_num_living_neighboring_cells(self) -> np.ndarray:
        a = (np.pad(self.board, pad_width=1, mode='wrap') > 1).astype(int)
        return a[:-2,:-2] + a[:-2,1:-1] + a[:-2,2:] + a[1:-1,:-2] + a[1:-1,1:-1] + a[1:-1,2:] + a[2:,:-2] + a[2:,1:-1] + a[2:,2:]

    def _calculate_tile_and_border_dimensions(self, screen_dimensions: Tuple[int, int]) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        screen_width, screen_height = screen_dimensions
        w_n, w_e = divmod(screen_width - cg.GRID_LINE_THICKNESS, cg.TILE_SIZE.width + cg.GRID_LINE_THICKNESS)
        h_n, h_e = divmod(screen_height - cg.GRID_LINE_THICKNESS, cg.TILE_SIZE.height + cg.GRID_LINE_THICKNESS)
        return ((w_n, h_n), (w_e, h_e))