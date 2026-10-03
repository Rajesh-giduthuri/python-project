import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from rag.search import search_meetings


# --------------------------------------------------
# LOAD ENVIRONMENT
# --------------------------------------------------

BASE_DIR = Path(
    __file__
).resolve().parent.parent

load_dotenv(
    BASE_DIR / ".env"
)


OPENROUTER_API_KEY = os.getenv(
    "OPENROUTER_API_KEY"
)

MODEL_NAME = os.getenv(
    "OPENROUTER_MODEL",
    "openrouter/free"
)


# --------------------------------------------------
# VALIDATE API KEY
# --------------------------------------------------

if not OPENROUTER_API_KEY:

    raise ValueError(
        "OPENROUTER_API_KEY is not configured."
    )


# --------------------------------------------------
# OPENROUTER CLIENT
# --------------------------------------------------

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY
)


# --------------------------------------------------
# ASK QUESTION
# --------------------------------------------------

def ask_meeting_question(
    question: str,
    top_k: int = 5
):
    """
    Answer a question using relevant
    meeting transcript chunks.
    """

    if not question.strip():

        raise ValueError(
            "Question cannot be empty."
        )


    # ----------------------------------------------
    # RETRIEVE RELEVANT CHUNKS
    # ----------------------------------------------

    results = search_meetings(
        question,
        top_k=top_k
    )


    if not results:

        return (
            "I could not find relevant "
            "information in the meeting."
        )


    # ----------------------------------------------
    # BUILD CONTEXT
    # ----------------------------------------------

    context_parts = []

    for result in results:

        context_parts.append(
            result["document"]
        )


    context = "\n\n".join(
        context_parts
    )


    # ----------------------------------------------
    # CREATE PROMPT
    # ----------------------------------------------

    prompt = f"""
You are an AI meeting assistant.

Answer the user's question using ONLY
the meeting transcript context provided below.

Do not invent information.

If the answer cannot be found in the
provided context, say:

"I could not find this information
in the meeting transcript."

MEETING CONTEXT:
{context}

USER QUESTION:
{question}

Provide a concise and clear answer.
"""


    # ----------------------------------------------
    # CALL OPENROUTER
    # ----------------------------------------------

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


    answer = response.choices[
        0
    ].message.content


    if not answer:

        raise ValueError(
            "OpenRouter returned an empty answer."
        )


    return answer


# --------------------------------------------------
# TEST
# --------------------------------------------------

if __name__ == "__main__":

    question = (
        "What is the project deadline?"
    )


    answer = ask_meeting_question(
        question
    )


    print("\n")
    print("=" * 60)
    print("MEETING Q&A")
    print("=" * 60)

    print(
        f"\nQuestion:\n{question}"
    )

    print(
        f"\nAnswer:\n{answer}"
    )

    print("=" * 60)