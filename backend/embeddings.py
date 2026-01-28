from sentence_transformers import SentenceTransformer
from typing import List

# embedding model - lazy load
_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer('all-MiniLM-L6-v2')
    return _model

def generate_embeddings(texts: List[str]) -> List[List[float]]:
    """
    Generates embeddings for a list of texts

    Args:
        texts (List[str]): List of texts to embed

    Returns:
        List[List[float]]: List of embeddings
    """
    model = get_model()
    return model.encode(texts).tolist()
    # bc Mongo doesn't support numpy types