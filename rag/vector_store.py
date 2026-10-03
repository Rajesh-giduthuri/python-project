from pathlib import Path

import chromadb

from config.settings import CHROMA_DIR
from rag.embeddings import create_embeddings


# --------------------------------------------------
# CHROMA DATABASE
# --------------------------------------------------

CHROMA_DIR = Path(CHROMA_DIR)

CHROMA_DIR.mkdir(
    parents=True,
    exist_ok=True
)


client = chromadb.PersistentClient(
    path=str(CHROMA_DIR)
)


# --------------------------------------------------
# COLLECTION
# --------------------------------------------------

collection = client.get_or_create_collection(
    name="meeting_transcripts"
)


# --------------------------------------------------
# ADD MEETING TRANSCRIPT
# --------------------------------------------------

def add_meeting_transcript(
    meeting_id: int,
    transcript: str
):
    """
    Split a meeting transcript into chunks,
    create embeddings, and store them in ChromaDB.
    """

    if not transcript.strip():
        raise ValueError(
            "Transcript is empty."
        )

    # ----------------------------------------------
    # CHUNK TRANSCRIPT
    # ----------------------------------------------

    words = transcript.split()

    chunk_size = 300

    chunks = []

    for i in range(
        0,
        len(words),
        chunk_size
    ):

        chunk = " ".join(
            words[
                i:i + chunk_size
            ]
        )

        if chunk.strip():
            chunks.append(chunk)


    # ----------------------------------------------
    # CREATE IDs
    # ----------------------------------------------

    ids = [
        f"meeting_{meeting_id}_chunk_{i}"
        for i in range(len(chunks))
    ]


    # ----------------------------------------------
    # CREATE EMBEDDINGS
    # ----------------------------------------------

    embeddings = create_embeddings(
        chunks
    )


    # ----------------------------------------------
    # METADATA
    # ----------------------------------------------

    metadatas = [
        {
            "meeting_id": meeting_id,
            "chunk_index": i
        }
        for i in range(len(chunks))
    ]


    # ----------------------------------------------
    # STORE IN CHROMADB
    # ----------------------------------------------

    collection.upsert(
        ids=ids,
        documents=chunks,
        embeddings=embeddings.tolist(),
        metadatas=metadatas
    )


    print(
        f"\nStored {len(chunks)} "
        f"transcript chunks."
    )


# --------------------------------------------------
# TEST
# --------------------------------------------------

if __name__ == "__main__":

    test_transcript = """
    The development team discussed the new project.
    The project deadline is next Friday.
    John will prepare the deployment documentation.
    The team decided to complete testing before deployment.
    """

    add_meeting_transcript(
        meeting_id=999,
        transcript=test_transcript
    )

    print(
        "ChromaDB test completed successfully."
    )