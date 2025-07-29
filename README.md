# MP4 to MP3 Converter

Convert `.mp4` video files or online videos to `.mp3` audio using Python.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Running the script without arguments will display a menu:

```bash
python mp4_to_mp3.py
```

You can choose to convert a local file or paste a link from YouTube or any other platform supported by `yt-dlp`. Converted files are saved in the `MP3 files` folder.

If you prefer the old behaviour of specifying files directly, use the `--cli` flag:

```bash
python mp4_to_mp3.py --cli input_video.mp4 [output_audio.mp3]
```

## Contributing

1. Make your changes.
2. Commit with an informative message.
3. Push your branch to your repository.
