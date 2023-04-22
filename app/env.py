import logging
from pathlib import Path
from typing import Any, Dict

import yaml


def read_config(path: Path) -> Dict[str, Any]:
    try:
        with path.open(encoding="utf8") as config_file:
            config: Dict[str, Any] = yaml.safe_load(config_file)
    except FileNotFoundError:
        logging.warn("Could not import config. This is expected behavior during testing phase.")
        config = {}
    return config


PROJECT_PATH: Path = Path(__file__).parent.parent
config: Dict[str, Any] = read_config(PROJECT_PATH / "config.yaml")
