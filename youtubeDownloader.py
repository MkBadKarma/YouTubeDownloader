from rich.console import Console
from rich.panel import Panel
import questionary
import yt_dlp as youtube_dl
import subprocess
from PyQt5.QtWidgets import QApplication, QFileDialog, QDialog
from PyQt5.QtCore import Qt
import os
import sys
import importlib

console = Console()

def check_ffmpeg_installed():
    try:
        subprocess.run(["ffmpeg", "-version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def install_ffmpeg():
    console.print(Panel("FFmpeg no está instalado.", title="Instalación Requerida", title_align="left", border_style="bold red"))
    if questionary.confirm("¿Deseas instalar FFmpeg ahora?").ask():
        console.print("Instalando FFmpeg...", style="bold yellow")
        if subprocess.run(["winget", "install", "--id=Gyan.FFmpeg", "-e"]).returncode == 0:
            console.print("Por favor, reinicia la aplicación o la terminal para que los cambios surtan efecto.", style="bold green")
        else:
            console.print("La instalación de FFmpeg falló. Por favor, instálalo manualmente.", style="bold red")
        sys.exit(0)
    else:
        console.print("No se puede continuar sin FFmpeg. Por favor, instálalo y vuelve a intentarlo.", style="bold red")
        sys.exit(1)

def instalar_paquete(paquete):
    subprocess.check_call([sys.executable, "-m", "pip", "install", paquete])

def verificar_paquetes(paquetes):
    for nombre_modulo, nombre_paquete in paquetes:
        try:
            importlib.import_module(nombre_modulo)
        except ImportError:
            console.print(f"{nombre_modulo} no está instalado. Instalando...", style="bold yellow")
            instalar_paquete(nombre_paquete)

def get_url():
    url = questionary.text("Ingrese la URL del video o playlist (debe comenzar con http:// o https://):").ask().strip()
    if not url.startswith(('http://', 'https://')):
        console.print("URL no válida. Debe comenzar con http:// o https://.", style="bold red")
        return None
    return url

def get_format_choice():
    format_choice = questionary.select("¿Qué formato deseas para el archivo descargado?", choices=["mp3", "mp4"]).ask()
    if not format_choice:
        console.print("No se seleccionó un formato. La descarga no continuará.", style="bold red")
        return None
    return format_choice

def get_target_directory(dialog):
    default_dir = os.path.expanduser("~/Downloads/")
    target_dir = QFileDialog.getExistingDirectory(dialog, "Selecciona la carpeta de destino", default_dir)
    if not target_dir:
        console.print("No se seleccionó una carpeta. La descarga no continuará.", style="bold red")
        return None
    return target_dir

def progress_hook(d):
    if d['status'] == 'finished':
        console.print(f"\rDescarga finalizada: {d['filename']}", style="bold green")

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

    console.print("Iniciando descarga...", style="bold yellow")
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        console.print("¡Descarga completa!", style="bold green")
    except Exception as e:
        console.print(f"Se produjo un error: {e}", style="bold red")

if __name__ == "__main__":
    paquetes = [
        ("rich", "rich"),
        ("questionary", "questionary"),
        ("yt_dlp", "yt-dlp"),
        ("PyQt5", "PyQt5")
    ]
    verificar_paquetes(paquetes)
    download_video_or_playlist()
