from sentence_transformers import SentenceTransformer
from typing import List

# embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

def generate_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Generates embeddings for a list of texts

    Args:
        texts (List[str]): List of texts to embed

    Returns:
        List[List[float]]: List of embeddings
    """
    return model.encode(texts).tolist()
    # bc Mongo doesn't support numpy types