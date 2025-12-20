"""Minimal example that exercises the shared pygame helpers."""

from __future__ import annotations

import pygame

from pygame_experimentation.common import TimingSettings, WindowSettings, run_game
from .scenes import SandboxScene


def launch() -> None:
    """Launch the sandbox demo."""

    window = WindowSettings(title="Sandbox Demo")
    timing = TimingSettings(fps=60)
    run_game(lambda screen: SandboxScene(screen), window_settings=window, timing_settings=timing)


if __name__ == "__main__":
    launch()
