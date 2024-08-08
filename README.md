# YT Downloader

Simple Python API to download any youtube videos or playlists in any video or audio format.

## Requirements
- **Python** >= 3.7
- **pip**
- **ffmpeg** [Check this out](https://www.ffmpeg.org/)

## Installation

1. **Clone the repository**

```
git clone https://github.com/bryanfks-dev/YT-Downloader.git
```

2. **Modify config.py as you like**

```
#/lib/config.py

{
    "OUTPUT_FILE": {
        "VIDEO": {
            # The extension of the video file
            # e.g mp4, mkv, etc.
            "EXTENSION": "mp4",
            "PATH": "./videos/",
        },
        "AUDIO": {
            # The extension of the audio file
            # e.g mp3, m4a, etc.
            "EXTENSION": "mp3",
            "PATH": "./audios/",
        },
    }
}
```

3. **Install needed depedency**

```bash
pip install requirements.txt
```

4. **Run main.py**

```bash
python main.py
```
