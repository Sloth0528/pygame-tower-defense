"""Find bundled resources relative to this project, independent of the cwd."""
from pathlib import Path

import pygame

PROJECT_DIR = Path(__file__).resolve().parent


def resource_path(relative_path):
    """Return the full path to a resource shipped with the game."""
    return str(PROJECT_DIR / relative_path)


def load_asset_image(relative_path):
    """Load an image and explain which file is missing if assets are incomplete."""
    path = resource_path(relative_path)
    if not Path(path).is_file():
        raise FileNotFoundError(
            f"Missing game image: {path}\n"
            "Download and extract the complete project, including asset folders."
        )
    return pygame.image.load(path)
