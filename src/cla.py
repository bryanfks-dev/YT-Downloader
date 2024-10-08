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
        dest="youtube_video_url",
        nargs="+",
        help="Download youtube video as video format",
        type=str,
    )

    parser.add_argument(
        "--audio",
        "-a",
        dest="youtube_audio_url",
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

    # Check if there are unknown arguments
    if len(unknown) > 0:
        # If there are unknown arguments, download as video
        # as default argument flag
        for URL in unknown:
            # Check if the URL is a playlist
            if "/playlist?list=" in URL:
                api.downloadPlaylist(lib.MediaType.VIDEO, URL)

                continue

            api.downloadVideo(URL)

    try:
        # Check if the video URL is provided
        if args.youtube_video_url:
            for URL in args.youtube_video_url:
                # Check if the URL is a playlist
                if "/playlist?list=" in URL:
                    api.downloadPlaylist(lib.MediaType.VIDEO, URL)

                    continue

                api.downloadVideo(URL)

        # Check if the audio URL is provided
        if args.youtube_audio_url:
            for URL in args.youtube_audio_url:
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
