from chilly_bird import GameFactory


def main():
    with GameFactory() as game:
        game.run()


if __name__ == "__main__":
    main()
