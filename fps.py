import pygame

import config as cg

class FPSCounter:
    def __init__(self):
        self.font = pygame.font.SysFont(cg.FPS_COUNTER_FONT, cg.FPS_COUNTER_SIZE)
        self.text = None

    def update(self, clock: pygame.time.Clock) -> None:
        fps = f'{int(clock.get_fps())} FPS'
        self.text = self.font.render(fps, False, cg.FPS_COUNTER_COLOR)

    def draw(self, surface: pygame.surface.Surface) -> None:
        surface.fill(cg.BACKGROUND_COLOR, self.text.get_rect(topleft=cg.FPS_COUNTER_POSITION))
        surface.blit(self.text, self.text.get_rect(topleft=cg.FPS_COUNTER_POSITION))