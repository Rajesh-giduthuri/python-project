from rag.embeddings import create_embeddings
from rag.vector_store import collection


# --------------------------------------------------
# SEARCH MEETING TRANSCRIPTS
# --------------------------------------------------

def search_meetings(
    query: str,
    top_k: int = 5
):
    """
    Search meeting transcripts using
    semantic similarity.
    """

    if not query.strip():

        raise ValueError(
            "Search query cannot be empty."
        )


    # ----------------------------------------------
    # CREATE QUERY EMBEDDING
    # ----------------------------------------------

    query_embedding = create_embeddings(
        [query]
    )


    # ----------------------------------------------
    # SEARCH CHROMADB
    # ----------------------------------------------

    results = collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=top_k
    )


    # ----------------------------------------------
    # RETURN RESULTS
    # ----------------------------------------------

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


    search_results = []


    for document, metadata, distance in zip(
        documents,
        metadatas,
        distances
    ):

        search_results.append(
            {
                "document": document,
                "meeting_id": metadata.get(
                    "meeting_id"
                ),
                "chunk_index": metadata.get(
                    "chunk_index"
                ),
                "distance": distance
            }
        )


    return search_results


# --------------------------------------------------
# TEST
# --------------------------------------------------

if __name__ == "__main__":

    query = (
        "What is the project deadline?"
    )


    results = search_meetings(
        query,
        top_k=3
    )


    print("\n")
    print("=" * 60)
    print("SEARCH RESULTS")
    print("=" * 60)


    for result in results:

        print(
            f"\nMeeting ID: "
            f"{result['meeting_id']}"
        )

        print(
            f"Chunk: "
            f"{result['chunk_index']}"
        )

        print(
            f"Distance: "
            f"{result['distance']:.4f}"
        )

        print(
            f"Content:\n"
            f"{result['document']}"
        )


    print("=" * 60)