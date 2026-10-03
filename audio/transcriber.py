
import os
import ctypes

CUBLAS_PATH = "/usr/local/lib/python3.13/dist-packages/nvidia/cublas/lib"

if os.path.exists(CUBLAS_PATH):
    os.environ["LD_LIBRARY_PATH"] = (
        CUBLAS_PATH + ":" + os.environ.get("LD_LIBRARY_PATH", "")
    )

    try:
        ctypes.CDLL(
            os.path.join(CUBLAS_PATH, "libcublas.so.12")
        )
    except OSError:
        pass

import av

_original_open = av.open

def _patched_open(*args, **kwargs):
    kwargs.pop("metadata_errors", None)
    return _original_open(*args, **kwargs)

av.open = _patched_open

from faster_whisper import WhisperModel

MODEL_NAME = "small"
DEVICE = "cuda"
COMPUTE_TYPE = "float16"

print("Loading Faster-Whisper...")

model = WhisperModel(
    MODEL_NAME,
    device=DEVICE,
    compute_type=COMPUTE_TYPE
)

print("Faster-Whisper loaded successfully.")


def transcribe_chunk(chunk_path: str, language: str = "english") -> list:
    segments, info = model.transcribe(
        chunk_path,
        language="en" if language.lower() == "english" else None,
        beam_size=5
    )

    results = []

    for segment in segments:
        results.append({
            "start": segment.start,
            "end": segment.end,
            "text": segment.text.strip()
        })

    return results


def transcribe_all(chunks: list, language: str = "english") -> str:
    all_segments = []
    offset = 0.0

    for chunk in chunks:
        print(f"Transcribing: {chunk}")

        segments = transcribe_chunk(
            chunk,
            language
        )

        for segment in segments:
            all_segments.append(
                f"[{segment['start'] + offset:.2f}s - "
                f"{segment['end'] + offset:.2f}s] "
                f"{segment['text']}"
            )

        offset += 5 * 60

    return "\n".join(all_segments)
