"""
This module provides utility functions and constants for managing file paths
in a cross-platform manner, with support for XDG-compliant paths on Unix-like
systems and default paths on Windows.

Functions:
    get_xdg_path(env_var, default): Returns the XDG-compliant path for the given
    environment variable, falling back to the specified default if the variable
    is not set.

Constants:
    CONFIG_DIR: The directory for configuration files.
    DATA_DIR: The directory for application data.
    LOG_DIR: The directory for log files.
    THEMES_DIR: The directory for theme files.
    TEMP_DIR: The directory for temporary files.
    CACHE_DIR: The directory for cached files.
    CONFIG_FILE: The path to the main configuration file.
    TEMP_FILE: The path to multipurpose json file.

The module ensures that the necessary directories exist upon import.
"""

import os
import sys
from .working_dir import get_base_dir
from .platform import is_windows

base_dir = get_base_dir()

def get_xdg_path(env_var, default):
    """Returns the XDG-compliant path, falling back to default."""
    return os.getenv(env_var, os.path.expanduser(default))


if not is_windows and getattr(sys, "frozen", False):
    CONFIG_DIR = get_xdg_path("XDG_CONFIG_HOME", "~/.config") + "/webdeck"
    DATA_DIR = get_xdg_path("XDG_DATA_HOME", "~/.local/share") + "/webdeck"
    LOG_DIR = os.path.join(DATA_DIR, "logs")
    THEMES_DIR = os.path.join(CONFIG_DIR, "themes")
    TEMP_DIR = os.path.join(CONFIG_DIR, "temp")
    CACHE_DIR = get_xdg_path("XDG_CACHE_HOME", "~/.cache") + "/webdeck"
else:
    CONFIG_DIR = os.path.join(base_dir, ".config")
    DATA_DIR = os.path.join(base_dir, ".config/data")
    LOG_DIR = os.path.join(base_dir, ".logs")
    THEMES_DIR = os.path.join(CONFIG_DIR, "themes")
    TEMP_DIR = os.path.join(base_dir, "temp")
    CACHE_DIR = os.path.join(TEMP_DIR, "cache")

# Ensure directories exist
for path in [CONFIG_DIR, DATA_DIR, LOG_DIR, TEMP_DIR, CACHE_DIR]:
    os.makedirs(path, exist_ok=True)

# Specific Files
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
TEMP_FILE = os.path.join(TEMP_DIR, "temp.json")
