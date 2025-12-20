"""Minimal example that exercises the shared pygame helpers."""

from __future__ import annotations

import pygame

# Allow running as a module (`python -m experiments.projects.sandbox.main`) or directly
# as a script (`python experiments/projects/sandbox/main.py`).
if __package__ in (None, ""):
    # When executed directly, ensure the repository root is on sys.path so
    # absolute imports from the experiments package succeed.
    import sys
    from pathlib import Path

    repo_root = Path(__file__).resolve().parents[2]
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))

from experiments.common import TimingSettings, WindowSettings, run_game
from experiments.projects.sandbox.scenes import SandboxScene


def launch() -> None:
    """Launch the sandbox demo."""

    window = WindowSettings(title="Sandbox Demo")
    timing = TimingSettings(fps=60)
    run_game(lambda screen: SandboxScene(screen), window_settings=window, timing_settings=timing)


if __name__ == "__main__":
    launch()
