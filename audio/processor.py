from pathlib import Path

from pydub import AudioSegment


# --------------------------------------------------
# AUDIO SETTINGS
# --------------------------------------------------

TARGET_SAMPLE_RATE = 16000
TARGET_CHANNELS = 1
TARGET_SAMPLE_WIDTH = 2  # 16-bit audio


# --------------------------------------------------
# PROCESS AUDIO
# --------------------------------------------------

def process_audio(input_path: str | Path) -> Path:
    """
    Convert an audio/video file into a normalized
    16 kHz, mono, 16-bit WAV file.

    Returns:
        Path: Path to the processed WAV file.
    """

    input_path = Path(input_path)

    if not input_path.exists():
        raise FileNotFoundError(
            f"Input file not found: {input_path}"
        )

    # Create output filename
    output_path = input_path.with_name(
        f"{input_path.stem}_processed.wav"
    )

    print(f"Processing: {input_path.name}")

    # Load audio/video
    audio = AudioSegment.from_file(input_path)

    print(
        f"Original audio: "
        f"{audio.frame_rate} Hz, "
        f"{audio.channels} channel(s)"
    )

    # Convert to:
    # 16 kHz
    # Mono
    # 16-bit
    audio = (
        audio
        .set_frame_rate(TARGET_SAMPLE_RATE)
        .set_channels(TARGET_CHANNELS)
        .set_sample_width(TARGET_SAMPLE_WIDTH)
    )

    # Export WAV
    audio.export(
        output_path,
        format="wav"
    )

    print(
        f"Processed audio saved to: "
        f"{output_path}"
    )

    return output_path


# # --------------------------------------------------
# # TEST FUNCTION
# # --------------------------------------------------

# if __name__ == "__main__":
#     print("Audio Processor Test")
#     input_file = r"C:\Users\rajes\OneDrive\Desktop\AI_MEETING_INTELLIGENCE\uploads\short_meeting-3.webm"

#     process_audio(input_file)