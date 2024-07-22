# YouTube Downloader

Este repositorio contiene un script de Python para descargar videos o playlists de YouTube, con la opción de elegir entre formatos mp3 y mp4. El script verifica e instala automáticamente los paquetes necesarios y se asegura de que FFmpeg esté instalado en el sistema en caso de usar Windows.

## Requisitos

- Python 3.6 o superior
- [pip](https://pip.pypa.io/en/stable/installation/)
- [winget](https://github.com/microsoft/winget-cli) (solo para Windows, utilizado para instalar FFmpeg)

## Instalación

1. Clona este repositorio:
    ```sh
    git clone https://github.com/MkBadKarma/YouTubeDownloader.git
    cd youtube-downloader
    ```

2. Ejecuta el script para instalar los paquetes necesarios:
    ```sh
    python youtubeDownloader.py
    ```

## Uso

1. Ejecuta el script:
    ```sh
    python youtubeDownloader.py
    ```

2. Sigue las instrucciones en la terminal para:
    - Ingresar la URL del video o playlist de YouTube.
    - Seleccionar el formato de descarga (mp3 o mp4).
    - Seleccionar la carpeta de destino para guardar el archivo descargado.

## Funcionamiento del Script

1. **Verificación e instalación de paquetes**: El script verifica si los paquetes `rich`, `questionary`, `yt_dlp` y `PyQt5` están instalados. Si no lo están, los instala automáticamente.

2. **Verificación de FFmpeg(Solo si tienes windows)**: Comprueba si FFmpeg está instalado en el sistema. Si no lo está, ofrece instalarlo utilizando `winget`.

3. **Interfaz de usuario**: Utiliza `questionary` para solicitar al usuario la URL del video, el formato de descarga y la carpeta de destino. `PyQt5` se utiliza para seleccionar la carpeta de destino.

4. **Descarga del video**: Utiliza `yt_dlp` para descargar el video o playlist en el formato seleccionado, mostrando el progreso de la descarga en la terminal.

## Dependencias

- [rich](https://github.com/Textualize/rich): Para una salida formateada en la terminal.
- [questionary](https://github.com/tmbo/questionary): Para crear prompts interactivos en la terminal.
- [yt-dlp](https://github.com/yt-dlp/yt-dlp): Para descargar videos de YouTube.
- [PyQt5](https://pypi.org/project/PyQt5/): Para la interfaz gráfica de selección de carpeta.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o envía un pull request para contribuir a este proyecto.
