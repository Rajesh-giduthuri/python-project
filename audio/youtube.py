from pathlib import Path

import yt_dlp

from config.settings import UPLOAD_DIR


def download_youtube_audio(
    youtube_url: str
) -> Path:
    """
    Download audio from a YouTube video.

    Returns:
        Path: Path to the downloaded audio file.
    """

    if not youtube_url.strip():
        raise ValueError(
            "YouTube URL cannot be empty."
        )

    output_template = str(
        UPLOAD_DIR / "%(title)s.%(ext)s"
    )

    ydl_options = {
        "format": "bestaudio/best",
        "outtmpl": output_template,
        "noplaylist": True,
        "quiet": False,
    }

    print(
        "\nDownloading YouTube audio..."
    )

    with yt_dlp.YoutubeDL(
        ydl_options
    ) as ydl:

        info = ydl.extract_info(
            youtube_url,
            download=True
        )

        downloaded_file = Path(
            ydl.prepare_filename(info)
        )

    print(
        f"\nYouTube audio downloaded:"
        f"\n{downloaded_file}"
    )

    return downloaded_file


if __name__ == "__main__":

    url = input(
        "Enter YouTube URL: "
    ).strip()

    file_path = download_youtube_audio(
        url
    )

    print(
        f"\nDownloaded file:\n{file_path}"
    )