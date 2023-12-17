from __future__ import annotations

import sys
from pathlib import Path

import loguru


def configure_logger(
    logger_: loguru.Logger,
    level: str = "TRACE",
    logs_path: str = "./logs/",
    print_stdout: bool = False,
) -> None:
    path = Path(logs_path).resolve() / "runtime_{time}.log"
    path.parent.mkdir(parents=True, exist_ok=True)

    logger_.remove(0)
    logger_.add(path, level=level, retention=5)

    if print_stdout:
        logger_.add(sys.stderr, level="INFO")
