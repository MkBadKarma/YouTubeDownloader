import os
import shutil
import subprocess
import sys
import importlib
import platform
from rich.console import Console
from flags import parse_args  # Import the flags defined in flags.py

console = Console()

def install_package(package):
    # Install a Python package using pip
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def check_packages(packages):
    missing_modules = 0
    for module_name, package_name in packages:
        try:
            importlib.import_module(module_name)
        except ImportError:
            missing_modules += 1
            console.print(f"{module_name} is not installed. Installing...", style="bold yellow")
            install_package(package_name)

    if missing_modules > 0:
        console.print(f"Missing modules ({missing_modules}) installed. Please restart the script.", style="bold green")
        exit(1)

# List of required packages
packages = [
    ("rich", "rich"),
    ("questionary", "questionary"),
    ("yt_dlp", "yt-dlp"),
    ("PyQt5", "PyQt5")
]

# Check and install required packages
check_packages(packages)

# Now that the packages are verified and installed, we can import them
from rich.panel import Panel
import questionary
import yt_dlp as youtube_dl
from PyQt5.QtWidgets import QApplication, QFileDialog, QDialog
from PyQt5.QtCore import Qt

def check_ffmpeg_installed():
    # Check if FFmpeg is installed
    return shutil.which("ffmpeg") is not None

def get_lin_distro():
    # Determine the Linux distribution
    if shutil.which("apt"):
        return "debian"
    elif shutil.which("pacman"):
        return "arch"
    return None

def install_ffmpeg():
    console.print(Panel("FFmpeg is not installed.", title="Installation Required", title_align="left", border_style="bold red"))
    command = []
    
    if platform.system() == "Windows":
        # Command to install FFmpeg on Windows
        command = ["winget", "install", "--id=Gyan.FFmpeg", "-e"]
    elif platform.system() == "Linux":
        # Command to install FFmpeg on Linux
        match get_lin_distro():
            case "debian":
                command = ["sudo", "apt", "install", "ffmpeg"]
            case "arch":
                command = ["sudo", "pacman", "-S", "ffmpeg"]
            case _:
                console.print("This script doesn't support your current GNU/Linux distribution. You have to install ffmpeg manually to continue.", style="bold red")
                return
    else:
        console.print(f"This script doesn't support your current platform ({platform.system()}). You have to install ffmpeg manually to continue.", style="bold red")
        return
    
    if questionary.confirm("Do you want to install FFmpeg now?").ask():
        console.print(f"Installing FFmpeg with the following command: '{command}'...", style="bold yellow")
        if subprocess.run(command).returncode == 0:
            console.print("Please restart the application or terminal for the changes to take effect (Windows only).", style="bold green")
        else:
            console.print("FFmpeg installation failed. Please install it manually.", style="bold red")
        exit(0)
    else:
        console.print("Cannot continue without FFmpeg. Please install it and try again.", style="bold red")
        exit(1)

def get_url():
    # Prompt the user for the video or playlist URL
    url = questionary.text("Enter the video or playlist URL (must start with http:// or https://):").ask().strip()
    if not url.startswith(('http://', 'https://')):
        console.print("Invalid URL. It must start with http:// or https://.", style="bold red")
        return None
    return url

def get_format_choice():
    # Prompt the user for the desired download format
    format_choice = questionary.select("What format do you want for the downloaded file?", choices=["mp3", "mp4"]).ask()
    if not format_choice:
        console.print("No format selected. The download will not continue.", style="bold red")
        return None
    return format_choice

def get_quality_choice():
    # Prompt the user for the desired download quality
    quality_choice = questionary.select("What quality do you want for the downloaded file?", choices=["144p", "240p", "360p", "480p", "720p", "1080p", "1440p", "2160p"]).ask()
    if not quality_choice:
        console.print("No quality selected. The download will not continue.", style="bold red")
        return None
    return quality_choice

def get_target_directory(dialog):
    # Prompt the user to select a target directory for the download
    default_dir = os.path.expanduser("~/Downloads/")
    target_dir = QFileDialog.getExistingDirectory(dialog, "Select the target folder", default_dir)
    if not target_dir:
        console.print("No folder selected. The download will not continue.", style="bold red")
        return None
    return target_dir

def progress_hook(d):
    # Hook to display progress of the download
    if d['status'] == 'finished':
        console.print(f"\nDownload completed: {d['filename']}", style="bold green")

def check_video_quality(url, quality):
    ydl_opts = {'format': 'best'}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        available_qualities = [f"{f['format_id']} ({f['height']}p)" for f in info_dict['formats'] if f.get('height')]
        requested_quality = int(quality.replace('p', '').replace('k', '000'))
        available_heights = [f['height'] for f in info_dict['formats'] if f.get('height')]
        if requested_quality in available_heights:
            return True, None
        else:
            return False, available_qualities

def download_video_or_playlist(url=None, format_choice=None, quality_choice=None, output_path=None):
    # Ensure FFmpeg is installed before proceeding
    if not check_ffmpeg_installed():
        install_ffmpeg()

    app = QApplication(sys.argv)
    dialog = QDialog()
    dialog.setWindowFlags(dialog.windowFlags() | Qt.WindowStaysOnTopHint)

    if not url:
        url = get_url()
        if not url:
            return

    if not format_choice:
        format_choice = get_format_choice()
        if not format_choice:
            return

    if format_choice == 'mp4':
        if not quality_choice:
            quality_choice = get_quality_choice()
            if not quality_choice:
                return

        quality_check, available_qualities = check_video_quality(url, quality_choice)
        if not quality_check:
            console.print(f"Requested quality {quality_choice} is not available. Available qualities are: {', '.join(available_qualities)}", style="bold yellow")
            return

        format_option = f'bestvideo[height<={quality_choice.replace("p", "")}]+bestaudio/best'
    else:
        format_option = 'bestaudio/best'

    outtmpl = ""
    if output_path:
        outtmpl = output_path
    else:
        target_dir = get_target_directory(dialog)
        if not target_dir:
            return
        outtmpl = os.path.join(target_dir, '%(title)s.%(ext)s')

    ydl_opts = {
        'format': format_option,
        'outtmpl': outtmpl,
        'merge_output_format': 'mp4' if format_choice == 'mp4' else None,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }] if format_choice == 'mp3' else [],
        'progress_hooks': [progress_hook],
        'noplaylist': False,
    }

    console.print("Starting download...", style="bold yellow")
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        console.print("Download complete!", style="bold green")
    except Exception as e:
        console.print(f"An error occurred: {e}", style="bold red")

if __name__ == "__main__":
    args = parse_args()  # Call the flags from flags.py

    if args.url and args.format:
        download_video_or_playlist(args.url, args.format, args.quality, args.output)
    else:
        url = get_url()
        if not url:
            exit(1)
        format_choice = get_format_choice()
        if not format_choice:
            exit(1)
        if format_choice == 'mp4':
            quality_choice = get_quality_choice()
            if not quality_choice:
                exit(1)
        else:
            quality_choice = None
        download_video_or_playlist(url, format_choice, quality_choice)
