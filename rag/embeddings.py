from sentence_transformers import SentenceTransformer


# --------------------------------------------------
# EMBEDDING MODEL
# --------------------------------------------------

MODEL_NAME = "all-MiniLM-L6-v2"


print(
    "Loading embedding model..."
)


model = SentenceTransformer(
    MODEL_NAME
)


print(
    "Embedding model loaded."
)


# --------------------------------------------------
# CREATE EMBEDDINGS
# --------------------------------------------------

def create_embeddings(
    texts: list[str]
):
    """
    Convert a list of text strings into
    numerical embeddings.
    """

    if not texts:

        return []


    embeddings = model.encode(
        texts,
        convert_to_numpy=True
    )


    return embeddings