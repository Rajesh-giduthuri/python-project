
import json
import re
from ai.llm import generate_text


def extract_meeting_data(transcript: str) -> dict:

    prompt = f"""
Extract meeting information from the transcript.

Return ONLY valid JSON using exactly this structure:

{{
  "meeting_overview": "",
  "key_discussion_points": [],
  "decisions": [],
  "action_items": [],
  "next_steps": []
}}

Rules:
- Use only information explicitly stated.
- Keep items short.
- Do not invent information.
- Every list item must be a string.
- Return JSON only.
- No markdown.

TRANSCRIPT:

{transcript}
"""

    messages = [
        {
            "role": "system",
            "content": "You extract factual meeting information and return valid JSON only."
        },
        {
            "role": "user",
            "content": prompt
        }
    ]

    result = generate_text(
        messages,
        max_new_tokens=500
    )

    result = re.sub(r"```json", "", result, flags=re.IGNORECASE)
    result = re.sub(r"```", "", result).strip()

    start = result.find("{")
    end = result.rfind("}")

    if start == -1 or end == -1:
        return {
            "meeting_overview": "",
            "key_discussion_points": [],
            "decisions": [],
            "action_items": [],
            "next_steps": []
        }

    try:
        data = json.loads(result[start:end + 1])
    except json.JSONDecodeError:
        return {
            "meeting_overview": "",
            "key_discussion_points": [],
            "decisions": [],
            "action_items": [],
            "next_steps": []
        }

    return {
        "meeting_overview": data.get("meeting_overview", ""),
        "key_discussion_points": data.get("key_discussion_points", []),
        "decisions": data.get("decisions", []),
        "action_items": data.get("action_items", []),
        "next_steps": data.get("next_steps", [])
    }
