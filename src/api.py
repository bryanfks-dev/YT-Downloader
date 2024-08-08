import lib
import sys
import os
from multiprocessing import Process

# Try-catch import required external libs
try:
    from pytubefix import YouTube, Stream, Playlist
    import ffmpeg
except ImportError:
    print(
        f"{lib.colors.FAIL}[ERROR]{lib.colors.ENDC} There are missing external libs. Please install using `pip install requirements.txt`"
    )


def mergeVideoAudio(fileNameWithoutExt: str) -> None:
    """
    Function to merge the video and audio

    :param fileNameWithoutExt: The file name without the extension
    :return: None
    """

    videoPath: str = (
        f"{lib.config['OUTPUT_FILE']['VIDEO']['PATH']}{fileNameWithoutExt}.{lib.config['OUTPUT_FILE']['VIDEO']['EXTENSION']}"
    )

    audioPath: str = (
        f"{lib.config['OUTPUT_FILE']['AUDIO']['PATH']}/.temp/{fileNameWithoutExt}.{lib.config['OUTPUT_FILE']['AUDIO']['EXTENSION']}"
    )

    outputPath: str = (
        f"{lib.config['OUTPUT_FILE']['VIDEO']['PATH']}{fileNameWithoutExt}_out.{lib.config['OUTPUT_FILE']['VIDEO']['EXTENSION']}"
    )

    video = ffmpeg.input(videoPath)
    audio = ffmpeg.input(audioPath)

    ffmpeg.output(
        audio,
        video,
        outputPath,
    ).run()

    # Delete the files
    os.remove(videoPath)
    os.remove(audioPath)


def constructFileName(fileNameWithoutExt: str, type: lib.enums.MediaType) -> str:
    """
    Function to construct the file name

    :param fileNameWithoutExt: The file name without the extension
    :param type: The type of the file
    :return: The constructed file name
    """

    return f"{fileNameWithoutExt}.{lib.config['OUTPUT_FILE'][type.value.upper()]['EXTENSION']}"


def confirmRewriteFile(stream: Stream, type: lib.enums.MediaType) -> bool:
    """
    Function to confirm if the user wants to rewrite the file

    :param stream: The stream to download
    :param type: The type of the stream
    :return: True if the user wants to rewrite the file, False otherwise
    """

    fileName: str = constructFileName(
        lib.removeExtension(stream.default_filename), type
    )

    if not stream.exists_at_path(
        f"{lib.config['OUTPUT_FILE'][type.value.upper()]['PATH']}/{fileName}"
    ):
        return True

    while True:
        # Ask the user if they want to rewrite the file
        ans: str = str.upper(
            input(
                f"{lib.colors.WARNING}[WARNING]{lib.colors.ENDC} {type.value} with this title already exists in your saving directory.\nDo you want to rewrite the {type.value.lower()}? [Y/N]"
            )
        )

        # Check if the input is valid
        if ans != "Y" and ans != "N":
            print(
                f"{lib.colors.FAIL}[ERROR]{lib.colors.ENDC} Invalid input. Please enter Y or N"
            )

            continue

        return ans == "Y"


def downloadStream(
    stream: Stream, type: lib.enums.MediaType, suffixDir: str = ""
) -> None:
    """
    Function to download the stream

    :param stream: The stream to download
    :param type: The type of the stream
    :param suffixDir: The suffix directory
    :return: None
    """

    dir: str = lib.config["OUTPUT_FILE"][type.value.upper()]["PATH"]

    # Add the playlist title to the directory
    if not lib.utils.strIsEmpty(suffixDir):
        dir += f"{suffixDir}/"

    # Get the file name
    fileName: str = constructFileName(
        lib.removeExtension(stream.default_filename), type
    )

    try:
        # Download the video
        print(
            f"{lib.colors.OKCYAN}[INFO]{lib.colors.ENDC} Downloading {type.value.lower()} {lib.removeExtension(fileName)}..."
        )

        # Create the directory if it does not exist
        lib.createDir(dir)

        # Ask the user if they want to rewrite the file
        if confirmRewriteFile(stream, type):
            # Get the file count
            fileCount: int = lib.getFileCount(
                dir,
                lib.removeExtension(fileName),
            )

            # Ensure the file count is greater than 0
            if fileCount > 0:
                # Rename the file if it already exists
                fileName = f"{lib.removeExtension(fileName)}({fileCount - 1}).{lib.config['OUTPUT_FILE'][type.value.upper()]['EXTENSION']}"

        stream.download(output_path=dir, filename=fileName, max_retries=3)

        print(
            f"{lib.colors.OKGREEN}[SUCCESS]{lib.colors.ENDC} {type.value} {lib.removeExtension(fileName)} downloaded successfully into {dir}"
        )
    except Exception as e:
        print(
            f"{lib.colors.FAIL}[ERROR]{lib.colors.ENDC} Error downloading {type.value.lower()} {lib.removeExtension(fileName)}"
        )

        print(f"{lib.colors.FAIL}[ERROR]{lib.colors.ENDC} {e}")


