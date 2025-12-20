"""Simple scene that shows movement and input handling."""

from __future__ import annotations

from dataclasses import dataclass

import pygame

from experiments.common import Scene


@dataclass(slots=True)
class Player:
    position: pygame.Vector2
    velocity: pygame.Vector2
    size: int = 32
    color: tuple[int, int, int] = (180, 220, 255)

    def rect(self) -> pygame.Rect:
        return pygame.Rect(int(self.position.x), int(self.position.y), self.size, self.size)


class SandboxScene(Scene):
    """A lightweight scene demonstrating the common helpers."""

    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.player = Player(position=pygame.Vector2(50, 50), velocity=pygame.Vector2(140, 110))
        self.font = pygame.font.SysFont("arial", 16)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.event.post(pygame.event.Event(pygame.QUIT))

    def update(self, dt: float) -> None:
        next_pos = self.player.position + self.player.velocity * dt
        width, height = self.screen.get_size()

        if next_pos.x < 0 or next_pos.x + self.player.size > width:
            self.player.velocity.x *= -1
        if next_pos.y < 0 or next_pos.y + self.player.size > height:
            self.player.velocity.y *= -1

        self.player.position += self.player.velocity * dt

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, self.player.color, self.player.rect())
        fps_text = self.font.render("Press ESC to quit", True, (200, 200, 200))
        surface.blit(fps_text, (10, 10))
