import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="Download videos or playlists from YouTube in the specified format.")
    parser.add_argument('-f', '--format', choices=['mp3', 'mp4'], help="Specify the format for download (mp3 or mp4).")
    parser.add_argument('-q', '--quality', choices=['144p', '240p', '360p', '480p', '720p', '1080p', '1440p', '2160p'], help="Specify the video quality.")
    parser.add_argument('url', nargs='?', help="The URL of the video or playlist to download.")
    parser.add_argument('-o', '--output', default=None, help="Path where to save the output.")
    return parser.parse_args()