def downloadVideo(url: str = "") -> None:
    """
    Function to download the video from the given URL

    :param url: The URL of the video
    :return: None
    """

    url = sanitizeURL(url)

    try:
        # Create a YouTube object
        yt: YouTube = YouTube(url)
    except Exception as e:
        print(f"{lib.colors.FAIL}[ERROR]{lib.colors.ENDC} Invalid youtube link")

        print(f"{lib.colors.FAIL}[ERROR]{lib.colors.ENDC} {e}")

        sys.exit(1)

    # Get the highest resolution stream
    streamVideo: Stream = (
        yt.streams.filter(adaptive=True).filter(mime_type="video/webm").first()
    )

    streamAudio: Stream = (
        yt.streams.filter(only_audio=True).order_by("abr").desc().first()
    )

    processes: list[Process] = [
        Process(target=downloadStream, args=(streamVideo, lib.enums.MediaType.VIDEO)),
        Process(
            target=downloadStream,
            args=(streamAudio, lib.enums.MediaType.AUDIO, ".temp"),
        ),
    ]

    # Start the processes
    for process in processes:
        process.start()

    # Wait for the processes to finish
    for process in processes:
        process.join()

    mergeVideoAudio(lib.removeExtension(streamVideo.default_filename))


def downloadAudio(url: str = "") -> None:
    """
    Function to download the audio from the given URL

    :param url: The URL of the video
    :return: None
    """

    url = sanitizeURL(url)

    try:
        # Create a YouTube object
        yt: YouTube = YouTube(url)
    except Exception as e:
        print(f"{lib.colors.FAIL}[ERROR]{lib.colors.ENDC} Invalid youtube link")

        print(f"{lib.colors.FAIL}[ERROR]{lib.colors.ENDC} {e}")

        sys.exit(1)

    stream: Stream = (
        yt.streams.filter(
            only_audio=True,
        )
        .order_by("abr")
        .desc()
        .first()
    )

    downloadStream(stream, lib.enums.MediaType.AUDIO)


def downloadPlaylistVideo(playlist: Playlist) -> None:
    """
    Function to download the playlist as video from the given URL

    :param playlist: The playlist object
    :return: None
    """

    for video in playlist.videos:
        if video.client.get_video(video.video_id).status == "Private":
            continue

        downloadStream(
            video.streams.get_highest_resolution(),
            lib.enums.MediaType.VIDEO,
            f"{playlist.title} {playlist.owner}",
        )


def downloadPlaylistAudio(playlist: Playlist) -> None:
    """
    Function to download the playlist audio only from the given URL

    :param playlist: The playlist object
    :return: None
    """

    for video in playlist.videos:
        if video.client.get_video(video.video_id).status == "Private":
            continue

        downloadStream(
            video.streams.filter(
                only_audio=True,
            )
            .order_by("abr")
            .desc()
            .first(),
            lib.enums.MediaType.AUDIO,
            f"{playlist.title} {playlist.owner}",
        )


def downloadPlaylist(type: lib.enums.MediaType, url: str = "") -> None:
    """
    Function to download the playlist from the given URL

    :param url: The URL of the playlist
    :return: None
    """

    url = sanitizeURL(url)

    try:
        # Create a Playlist object
        playlist: Playlist = Playlist(url)
    except Exception as e:
        print(f"{lib.colors.FAIL}[ERROR]{lib.colors.ENDC} Invalid youtube link")

        print(f"{lib.colors.FAIL}[ERROR]{lib.colors.ENDC} {e}")

        sys.exit(1)

    # Check if the playlist is private or not available or doesn't have any video
    try:
        if playlist.length == 0:
            print(
                f"{lib.colors.OKCYAN}[INFO]{lib.colors.ENDC} No video available in the playlist"
            )

            return
    except:
        print(
            f"{lib.colors.FAIL}[ERROR]{lib.colors.ENDC} Playlist is either private or not available"
        )

        return

    # Download the playlist based on the type
    if type == lib.MediaType.VIDEO:
        downloadPlaylistVideo(playlist)

        return

    downloadPlaylistAudio(playlist)


def sanitizeURL(url: str = "") -> str:
    """Function to sanitize the URL to a valid YouTube URL"""

    # Ensure the URL is not empty
    if lib.utils.strIsEmpty(url):
        print(f"{lib.colors.FAIL}[ERROR]{lib.colors.ENDC} Given URL is empty")
        sys.exit(1)

    return str.strip(url)
