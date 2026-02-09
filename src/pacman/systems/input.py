from __future__ import annotations
from dataclasses import dataclass
from typing import Tuple

@dataclass
class InputSample:
    move_dx: int = 0
    move_dy: int = 0
    pause_toggle: bool = False
    restart: bool = False
    quit_requested: bool = False
    skin_toggle: bool = False


class InputHandler:
    def __init__(self) -> None:
        self._available = False
        self._pygame = None
        try:
            import pygame  # type: ignore

            self._pygame = pygame
            self._available = True
        except Exception:
            self._available = False

    @property
    def available(self) -> bool:
        return self._available

    def init_window(self, width: int = 320, height: int = 320):
        if not self._available:
            return None
        pygame = self._pygame
        pygame.init()
        pygame.display.set_caption("Pacman Demo")
        screen = pygame.display.set_mode((width, height))
        return screen

    def poll(self) -> InputSample:
        sample = InputSample()
        if not self._available:
            return sample
        pygame = self._pygame
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sample.quit_requested = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sample.quit_requested = True
                elif event.key == pygame.K_p:
                    sample.pause_toggle = True
                elif event.key == pygame.K_r:
                    sample.restart = True
                elif event.key == pygame.K_s:
                    sample.skin_toggle = True
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[self._pygame.K_LEFT]:
            dx = -1
        elif keys[self._pygame.K_RIGHT]:
            dx = 1
        elif keys[self._pygame.K_UP]:
            dy = -1
        elif keys[self._pygame.K_DOWN]:
            dy = 1
        sample.move_dx, sample.move_dy = dx, dy
        return sample

    def shutdown(self) -> None:
        if not self._available:
            return
        self._pygame.quit()
