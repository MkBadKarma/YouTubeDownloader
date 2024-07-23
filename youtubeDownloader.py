import subprocess
import sys
import importlib

def install_package(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def check_packages(packages):
    for module_name, package_name in packages:
        try:
            importlib.import_module(module_name)
        except ImportError:
            print(f"{module_name} is not installed. Installing...")
            install_package(package_name)

# List of necessary packages
packages = [
    ("rich", "rich"),
    ("questionary", "questionary"),
    ("yt_dlp", "yt-dlp"),
    ("PyQt5", "PyQt5")
]

# Check and install necessary packages
check_packages(packages)

# Now that the packages are checked and installed, we can import them
from rich.console import Console
from rich.panel import Panel
import questionary
import yt_dlp as youtube_dl
from PyQt5.QtWidgets import QApplication, QFileDialog, QDialog
from PyQt5.QtCore import Qt
import os

console = Console()

def check_ffmpeg_installed():
    try:
        subprocess.run(["ffmpeg", "-version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def install_ffmpeg():
    console.print(Panel("FFmpeg is not installed.", title="Installation Required", title_align="left", border_style="bold red"))
    if questionary.confirm("Do you want to install FFmpeg now?").ask():
        console.print("Installing FFmpeg...", style="bold yellow")
        if subprocess.run(["winget", "install", "--id=Gyan.FFmpeg", "-e"]).returncode == 0:
            console.print("Please restart the application or terminal for the changes to take effect.", style="bold green")
        else:
            console.print("FFmpeg installation failed. Please install it manually.", style="bold red")
        sys.exit(0)
    else:
        console.print("Cannot continue without FFmpeg. Please install it and try again.", style="bold red")
        sys.exit(1)

def get_url():
    url = questionary.text("Enter the video or playlist URL (must start with http:// or https://):").ask().strip()
    if not url.startswith(('http://', 'https://')):
        console.print("Invalid URL. It must start with http:// or https://.", style="bold red")
        return None
    return url

def get_format_choice():
    format_choice = questionary.select("What format do you want for the downloaded file?", choices=["mp3", "mp4"]).ask()
    if not format_choice:
        console.print("No format selected. The download will not continue.", style="bold red")
        return None
    return format_choice

def get_target_directory(dialog):
    default_dir = os.path.expanduser("~/Downloads/")
    target_dir = QFileDialog.getExistingDirectory(dialog, "Select the target folder", default_dir)
    if not target_dir:
        console.print("No folder selected. The download will not continue.", style="bold red")
        return None
    return target_dir

def progress_hook(d):
    if d['status'] == 'finished':
        console.print(f"\rDownload completed: {d['filename']}", style="bold green")

def download_video_or_playlist():
    if not check_ffmpeg_installed():
        install_ffmpeg()

    app = QApplication(sys.argv)
    dialog = QDialog()
    dialog.setWindowFlags(dialog.windowFlags() | Qt.WindowStaysOnTopHint)

    url = get_url()
    if not url:
        return

    format_choice = get_format_choice()
    if not format_choice:
        return

    target_dir = get_target_directory(dialog)
    if not target_dir:
        return

    outtmpl = os.path.join(target_dir, '%(title)s.%(ext)s')
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best' if format_choice == 'mp4' else 'bestaudio/best',
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
    download_video_or_playlist()
