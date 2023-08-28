"""Boilerplate to handle local configuration."""

import os
import pathlib
import platform
import typing as t

CONFIGS_PATHS = {
    'Linux': pathlib.Path('~', '.config'),
    'Darwin': pathlib.Path('~', 'Library', 'Preferences'),
    'Windows': pathlib.Path('%LOCALAPPDATA%')}

CONFIGS_PATH = CONFIGS_PATHS[platform.system()]

PathOrStr = t.TypeVar('PathOrStr', pathlib.Path, str)


def normalize_path(path: PathOrStr) -> PathOrStr:
    """Normalize path variable by expanding user symbol and environment variables."""
    if isinstance(path, str):
        return os.path.expanduser(os.path.expandvars(path))
    assert isinstance(path, pathlib.Path), type(path)
    _ = normalize_path(str(path))
    return pathlib.Path(_)


def initialize_config_directory(app_name: str) -> None:
    """Create a configuration directory for an application."""
    config_path = normalize_path(CONFIGS_PATH.joinpath(app_name))
    if not config_path.is_dir():
        config_path.mkdir(parents=True)
