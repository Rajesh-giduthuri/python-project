import os
from pydub import AudioSegment

TARGET_SAMPLE_RATE = 16000
CHUNK_MINUTES = 5


def normalize_audio(audio: AudioSegment) -> AudioSegment:
    return audio.set_channels(1).set_frame_rate(TARGET_SAMPLE_RATE)


def convert_to_wav(input_path: str) -> str:
    root, _ = os.path.splitext(input_path)
    output_path = root + "_converted.wav"

    audio = AudioSegment.from_file(input_path)
    audio = normalize_audio(audio)
    audio.export(output_path, format="wav")

    return output_path


def chunk_audio(wav_path: str, chunk_minutes: int = CHUNK_MINUTES) -> list:
    audio = AudioSegment.from_wav(wav_path)
    audio = normalize_audio(audio)

    chunk_ms = chunk_minutes * 60 * 1000
    chunks = []

    for i, start in enumerate(range(0, len(audio), chunk_ms)):
        chunk = audio[start:start + chunk_ms]

        if len(chunk) == 0:
            continue

        chunk_path = f"{wav_path}_chunk_{i}.wav"

        chunk.export(chunk_path, format="wav")
        chunks.append(chunk_path)

        print(f"Created chunk {i + 1}: {chunk_path}")

    print(f"\nTotal chunks created: {len(chunks)}")

    return chunks


def process_audio(input_file: str):
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"File not found: {input_file}")

    print("Converting audio to WAV...")

    wav_path = convert_to_wav(input_file)

    print("Splitting audio into chunks...")

    return chunk_audio(wav_path)