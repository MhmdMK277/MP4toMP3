import argparse
from pathlib import Path
from moviepy.editor import VideoFileClip

def convert(input_path: str, output_path: str | None = None) -> Path:
    """Convert an MP4 file to MP3."""
    input_path = Path(input_path)
    if output_path is None:
        output_path = input_path.with_suffix('.mp3')
    else:
        output_path = Path(output_path)

    with VideoFileClip(str(input_path)) as video:
        audio = video.audio
        audio.write_audiofile(str(output_path))
    return output_path


def main() -> None:
    parser = argparse.ArgumentParser(description='Convert MP4 video files to MP3 audio.')
    parser.add_argument('input', help='Path to the MP4 file')
    parser.add_argument('output', nargs='?', help='Optional output MP3 file path')
    args = parser.parse_args()

    convert(args.input, args.output)


if __name__ == '__main__':
    main()
