
from pathlib import Path
from ai.llm import generate_text


def analyze_meeting(transcript: str) -> str:

    if not transcript.strip():
        raise ValueError("Transcript is empty.")

    prompt = f"""
You are a factual meeting transcription analyst.

Summarize ONLY information explicitly stated in the transcript.

STRICT RULES:
- Do not invent or infer information.
- Preserve names, numbers, dates, and timing exactly.
- Do not assign responsibility unless explicitly stated.
- Do not add recommendations.
- Do not add actions that were not discussed.

Create exactly these sections:

1. Meeting Overview
2. Key Discussion Points
3. Important Decisions
4. Action Items
5. Next Steps

TRANSCRIPT:

{transcript}
"""

    messages = [
        {
            "role": "system",
            "content": "You are a factual meeting analysis assistant. Never invent information."
        },
        {
            "role": "user",
            "content": prompt
        }
    ]

    print("\nGenerating meeting analysis...")

    return generate_text(
        messages,
        max_new_tokens=600
    )


def read_transcript(transcript_path: str | Path) -> str:

    transcript_path = Path(transcript_path)

    if not transcript_path.exists():
        raise FileNotFoundError(
            f"Transcript not found: {transcript_path}"
        )

    return transcript_path.read_text(encoding="utf-8")


def save_analysis(analysis: str, output_path: str | Path):

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    output_path.write_text(
        analysis,
        encoding="utf-8"
    )

    print(f"\nAnalysis saved to:\n{output_path}")
