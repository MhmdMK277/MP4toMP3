import argparse
import logging
from pathlib import Path

from moviepy import VideoFileClip
from yt_dlp import YoutubeDL

MP3_DIR = Path('MP3 files')
LOG_FILE = 'converter.log'


def setup_logging() -> None:
    """Configure logging to file."""
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(message)s'
    )


def ensure_output_dir() -> Path:
    """Ensure the output directory exists and return its Path."""
    MP3_DIR.mkdir(exist_ok=True)
    return MP3_DIR


def convert(input_path: str, output_path: Path | None = None) -> Path:
    """Convert an MP4 file to MP3."""
    input_path = Path(input_path)
    if output_path is None:
        output_path = ensure_output_dir() / input_path.with_suffix('.mp3').name
    else:
        output_path = Path(output_path)

    try:
        with VideoFileClip(str(input_path)) as video:
            audio = video.audio
            audio.write_audiofile(str(output_path))
        logging.info('Converted %s to %s', input_path, output_path)
    except Exception as e:
        logging.exception('Failed to convert %s', input_path)
        raise e
    return output_path


def select_file() -> str:
    """Try to open a GUI file selector; fall back to console input."""
    try:
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()
        path = filedialog.askopenfilename(title='Select video file')
        root.destroy()
        if path:
            return path
    except Exception as e:
        logging.warning('GUI file selector unavailable: %s', e)
    return input('Enter path to video file: ')


def convert_from_url(url: str) -> None:
    """Download a video from a URL and convert it to MP3."""
    ensure_output_dir()
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': str(MP3_DIR / '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'noplaylist': True,
    }
    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        logging.info('Downloaded and converted %s', url)
    except Exception:
        logging.exception('Failed to download %s', url)
        raise


def menu() -> None:
    """Display a simple menu for the user."""
    while True:
        print('\nSelect an option:')
        print('1. Convert a file on your PC')
        print('2. Convert a video link (YouTube and many others)')
        print('3. Exit')
        choice = input('Enter choice: ').strip()

        if choice == '1':
            path = select_file()
            convert(path)
        elif choice == '2':
            url = input('Paste video link: ').strip()
            convert_from_url(url)
        elif choice == '3':
            break
        else:
            print('Invalid option. Please try again.')


def main() -> None:
    setup_logging()
    parser = argparse.ArgumentParser(description='MP4/Online video to MP3 converter')
    parser.add_argument('--cli', action='store_true', help='Run using command line arguments (old behavior)')
    parser.add_argument('input', nargs='?', help='Path to the MP4 file')
    parser.add_argument('output', nargs='?', help='Optional output MP3 file path')
    args = parser.parse_args()

    if args.cli and args.input:
        convert(args.input, args.output)
    else:
        menu()


if __name__ == '__main__':
    main()
