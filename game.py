from loguru import logger

from chilly_bird.configs import load_config
from chilly_bird.logging import configure_logger
from chilly_bird.objects import Game


def main():
    configure_logger(logger, level="DEBUG", print_stdout=True)
    cfg = load_config()

    logger.info("Initializing Game")
    game = Game(cfg.window.screen_width, cfg.window.screen_height)
    game.run()


if __name__ == "__main__":
    main()
