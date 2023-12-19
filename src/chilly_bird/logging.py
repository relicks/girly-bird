from __future__ import annotations

import sys
from pathlib import Path

import loguru


def configure_logger(
    logger_: loguru.Logger,
    level: str = "DEBUG",
    logs_path: str = "./logs/",
    print_stdout: bool = False,
    tracing: bool = False,
) -> None:
    path = Path(logs_path).resolve()
    path.mkdir(parents=True, exist_ok=True)

    logger_.remove(0)
    logger_.add(path / "game.log", level=level)
    if tracing:
        tracing_path = path / "runtime_{time}.log"
        logger_.add(tracing_path, level="TRACE", retention=5)

    if print_stdout:
        logger_.add(sys.stderr, level="DEBUG")
