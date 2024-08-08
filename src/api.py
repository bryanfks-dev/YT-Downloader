import lib
import sys

# Try-catch import required external libs
try:
    from pytubefix import YouTube, Stream
except ImportError:
    print(
        f"{lib.colors.FAIL}[ERROR]{lib.colors.ENDC} There are missing external libs. Please install using `pip install requirements.txt`"
    )


def constructFileName(fileNameWithoutExt: str, type: lib.enumurates.MediaType) -> str:
    """
    Function to construct the file name

    :param fileNameWithoutExt: The file name without the extension
    :param type: The type of the file
    :return: The constructed file name
    """

    return f"{fileNameWithoutExt}.{lib.config['OUTPUT_FILE'][type.value.upper()]['EXTENSION']}"


def confirmRewriteFile(stream: Stream, type: lib.enumurates.MediaType) -> bool:
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


def downloadStream(stream: Stream, type: lib.enumurates.MediaType) -> None:
    """
    Function to download the stream

    :param stream: The stream to download
    :param type: The type of the stream
    :return: None
    """

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
        lib.createDir(lib.config["OUTPUT_FILE"][type.value.upper()]["PATH"])

        # Ask the user if they want to rewrite the file
        if confirmRewriteFile(stream, type):
            # Get the file count
            fileCount: int = lib.getFileCount(
                lib.config["OUTPUT_FILE"][type.value.upper()]["PATH"],
                lib.removeExtension(fileName),
            )

            # Ensure the file count is greater than 0
            if fileCount > 0:
                # Rename the file if it already exists
                fileName = f"{lib.removeExtension(fileName)}({fileCount - 1}).{lib.config['OUTPUT_FILE'][type.value.upper()]['EXTENSION']}"

        stream.download(
            output_path=lib.config["OUTPUT_FILE"][type.value.upper()]["PATH"],
            filename=fileName,
        )

        print(
            f"{lib.colors.OKGREEN}[SUCCESS]{lib.colors.ENDC} {type.value} {lib.removeExtension(fileName)} downloaded successfully into {lib.config['OUTPUT_FILE'][type.value.upper()]['PATH']}"
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
        print(f"{lib.colors.FAIL}[ERROR]{lib.colors.ENDC} Connection error")

        print(f"{lib.colors.FAIL}[ERROR]{lib.colors.ENDC} {e}")

    # Get the highest resolution stream
    stream: Stream = yt.streams.filter(
        progressive=True,
    ).get_highest_resolution()

    downloadStream(stream, lib.enumurates.MediaType.VIDEO)


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
        print(f"{lib.colors.FAIL}[ERROR]{lib.colors.ENDC} Connection error")

        print(f"{lib.colors.FAIL}[ERROR]{lib.colors.ENDC} {e}")

    stream: Stream = (
        yt.streams.filter(
            only_audio=True,
        )
        .order_by("abr")
        .desc()
        .first()
    )

    downloadStream(stream, lib.enumurates.MediaType.AUDIO)


def sanitizeURL(url: str = "") -> str:
    """Function to sanitize the URL to a valid YouTube URL"""

    # Ensure the URL is not empty
    if lib.utils.strIsEmpty(url):
        print(f"{lib.colors.FAIL}[ERROR]{lib.colors.ENDC} Given URL is empty")
        sys.exit(1)

    return str.strip(url)
