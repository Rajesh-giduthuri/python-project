import os
import json
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


def extract_meeting_data(transcript: str) -> dict:
    """Extract structured meeting information as JSON."""

    if not transcript.strip():
        raise ValueError("Transcript is empty.")

    prompt = f"""
You are an AI meeting intelligence assistant.

Analyze the following meeting transcript and extract the
information into the exact JSON structure below.

Return ONLY valid JSON.
Do not use markdown.
Do not add explanations before or after the JSON.

Required JSON structure:

{{
    "meeting_overview": "Brief overview of the meeting",

    "key_discussion_points": [
        "Discussion point 1",
        "Discussion point 2"
    ],
    "decisions": [
        "Decision 1",
        "Decision 2"
    ],
    "action_items": [
        {{
            "person": "Person name",
            "task": "Task assigned to the person",
            "deadline": "Deadline if mentioned, otherwise Not Specified"
        }}
    ],
    
}}

Important:
- Do not invent information.
- If a person is not explicitly identified, use "Unassigned".
- If a deadline is not mentioned, use null.
- Keep each item concise.
- Preserve important details from the transcript.

MEETING TRANSCRIPT:

{transcript}
"""

    print("\nSending transcript to Groq for structured extraction...")

    response = client.chat.completions.create(
        model=GROQ_LLM_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You extract structured meeting information "
                    "and return valid JSON only."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.1,
    )

    result = response.choices[0].message.content.strip()

    if not result:
        raise ValueError("Groq returned an empty response.")

    try:
        meeting_data = json.loads(result)
    except json.JSONDecodeError as e:
        print("\nGroq returned invalid JSON:")
        print(result)
        raise ValueError(
            f"Failed to parse Groq response as JSON: {e}"
        )

    return meeting_data

# "next_steps": [
#         "Next step 1",
#         "Next step 2"
#  ]