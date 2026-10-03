
import os
from pathlib import Path
from pydub import AudioSegment

TARGET_SAMPLE_RATE = 16000
CHUNK_MINUTES = 5


def normalize_audio(audio: AudioSegment) -> AudioSegment:
    """Convert audio to mono 16 kHz."""
    return (
        audio
        .set_channels(1)
        .set_frame_rate(TARGET_SAMPLE_RATE)
    )


def convert_to_wav(input_path: str) -> str:
    """Convert any supported input audio/video file to WAV."""

    input_path = Path(input_path)

    if not input_path.exists():
        raise FileNotFoundError(
            f"Input file not found: {input_path}"
        )

    output_path = input_path.with_name(
        input_path.stem + "_converted.wav"
    )

    print(f"Converting: {input_path.name}")

    # Do NOT pass metadata_errors.
    # pydub handles the input through ffmpeg.
    audio = AudioSegment.from_file(
        str(input_path)
    )

    audio = normalize_audio(audio)

    audio.export(
        str(output_path),
        format="wav"
    )

    print(f"Converted: {output_path}")

    return str(output_path)


def chunk_audio(
    wav_path: str,
    chunk_minutes: int = CHUNK_MINUTES
) -> list:

    wav_path = Path(wav_path)

    if not wav_path.exists():
        raise FileNotFoundError(
            f"WAV file not found: {wav_path}"
        )

    audio = AudioSegment.from_wav(
        str(wav_path)
    )

    audio = normalize_audio(audio)

    chunk_ms = chunk_minutes * 60 * 1000

    chunks = []

    for index, start in enumerate(
        range(0, len(audio), chunk_ms)
    ):

        chunk = audio[start:start + chunk_ms]

        if len(chunk) == 0:
            continue

        chunk_path = wav_path.with_name(
            f"{wav_path.stem}_chunk_{index}.wav"
        )

        chunk.export(
            str(chunk_path),
            format="wav"
        )

        chunks.append(str(chunk_path))

        print(
            f"Created chunk {index + 1}: "
            f"{chunk_path.name}"
        )

    print(
        f"\nTotal chunks created: {len(chunks)}"
    )

    return chunks


def process_audio(input_file: str) -> list:
    """Complete audio preprocessing pipeline."""

    input_file = str(input_file)

    if not os.path.exists(input_file):
        raise FileNotFoundError(
            f"File not found: {input_file}"
        )

    print("\n========== AUDIO PROCESSING ==========")

    wav_path = convert_to_wav(input_file)

    print("Splitting audio into chunks...")

    chunks = chunk_audio(wav_path)

    if not chunks:
        raise RuntimeError(
            "No audio chunks were created."
        )

    print("Audio processing completed successfully.")

    return chunks
