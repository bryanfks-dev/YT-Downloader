import argparse
from src import api
import lib


def registerArgs() -> tuple[argparse.Namespace, list[str]]:
    """
    Function to register the arguments

    :return: None
    """

    parser = argparse.ArgumentParser()

    # Register video and audio arguments
    parser.add_argument(
        "--video",
        "-v",
        dest="youtube_url",
        nargs="+",
        help="Download youtube video as video format",
        default="d",
        type=str,
    )

    parser.add_argument(
        "--audio",
        "-a",
        dest="youtube_url",
        nargs="+",
        help="Download youtube video as audio format",
        type=str,
    )

    return parser.parse_known_args()


def handleArgs(args: argparse.Namespace, unknown: list[str]) -> None:
    """
    Function to handle the arguments

    :param args: The arguments
    :param unknown: The unknown arguments
    :return: None
    """

    if len(unknown) > 0:
        for URL in unknown:
            # Check if the URL is a playlist
            if "/playlist?list=" in URL:
                api.downloadPlaylist(lib.MediaType.VIDEO, URL)

                continue

            api.downloadVideo(URL)

    try:
        if args.video:
            for URL in args.video:
                # Check if the URL is a playlist
                if "/playlist?list=" in URL:
                    api.downloadPlaylist(lib.MediaType.VIDEO, URL)

                    continue

                api.downloadVideo(URL)

        if args.audio:
            for URL in args.audio:
                # Check if the URL is a playlist
                if "/playlist?list=" in URL:
                    api.downloadPlaylist(lib.MediaType.AUDIO, URL)

                    continue

                api.downloadAudio(URL)
    except:
        pass


def run() -> None:
    """
    Function to run the CLA

    :return: None
    """

    args, unknown = registerArgs()

    handleArgs(args, unknown)
