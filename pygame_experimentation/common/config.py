"""Configuration dataclasses for pygame experiments."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class WindowSettings:
    """Basic window settings used when creating a pygame display surface."""

    width: int = 800
    height: int = 600
    title: str = "Pygame Experiment"
    background_color: tuple[int, int, int] = (30, 30, 30)


@dataclass(slots=True)
class TimingSettings:
    """Frame timing settings for the main loop."""

    fps: int = 60
