import colors
import sys
import os
import utils
import config

# Try-catch import required external libs
try:
    from pytubefix import YouTube, Stream
except ImportError:
    print(
        f"{colors.FAIL}[ERROR]{colors.ENDC} There are missing external libs. Please install using `pip install requirements.txt`"
    )


def confirmRewriteFile(path: str) -> bool:
    """Function to check if the file already exists in the given path"""

    # Check if the filemame already exists
    if not os.path.exists(path):
        return True

    while True:
        # Ask the user if they want to rewrite the file
        ans: str = str.upper(
            input(
                f"{colors.WARNING}[WARNING]{colors.ENDC} File with this name already exists. Do you want to rewrite the file? [Y/N]"
            )
        )

        # Check if the input is valid
        if [ans != "Y", ans != "N"]:
            print(
                f"{colors.FAIL}[ERROR]{colors.ENDC} Invalid input. Please enter Y or N"
            )

        if ans == "Y":
            return True

        if ans == "N":
            return False


def downloadStream(stream: Stream | None) -> None:
    """Function to download the stream"""

    # Get the file name
    fileName: str = stream.default_filename

    rewrite: bool = confirmRewriteFile(f"{fileName}{stream.exists_at_path}")

    try:
        # Download the video
        print(f"{colors.OKCYAN}[INFO]{colors.ENDC} Downloading video {fileName}...")

        stream.download(
            output_path=config["OUTPUT_FILE"]["VIDEO"]["PATH"],
            filename=f"{fileName}.mp4",
        )

        print(
            f"{colors.OKGREEN}[SUCCESS]{colors.ENDC} Video {fileName} downloaded successfully"
        )
    except:
        print(f"{colors.FAIL}[ERROR]{colors.ENDC} Error downloading the video")


def downloadVideo(url: str = "") -> None:
    """Function to download the video from the given URL"""
    url = sanitizeURL(url)

    try:
        # Create a YouTube object
        yt: YouTube = YouTube(url)
    except:
        print(f"{colors.FAIL}[ERROR]{colors.ENDC} Connection error")

    # Get the highest resolution stream
    stream = (
        yt.streams.filter(progressive=True, file_extension="mp4")
        .order_by("resolution")
        .desc()
        .first()
    )

    downloadStream(stream)


def sanitizeURL(url: str = "") -> str:
    """Function to sanitize the URL to a valid YouTube URL"""

    # Ensure the URL is not empty
    if utils.strIsEmpty(url):
        print(f"{colors.FAIL}[ERROR]{colors.ENDC} Given URL is empty")
        sys.exit(1)

    return str.strip(url)


def main() -> None:
    """Main driver to download the file"""
    downloadVideo("https://www.youtube.com/watch?v=0yqnWZJ3xl8&list=RD0yqnWZJ3xl")
    return


if __name__ == "__main__":
    main()
