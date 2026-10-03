import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from ai.prompts import MEETING_ANALYSIS_PROMPT


# --------------------------------------------------
# LOAD ENVIRONMENT VARIABLES
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


OPENROUTER_API_KEY = os.getenv(
    "OPENROUTER_API_KEY"
)


# --------------------------------------------------
# VALIDATE API KEY
# --------------------------------------------------

if not OPENROUTER_API_KEY:

    raise ValueError(
        "OPENROUTER_API_KEY is not configured "
        "in the .env file."
    )


# --------------------------------------------------
# OPENROUTER CLIENT
# --------------------------------------------------

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY
)


# --------------------------------------------------
# MODEL
# --------------------------------------------------

MODEL_NAME = os.getenv(
    "OPENROUTER_MODEL",
    "openai/gpt-4o-mini"
)


# --------------------------------------------------
# ANALYZE MEETING
# --------------------------------------------------

def analyze_meeting(transcript: str) -> str:
    """
    Send the meeting transcript to OpenRouter
    and return the AI-generated analysis.
    """

    if not transcript.strip():

        raise ValueError(
            "Transcript is empty."
        )


    prompt = MEETING_ANALYSIS_PROMPT.format(
        transcript=transcript
    )


    print(
        "\nSending transcript to OpenRouter..."
    )


    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )


    result = response.choices[0].message.content


    if not result:

        raise ValueError(
            "OpenRouter returned an empty response."
        )


    return result


# --------------------------------------------------
# READ TRANSCRIPT FILE
# --------------------------------------------------

def read_transcript(
    transcript_path: str | Path
) -> str:

    transcript_path = Path(
        transcript_path
    )


    if not transcript_path.exists():

        raise FileNotFoundError(
            f"Transcript not found: "
            f"{transcript_path}"
        )


    with open(
        transcript_path,
        "r",
        encoding="utf-8"
    ) as file:

        return file.read()


# --------------------------------------------------
# SAVE ANALYSIS
# --------------------------------------------------

def save_analysis(
    analysis: str,
    output_path: str | Path
):

    output_path = Path(
        output_path
    )


    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )


    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(analysis)


    print(
        f"\nAnalysis saved to:"
        f"\n{output_path}"
    )


# --------------------------------------------------
# TEST
# --------------------------------------------------

if __name__ == "__main__":

    transcript_file = (
        BASE_DIR
        / "outputs"
        / "transcript.txt"
    )


    analysis_file = (
        BASE_DIR
        / "outputs"
        / "meeting_analysis.txt"
    )


    transcript = read_transcript(
        transcript_file
    )


    analysis = analyze_meeting(
        transcript
    )


    print("\n")
    print("=" * 60)
    print("MEETING ANALYSIS")
    print("=" * 60)
    print(analysis)
    print("=" * 60)


    save_analysis(
        analysis,
        analysis_file
    )