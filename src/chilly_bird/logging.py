"""Contains logging-specific utilities."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import loguru


def configure_logger(
    logger_: loguru.Logger,
    level: str = "DEBUG",
    logs_path: str = "./logs/",
    *,
    print_stdout: bool = False,
    tracing: bool = False,
) -> None:
    """Configure `loguru`'s logger with specific level and logs path.

    Args:
    ----
        logger_: `loguru`'s logger instance
        level: specifies debugging level
        logs_path: path to store logs
        print_stdout: whether to print DEBUG level logs to stdout
        tracing: whether to save tracing logs to file

    """
    path = Path(logs_path).resolve()
    path.mkdir(parents=True, exist_ok=True)
    logger_.add(path / "game.log", level=level)

    try:  # trying to remove the default handler
        logger_.remove(0)
    except ValueError:
        pass
    else:
        if tracing:  # whether to enable tracing logs
            tracing_path = path / "runtime_{time}.log"
            logger_.add(tracing_path, level="TRACE", retention=5)

        if print_stdout:
            logger_.add(sys.stderr, level="DEBUG")
