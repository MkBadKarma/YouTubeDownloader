import os
import shutil
import subprocess
import sys
import importlib
import platform
from rich.console import Console

console = Console()

def install_package(package):
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

# Lista de paquetes necesarios
packages = [
    ("rich", "rich"),
    ("questionary", "questionary"),
    ("yt_dlp", "yt-dlp"),
    ("PyQt5", "PyQt5")
]

# Comprobar e instalar paquetes necesarios
check_packages(packages)

# Ahora que los paquetes están verificados e instalados, podemos importarlos
from rich.panel import Panel
import argparse
import questionary
import yt_dlp as youtube_dl
from PyQt5.QtWidgets import QApplication, QFileDialog, QDialog
from PyQt5.QtCore import Qt

def check_ffmpeg_installed():
    return shutil.which("ffmpeg") is not None

def get_lin_distro():
    if shutil.which("apt"):
        return "debian"
    elif shutil.which("pacman"):
        return "arch"
    return None

def install_ffmpeg():
    console.print(Panel("FFmpeg is not installed.", title="Installation Required", title_align="left", border_style="bold red"))
    command = []
    
    if platform.system() == "Windows":
        command = ["winget", "install", "--id=Gyan.FFmpeg", "-e"]
    elif platform.system() == "Linux":
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

def download_video_or_playlist(url=None, format_choice=None):
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
    parser = argparse.ArgumentParser(description="Download videos or playlists from YouTube in the specified format.")
    parser.add_argument('-f', '--format', choices=['mp3', 'mp4'], help="Specify the format for download (mp3 or mp4).")
    parser.add_argument('url', nargs='?', help="The URL of the video or playlist to download.")
    args = parser.parse_args()

    if args.url and args.format:
        download_video_or_playlist(args.url, args.format)
    else:
        url = get_url()
        if not url:
            sys.exit(1)
        format_choice = get_format_choice()
        if not format_choice:
            sys.exit(1)
        download_video_or_playlist(url, format_choice)
