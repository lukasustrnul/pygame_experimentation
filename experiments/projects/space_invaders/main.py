"""Entry point for the Space Invaders inspired experiment."""

from __future__ import annotations

if __package__ in (None, ""):
    import sys
    from pathlib import Path

    repo_root = Path(__file__).resolve().parents[2]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))

from experiments.common import TimingSettings, WindowSettings, run_game
from experiments.projects.space_invaders.scenes import SpaceInvadersScene


def launch() -> None:
    """Launch the Space Invaders demo."""

    window = WindowSettings(width=900, height=700, title="Space Invaders")
    timing = TimingSettings(fps=60)
    run_game(lambda screen: SpaceInvadersScene(screen), window_settings=window, timing_settings=timing)


if __name__ == "__main__":
    launch()
