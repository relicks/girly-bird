from __future__ import annotations

import sys
from pathlib import Path

import loguru


def configure_logger(
    logger_: loguru.Logger,
    logger_level: str = "TRACE",
    log_file_path: str = "./logs/",
    print_stdout: bool = False,
) -> None:
    path = Path(log_file_path).resolve() / "runtime_{time}.log"
    path.parent.mkdir(parents=True, exist_ok=True)

    logger_.remove(0)
    logger_.add(path, level=logger_level, retention=5)

    if print_stdout:
        logger_.add(sys.stderr, level="INFO")
