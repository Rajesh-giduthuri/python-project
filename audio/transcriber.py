import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_STT_MODEL = os.getenv("GROQ_STT_MODEL", "whisper-large-v3")

if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY is not set in .env")

client = Groq(api_key=GROQ_API_KEY)


def format_timestamp(seconds: float) -> str:
    """Convert seconds into HH:MM:SS format."""

    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)

    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def transcribe_chunk_groq(
    chunk_path: str,
    language: str = "english"
) -> list:
    """Transcribe one audio chunk using Groq Whisper with timestamps."""

    if not os.path.exists(chunk_path):
        raise FileNotFoundError(
            f"Audio chunk not found: {chunk_path}"
        )

    print(f"Sending to Groq Whisper: {chunk_path}")

    with open(chunk_path, "rb") as audio_file:

        transcription = client.audio.transcriptions.create(
            file=audio_file,
            model=GROQ_STT_MODEL,
            language="en" if language.lower() == "english" else None,
            response_format="verbose_json",
            timestamp_granularities=["segment"],
        )

    segments = []

    for segment in transcription.segments:

        segments.append({
            "start": segment["start"],
            "end": segment["end"],
            "text": segment["text"].strip()
        })

    if not segments:
        raise ValueError(
            f"Groq returned an empty transcription for: {chunk_path}"
        )

    return segments


def transcribe_all(
    chunks: list,
    language: str = "english"
) -> str:
    """Transcribe all chunks and create one timestamped transcript."""

    if not chunks:
        raise ValueError(
            "No audio chunks provided for transcription."
        )

    full_transcript = []
    total_chunks = len(chunks)

    print("\n========== GROQ TRANSCRIPTION ==========")

    # Your current chunk size
    CHUNK_DURATION = 5 * 60

    for i, chunk_path in enumerate(chunks):

        print(
            f"\nTranscribing chunk "
            f"{i + 1}/{total_chunks}..."
        )

        segments = transcribe_chunk_groq(
            chunk_path,
            language=language
        )

        # Add the correct time offset for this chunk
        chunk_offset = i * CHUNK_DURATION

        for segment in segments:

            start = segment["start"] + chunk_offset
            end = segment["end"] + chunk_offset

            text = segment["text"]

            timestamp = (
                f"[{format_timestamp(start)} - "
                f"{format_timestamp(end)}]"
            )

            full_transcript.append(
                f"{timestamp} {text}"
            )

        print(f"Chunk {i + 1} completed.")

    transcript = "\n".join(full_transcript).strip()

    if not transcript:
        raise ValueError(
            "Transcription resulted in empty text."
        )

    print(
        "\n========== TRANSCRIPTION COMPLETE =========="
    )

    print(f"Chunks processed: {total_chunks}")
    print(f"Transcript characters: {len(transcript)}")

    return transcript