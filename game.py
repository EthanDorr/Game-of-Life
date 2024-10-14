import pygame

import board, fps
import config as cg

class ConwayGame:
    def __init__(self, paused: bool = False) -> None:
        pygame.init()
        pygame.display.set_caption(cg.TITLE)

        self.canvas = pygame.display.set_mode(cg.SCREEN_RESOLUTION, pygame.FULLSCREEN if cg.FULLSCREEN else pygame.RESIZABLE)
        self.board = board.Board(cg.SCREEN_RESOLUTION)
        self.fps_counter = fps.FPSCounter()
        self.paused = paused
        self.running = True
        
        # Draw initial background/grid
        self.canvas.fill(cg.BACKGROUND_COLOR)
        self.draw_grid()

    def run(self) -> None:
        while self.running:
            self.update()
            self.draw()
            self.fps_counter.tick(cg.FPS)
        pygame.quit()

    def update(self) -> None:
        # Handle events
        events = pygame.event.get()
        for event in events:
            # Check if the player quit the game
            if event.type == pygame.QUIT:
                return self.shutdown()
            # Check to see if the player resized the video
            if event.type == pygame.VIDEORESIZE:
                self.canvas = pygame.display.set_mode(event.size, pygame.FULLSCREEN if cg.FULLSCREEN else pygame.RESIZABLE)
                self.board.adjust_board_with_screen(self.canvas.get_size())
                self.canvas.fill(cg.BACKGROUND_COLOR)
                self.draw_grid()
            # Check if the player paused the game
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return self.shutdown()
                if event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                if event.key == pygame.K_r:
                    self.clear_board()
                    self.paused = True

            # Check if the player has their mouse on a tile in any frame
            mouse_pos = pygame.mouse.get_pos()
            row, col = self.convert_mouse_pos_to_coords(*mouse_pos)
            if row is None or col is None:
                continue
            # Check for initial click
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if LMB clicked
                if event.button == 1 and not pygame.mouse.get_pressed()[2]:
                    self.board.resurrect(row, col)
                # Check if RMB clicked
                elif event.button == 3 and not pygame.mouse.get_pressed()[0]:
                    self.board.terminate(row, col)
            # Check for a held mouse click
            elif any(pygame.mouse.get_pressed()):
                # Check if LMB held
                if pygame.mouse.get_pressed()[0] and not pygame.mouse.get_pressed()[2]:
                    self.board.resurrect(row, col)
                # Check if RMB held
                elif pygame.mouse.get_pressed()[2] and not pygame.mouse.get_pressed()[0]:
                    self.board.terminate(row, col)

        # Handle logic
        if not self.paused:
            self.board.tick()
        self.board.evolve()

        # FPS counter
        if cg.FPS_COUNTER_ENABLED:
            self.fps_counter.update()

    def draw(self) -> None:
        # Render board
        self.board.draw(self.canvas)

        # FPS counter
        if cg.FPS_COUNTER_ENABLED:
            self.fps_counter.draw(self.canvas)

        # Display screen
        pygame.display.flip()

    def shutdown(self) -> None:
        self.running = False

    def clear_board(self) -> None:
        self.board.clear()

    def draw_grid(self) -> None:
        if cg.GRID_LINE_THICKNESS <= 0: return

        # Horizontal
        for h in range(self.board.border_height // 2, self.canvas.get_height() - self.board.border_height // 2, cg.TILE_SIZE.height + cg.GRID_LINE_THICKNESS):
            pygame.draw.line(self.canvas, cg.GRID_LINE_COLOR, (self.board.border_width // 2, h), (self.canvas.get_width() - (self.board.border_width + 1) // 2 - 1, h), width=cg.GRID_LINE_THICKNESS)
        # Vertical
        for w in range(self.board.border_width // 2, self.canvas.get_width() - self.board.border_width // 2, cg.TILE_SIZE.width + cg.GRID_LINE_THICKNESS):
            pygame.draw.line(self.canvas, cg.GRID_LINE_COLOR, (w, self.board.border_height // 2), (w, self.canvas.get_height() - (self.board.border_height + 1) // 2 - 1), width=cg.GRID_LINE_THICKNESS)

    def convert_mouse_pos_to_coords(self, x: int, y: int) -> tuple[int | None, int | None]:
        row = (y - cg.GRID_LINE_THICKNESS - self.board.border_height // 2 + 1) // (cg.TILE_SIZE.height + cg.GRID_LINE_THICKNESS)
        col = (x - cg.GRID_LINE_THICKNESS - self.board.border_width // 2 + 1) // (cg.TILE_SIZE.width + cg.GRID_LINE_THICKNESS)
        return (row if 0 <= row < self.board.board_height else None, col if 0 <= col < self.board.board_width else None)
