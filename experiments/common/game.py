"""Shared pygame game loop helpers."""

from __future__ import annotations

from typing import Callable

import pygame

from .config import TimingSettings, WindowSettings
from .scenes import Scene, SceneManager


def run_game(
    scene_factory: Callable[[pygame.Surface], Scene],
    window_settings: WindowSettings | None = None,
    timing_settings: TimingSettings | None = None,
) -> None:
    """Run a pygame main loop using a provided scene factory.

    The factory receives the primary display surface so scenes can perform any
    setup that depends on the surface configuration.
    """

    window = window_settings or WindowSettings()
    timing = timing_settings or TimingSettings()

    pygame.init()
    screen = pygame.display.set_mode((window.width, window.height))
    pygame.display.set_caption(window.title)
    clock = pygame.time.Clock()

    manager = SceneManager(scene_factory(screen))

    is_running = True
    while is_running:
        dt = clock.tick(timing.fps) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
                break
            manager.handle_event(event)

        manager.update(dt)
        screen.fill(window.background_color)
        manager.draw(screen)
        pygame.display.flip()

    pygame.quit()
