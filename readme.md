# YouTube Downloader

This repository contains a Python script to download videos or playlists from YouTube, with the option to choose between mp3 and mp4 formats. The script automatically checks and installs necessary packages and ensures FFmpeg is installed on the system.

## Supported Platforms

- **Windows**
- **Linux**:
  - Debian-based distributions (e.g., Ubuntu)
  - Arch-based distributions (e.g., Manjaro)

## Requirements

- Python 3.6 or higher
- [pip](https://pip.pypa.io/en/stable/installation/)
- [winget](https://github.com/microsoft/winget-cli) (Windows only, used to install FFmpeg)

## Installation

1. Clone this repository:
    ```sh
    git clone https://github.com/MkBadKarma/YouTubeDownloader.git
    cd YouTubeDownloader
    ```

2. Run the script to install the necessary packages:
    ```sh
    python youtubeDownloader.py
    ```

## Usage

1. Run the script:
    ```sh
    python youtubeDownloader.py
    ```

2. Follow the terminal instructions to:
    - Enter the URL of the YouTube video or playlist.
    - Select the download format (mp3 or mp4).
    - Choose the destination folder to save the downloaded file.

## Script Functionality

1. **Package Verification and Installation**: The script checks if `rich`, `questionary`, `yt_dlp`, and `PyQt5` packages are installed. If not, it installs them automatically.

2. **FFmpeg Verification and Installation**: 
   - **Windows**: Checks if FFmpeg is installed. If not, offers to install it using `winget`.
   - **Linux**: Checks if FFmpeg is installed. If not, offers to install it using `apt` for Debian-based distributions or `pacman` for Arch-based distributions.

3. **User Interface**: Uses `questionary` to prompt the user for the video URL, download format, and destination folder. `PyQt5` is used for selecting the destination folder.

4. **Video Download**: Utilizes `yt_dlp` to download the video or playlist in the selected format, showing the download progress in the terminal.

## Dependencies

- [rich](https://github.com/Textualize/rich): For formatted terminal output.
- [questionary](https://github.com/tmbo/questionary): For creating interactive prompts in the terminal.
- [yt-dlp](https://github.com/yt-dlp/yt-dlp): For downloading YouTube videos.
- [PyQt5](https://pypi.org/project/PyQt5/): For the graphical folder selection interface.

## Contributions

Contributions are welcome. Please open an issue or submit a pull request to contribute to this project.