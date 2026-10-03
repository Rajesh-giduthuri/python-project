
from ai.llm import generate_text
from rag.search import search_meetings


def answer_question(question: str, top_k: int = 5) -> str:

    if not question.strip():
        return "Please enter a question."

    results = search_meetings(
        question,
        top_k=top_k
    )

    if not results:
        return "No relevant information was found in the meeting transcript."

    context = "\n\n".join(
        result["document"]
        for result in results
    )

    messages = [
        {
            "role": "system",
            "content": (
                "You are a meeting question-answering assistant. "
                "Answer ONLY from the provided meeting context. "
                "Do not invent information. "
                "If the answer is not present, say that it was not "
                "mentioned in the meeting."
            )
        },
        {
            "role": "user",
            "content": f"""
Answer the question using ONLY the meeting context.

Question:
{question}

Meeting context:
{context}
"""
        }
    ]

    return generate_text(
        messages,
        max_new_tokens=200
    )
