import sys
from os import chdir, path

from chilly_bird import GameFactory


def main():
    """Game entrypoint, supports PyInstaller and normal Python proccess."""
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        print("running in a PyInstaller bundle", file=sys.stderr)
        chdir(path.abspath(path.dirname(__file__)))
    else:
        print("running in a normal Python process", file=sys.stderr)

    with GameFactory() as game:
        game.run()


if __name__ == "__main__":
    main()
