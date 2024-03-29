"""Start the game from here."""

import sys
from os import chdir
from pathlib import Path

from chilly_bird import GameFactory


def main() -> None:
    """Game entrypoint, supports PyInstaller and normal Python process."""
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        print("running in a PyInstaller bundle", file=sys.stderr)
        chdir(Path(__file__).parent.resolve())
    else:
        print("running in a normal Python process", file=sys.stderr)

    with GameFactory() as game:
        game.run()


if __name__ == "__main__":
    main()
