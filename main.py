import src
import sys


def main() -> None:
    """
    Main driver to download the file

    :return: None
    """

    args: list[str] = sys.argv[1:]

    # Check if there are no arguments
    if len(args) == 0:
        src.cli.run()

        return

    src.cla.run()


if __name__ == "__main__":
    main()
