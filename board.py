import numpy as np
import pygame

import config as cg

class Board():
    def __init__(self, screen_dimensions: cg.Size) -> None:
        self.surface = pygame.Surface(screen_dimensions)
        (self.board_width, self.board_height), (self.border_width, self.border_height) = self._calculate_tile_and_border_dimensions(*screen_dimensions)
        self.board = np.zeros((self.board_height, self.board_width), dtype=int)
        self.board_copy = None
        self.tiles_to_draw: set[tuple[int, int]] = set(np.ndindex(self.board.shape))
        self.tile_colors = (cg.DEAD_TILE_COLOR, cg.LIVING_TILE_COLOR, cg.DYING_TILE_COLOR, cg.LIVE_TILE_COLOR)

    def evolve(self) -> None:
        self.board_copy = np.copy(self.board)

        num_living_neighbors = self._num_living_neighboring_cells()
        self.board[num_living_neighbors == 3] |= 0b01 # Live cell with two neighbors or dead cell with 3 -> Set to living
        self.board[num_living_neighbors != 3] &= ~0b01 # Assume either too few or too many neighbors
        self.board[num_living_neighbors == 4] |= (self.board[num_living_neighbors == 4] >> 1) & 0b01 # Live cell with 3 neighbors -> set to living

    def tick(self) -> None:
        self.board &= ~0b10
        self.board |= (self.board & 0b01) << 1
        
        self.tiles_to_draw.update(set(zip(*np.where(self.board != self.board_copy))))

    def draw(self, surface: pygame.surface.Surface) -> None:
        for row, col in self.tiles_to_draw:
            self.surface.fill(self.tile_colors[self.board[row, col]], pygame.Rect(*self._tile_to_pixel(row, col), *cg.TILE_SIZE))
        surface.blit(self.surface, (0,0))
        self.tiles_to_draw.clear()

    def resurrect(self, row: int, col: int) -> None:
        self.board[row, col] |= 0b11
        self.tiles_to_draw.update(set([*zip(*map(tuple, self._neighboring_cells(row, col)))]))
    
    def terminate(self, row: int, col: int) -> None:
        self.board[row, col] &= ~0b11
        self.tiles_to_draw.update(set([*zip(*map(tuple, self._neighboring_cells(row, col)))]))

    def clear(self) -> None:
        self.board = np.zeros((self.board_height, self.board_width), dtype=int)
        self.tiles_to_draw.update(np.ndindex(self.board.shape))

    # Blegh, needs work
    def adjust_board_with_screen(self, screen_dimensions: tuple[int, int]) -> None:
        old_board_width, old_board_height = self.board_width, self.board_height
        (self.board_width, self.board_height), (self.border_width, self.border_height) = self._calculate_tile_and_border_dimensions(*screen_dimensions)
        self.board = np.asarray([[self.board[row, col] if row < old_board_height and col < old_board_width else 0 for col in range(self.board_width)] for row in range(self.board_height)], dtype=int)
        self.board_copy = None
        self.tiles_to_draw = set(np.ndindex(self.board.shape))

    def _tile_to_pixel(self, row: int, col: int) -> tuple[int, int]:
        return (
            cg.GRID_LINE_THICKNESS + col * (cg.GRID_LINE_THICKNESS + cg.TILE_SIZE.width) + self.border_width // 2,
            cg.GRID_LINE_THICKNESS + row * (cg.GRID_LINE_THICKNESS + cg.TILE_SIZE.height) + self.border_height // 2
        )
    
    def _neighboring_cells(self, row, col):
        return (
            np.array([row-1, row-1, row-1, row,   row, row,   row+1, row+1, row+1]) % self.board_height,
            np.array([col-1, col,   col+1, col-1, col, col+1, col-1, col,   col+1]) % self.board_width
        )
    
    def _num_living_neighboring_cells(self) -> np.ndarray:
        a = (np.pad(self.board, pad_width=1, mode='wrap') > 1).astype(int)
        return a[:-2,:-2] + a[:-2,1:-1] + a[:-2,2:] + a[1:-1,:-2] + a[1:-1,1:-1] + a[1:-1,2:] + a[2:,:-2] + a[2:,1:-1] + a[2:,2:]
    
    def _calculate_tile_and_border_dimensions(self, screen_width: int, screen_height: int) -> tuple[tuple[int, int], tuple[int, int]]:
        w_n, w_e = divmod(screen_width - cg.GRID_LINE_THICKNESS, cg.TILE_SIZE.width + cg.GRID_LINE_THICKNESS)
        h_n, h_e = divmod(screen_height - cg.GRID_LINE_THICKNESS, cg.TILE_SIZE.height + cg.GRID_LINE_THICKNESS)
        return ((w_n, h_n), (w_e, h_e))
