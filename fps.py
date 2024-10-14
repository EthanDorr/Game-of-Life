import pygame

import config as cg

class FPSCounter:
    def __init__(self):
        self.surface = pygame.Surface(cg.FPS_COUNTER_SIZE)
        self.surface.set_colorkey(cg.BACKGROUND_COLOR)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(cg.FPS_COUNTER_FONT, cg.FPS_COUNTER_FONTSIZE)
        self.text = None

        self.rect = pygame.Rect(cg.FPS_COUNTER_POSITION, cg.FPS_COUNTER_SIZE)

    def tick(self, fps: int) -> None:
        self.clock.tick(fps)

    def update(self) -> None:
        fps = f'{int(self.clock.get_fps())} FPS'
        self.text = self.font.render(fps, False, cg.FPS_COUNTER_COLOR)

    def draw(self, surface: pygame.surface.Surface) -> None:
        self.surface.fill(cg.BACKGROUND_COLOR)
        self.surface.blit(self.text, (0, 0))
        surface.blit(self.surface, cg.FPS_COUNTER_POSITION)

        pygame.display.update(self.rect)
