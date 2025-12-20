"""Playable Space Invaders inspired scene."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
import random

import pygame

from experiments.common import Scene


class BonusType(Enum):
    RAPID_FIRE = auto()
    SPREAD = auto()


@dataclass(slots=True)
class ActiveBonus:
    bonus_type: BonusType
    remaining_time: float


@dataclass(slots=True)
class Player:
    position: pygame.Vector2
    width: int = 48
    height: int = 26
    speed: float = 320
    base_cooldown: float = 0.45
    color: tuple[int, int, int] = (200, 240, 255)

    def rect(self) -> pygame.Rect:
        return pygame.Rect(int(self.position.x), int(self.position.y), self.width, self.height)


@dataclass(slots=True)
class Projectile:
    position: pygame.Vector2
    velocity: pygame.Vector2
    width: int = 6
    height: int = 16
    color: tuple[int, int, int] = (120, 200, 255)

    def rect(self) -> pygame.Rect:
        return pygame.Rect(int(self.position.x), int(self.position.y), self.width, self.height)


@dataclass(slots=True)
class Alien:
    position: pygame.Vector2
    size: int = 32
    color: tuple[int, int, int] = (140, 220, 120)

    def rect(self) -> pygame.Rect:
        return pygame.Rect(int(self.position.x), int(self.position.y), self.size, self.size)


@dataclass(slots=True)
class Bonus:
    bonus_type: BonusType
    position: pygame.Vector2
    fall_speed: float = 120
    radius: int = 10
    color: tuple[int, int, int] = (250, 200, 120)

    def rect(self) -> pygame.Rect:
        return pygame.Rect(
            int(self.position.x - self.radius), int(self.position.y - self.radius), self.radius * 2, self.radius * 2
        )


class SpaceInvadersScene(Scene):
    """A lightweight 2D shooter that mirrors classic Space Invaders."""

    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        width, height = self.screen.get_size()
        self.player = Player(position=pygame.Vector2(width / 2 - 24, height - 70))
        self.projectiles: list[Projectile] = []
        self.aliens: list[Alien] = []
        self.bonuses: list[Bonus] = []
        self.active_bonuses: list[ActiveBonus] = []
        self.fire_timer = 0.0
        self.is_firing = False
        self.score = 0
        self.level = 1
        self.alien_direction = 1
        self.alien_speed = 55.0
        self.drop_distance = 26
        self.projectile_speed = 460
        self.font = pygame.font.SysFont("arial", 18)
        self.title_font = pygame.font.SysFont("arial", 24)
        self._spawn_wave()

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
            if event.key == pygame.K_SPACE:
                self.is_firing = True
        if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
            self.is_firing = False

    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()
        move_direction = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            move_direction -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            move_direction += 1

        self.player.position.x += move_direction * self.player.speed * dt
        screen_width, screen_height = self.screen.get_size()
        self.player.position.x = max(16, min(self.player.position.x, screen_width - self.player.width - 16))

        self.fire_timer += dt
        wants_fire = self.is_firing or keys[pygame.K_SPACE]
        if wants_fire and self.fire_timer >= self._current_cooldown():
            self._fire_projectile()

        self._update_projectiles(dt)
        self._update_aliens(dt, screen_width)
        self._update_collisions()
        self._update_bonuses(dt, screen_height)
        self._update_bonus_timers(dt)

        if not self.aliens:
            self.level += 1
            self.alien_speed *= 1.12
            self._spawn_wave()

    def draw(self, surface: pygame.Surface) -> None:
        for projectile in self.projectiles:
            pygame.draw.rect(surface, projectile.color, projectile.rect())

        for alien in self.aliens:
            pygame.draw.rect(surface, alien.color, alien.rect())

        for bonus in self.bonuses:
            pygame.draw.circle(surface, bonus.color, (int(bonus.position.x), int(bonus.position.y)), bonus.radius)

        pygame.draw.rect(surface, self.player.color, self.player.rect())

        hud_lines = [
            f"Score: {self.score}",
            f"Wave: {self.level}",
            f"Bonuses: {self._bonus_status_text()}",
            "Left/Right or A/D to move",
            "Space to shoot",
            "ESC to quit",
        ]

        for idx, line in enumerate(hud_lines):
            text_surface = self.font.render(line, True, (210, 210, 220))
            surface.blit(text_surface, (14, 12 + idx * 20))

        title = self.title_font.render("Space Invaders", True, (255, 255, 255))
        surface.blit(title, (14, 12 + len(hud_lines) * 20))

    def _current_cooldown(self) -> float:
        if self._has_bonus(BonusType.RAPID_FIRE):
            return max(0.15, self.player.base_cooldown * 0.4)
        return self.player.base_cooldown

    def _fire_projectile(self) -> None:
        self.fire_timer = 0.0
        shot_origin = pygame.Vector2(self.player.position.x + self.player.width / 2, self.player.position.y)
        velocities = [pygame.Vector2(0, -self.projectile_speed)]

        if self._has_bonus(BonusType.SPREAD):
            velocities.extend(
                [
                    pygame.Vector2(-160, -self.projectile_speed),
                    pygame.Vector2(160, -self.projectile_speed),
                ]
            )

        for velocity in velocities:
            projectile_pos = pygame.Vector2(shot_origin.x - 3, shot_origin.y - 10)
            self.projectiles.append(Projectile(position=projectile_pos, velocity=velocity))

    def _update_projectiles(self, dt: float) -> None:
        screen_height = self.screen.get_height()
        remaining: list[Projectile] = []
        for projectile in self.projectiles:
            projectile.position += projectile.velocity * dt
            if projectile.position.y + projectile.height > 0:
                remaining.append(projectile)
        self.projectiles = remaining

    def _update_aliens(self, dt: float, screen_width: int) -> None:
        if not self.aliens:
            return

        dx = self.alien_speed * dt * self.alien_direction
        for alien in self.aliens:
            alien.position.x += dx

        min_x = min(alien.position.x for alien in self.aliens)
        max_x = max(alien.position.x + alien.size for alien in self.aliens)
        if min_x < 12 or max_x > screen_width - 12:
            self.alien_direction *= -1
            for alien in self.aliens:
                alien.position.y += self.drop_distance

    def _update_collisions(self) -> None:
        remaining_projectiles: list[Projectile] = []
        for projectile in self.projectiles:
            hit_alien = next((alien for alien in self.aliens if projectile.rect().colliderect(alien.rect())), None)
            if hit_alien:
                self.score += 10
                self._maybe_drop_bonus(hit_alien)
                self.aliens.remove(hit_alien)
            else:
                remaining_projectiles.append(projectile)
        self.projectiles = remaining_projectiles

    def _update_bonuses(self, dt: float, screen_height: int) -> None:
        remaining: list[Bonus] = []
        player_rect = self.player.rect()
        for bonus in self.bonuses:
            bonus.position.y += bonus.fall_speed * dt
            if bonus.position.y - bonus.radius > screen_height:
                continue
            if bonus.rect().colliderect(player_rect):
                self._apply_bonus(bonus.bonus_type)
                continue
            remaining.append(bonus)
        self.bonuses = remaining

    def _update_bonus_timers(self, dt: float) -> None:
        still_active: list[ActiveBonus] = []
        for active in self.active_bonuses:
            active.remaining_time -= dt
            if active.remaining_time > 0:
                still_active.append(active)
        self.active_bonuses = still_active

    def _apply_bonus(self, bonus_type: BonusType) -> None:
        duration = 6.0 if bonus_type == BonusType.RAPID_FIRE else 7.5
        for active in self.active_bonuses:
            if active.bonus_type == bonus_type:
                active.remaining_time = duration
                break
        else:
            self.active_bonuses.append(ActiveBonus(bonus_type=bonus_type, remaining_time=duration))

    def _has_bonus(self, bonus_type: BonusType) -> bool:
        return any(active.bonus_type == bonus_type for active in self.active_bonuses)

    def _bonus_status_text(self) -> str:
        if not self.active_bonuses:
            return "None"
        return ", ".join(f"{active.bonus_type.name.title()} ({active.remaining_time:0.1f}s)" for active in self.active_bonuses)

    def _maybe_drop_bonus(self, alien: Alien) -> None:
        if random.random() < 0.22:
            bonus_type = random.choice(list(BonusType))
            start = pygame.Vector2(alien.position.x + alien.size / 2, alien.position.y + alien.size)
            self.bonuses.append(Bonus(bonus_type=bonus_type, position=start))

    def _spawn_wave(self) -> None:
        width, _ = self.screen.get_size()
        cols = 9
        rows = 4 + (self.level // 2)
        horizontal_spacing = 12
        vertical_spacing = 12
        alien_size = 32
        total_width = cols * alien_size + (cols - 1) * horizontal_spacing
        start_x = (width - total_width) / 2
        start_y = 70

        self.aliens = []
        for row in range(rows):
            for col in range(cols):
                pos_x = start_x + col * (alien_size + horizontal_spacing)
                pos_y = start_y + row * (alien_size + vertical_spacing)
                self.aliens.append(Alien(position=pygame.Vector2(pos_x, pos_y), size=alien_size))

        self.alien_direction = 1
        self.fire_timer = 0.0
        self.is_firing = False
