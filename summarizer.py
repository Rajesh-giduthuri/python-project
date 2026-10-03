import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_LLM_MODEL = os.getenv(
    "GROQ_LLM_MODEL",
    "openai/gpt-oss-20b"
)

if not GROQ_API_KEY:
    raise RuntimeError("GROQ_API_KEY is not set in .env")

client = Groq(api_key=GROQ_API_KEY)


def generate_summary(transcript: str) -> str:
    """Generate an AI meeting summary using Groq."""

    if not transcript.strip():
        raise ValueError("Transcript is empty.")

    prompt = f"""
You are an AI meeting assistant.

Analyze the following meeting transcript and create a clear,
professional summary.

Include:

1. Meeting Overview
2. Key Discussion Points
3. Important Decisions
4. Action Items

Keep the summary concise but informative.

MEETING TRANSCRIPT:
{transcript}
"""

    print("\nSending transcript to Groq for summarization...")

    response = client.chat.completions.create(
        model=GROQ_LLM_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a professional meeting summarization assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
    )

    summary = response.choices[0].message.content.strip()

    if not summary:
        raise ValueError("Groq returned an empty summary.")

    return summary

#5. Next Steps