"""Asset loading helpers with simple caching."""

from __future__ import annotations

from pathlib import Path
from typing import Dict

import pygame


class AssetLoader:
    """Load and cache image and font assets relative to a root directory."""

    def __init__(self, asset_root: Path | str) -> None:
        self.asset_root = Path(asset_root)
        self._image_cache: Dict[Path, pygame.Surface] = {}
        self._font_cache: Dict[tuple[Path, int], pygame.font.Font] = {}

    def resolve(self, relative_path: str | Path) -> Path:
        """Resolve a relative path inside the asset root."""

        return (self.asset_root / relative_path).resolve()

    def image(self, relative_path: str | Path) -> pygame.Surface:
        """Load an image, caching it after the first request."""

        absolute_path = self.resolve(relative_path)
        if absolute_path not in self._image_cache:
            self._image_cache[absolute_path] = pygame.image.load(absolute_path.as_posix()).convert_alpha()
        return self._image_cache[absolute_path]

    def font(self, relative_path: str | Path, size: int) -> pygame.font.Font:
        """Load a TTF font file with the given size, caching the result."""

        absolute_path = self.resolve(relative_path)
        cache_key = (absolute_path, size)
        if cache_key not in self._font_cache:
            self._font_cache[cache_key] = pygame.font.Font(absolute_path.as_posix(), size)
        return self._font_cache[cache_key]
