"""Scene abstractions shared across projects."""

from __future__ import annotations

from typing import Protocol

import pygame


class Scene(Protocol):
    """A logical screen in a pygame experiment."""

    def handle_event(self, event: pygame.event.Event) -> None:
        ...

    def update(self, dt: float) -> None:
        ...

    def draw(self, surface: pygame.Surface) -> None:
        ...


class SceneManager:
    """Manage the currently active scene and switching between them."""

    def __init__(self, initial_scene: Scene) -> None:
        self._scene = initial_scene

    @property
    def scene(self) -> Scene:
        return self._scene

    def switch(self, new_scene: Scene) -> None:
        self._scene = new_scene

    def handle_event(self, event: pygame.event.Event) -> None:
        self._scene.handle_event(event)

    def update(self, dt: float) -> None:
        self._scene.update(dt)

    def draw(self, surface: pygame.Surface) -> None:
        self._scene.draw(surface)
