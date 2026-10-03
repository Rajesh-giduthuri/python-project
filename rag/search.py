
from pathlib import Path
import chromadb
from sentence_transformers import SentenceTransformer

CHROMA_PATH = "/content/chroma_db"

print("Loading embedding model...")

embedding_model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2",
    device="cuda"
)

print("Embedding model loaded.")

client = chromadb.PersistentClient(path=CHROMA_PATH)

collection = client.get_or_create_collection(
    name="meeting_transcripts",
    metadata={"hnsw:space": "cosine"}
)


def search_meetings(query: str, top_k: int = 5):

    if not query.strip():
        raise ValueError("Search query cannot be empty.")

    count = collection.count()

    if count == 0:

        transcript_path = Path("/content/transcript.txt")

        if not transcript_path.exists():
            return []

        transcript = transcript_path.read_text(
            encoding="utf-8"
        )

        lines = [
            line.strip()
            for line in transcript.splitlines()
            if line.strip()
        ]

        chunks = []
        current = ""

        for line in lines:

            if len(current) + len(line) > 500:

                if current:
                    chunks.append(current)

                current = line

            else:
                current += " " + line

        if current:
            chunks.append(current)

        embeddings = embedding_model.encode(
            chunks,
            convert_to_numpy=True
        )

        collection.add(
            ids=[f"chunk_{i}" for i in range(len(chunks))],
            documents=chunks,
            embeddings=embeddings.tolist()
        )

    query_embedding = embedding_model.encode(
        [query],
        convert_to_numpy=True
    )

    results = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=min(
            top_k,
            collection.count()
        )
    )

    documents = results.get(
        "documents",
        [[]]
    )[0]

    metadatas = results.get(
        "metadatas",
        [[]]
    )[0]

    distances = results.get(
        "distances",
        [[]]
    )[0]

    return [
        {
            "document": document,
            "meeting_id": (
                metadata.get("meeting_id")
                if metadata else None
            ),
            "chunk_index": (
                metadata.get("chunk_index")
                if metadata else None
            ),
            "distance": distance
        }
        for document, metadata, distance
        in zip(
            documents,
            metadatas,
            distances
        )
    ]
