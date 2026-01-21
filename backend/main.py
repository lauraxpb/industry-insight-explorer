from torch import cosine_similarity
from fastapi import FastAPI
from database import industries_collection, articles_collection
from embeddings import generate_embeddings
from backend.ai_service import generate_insight
import numpy as np

app = FastAPI(title="Industry Insight Explorer API")

@app.get("/")
def root():
    return {"message": "API running"}

@app.get("/industries")
def get_industries():
    industries = list(industries_collection.find({}, {"_id": 0}))
    return industries

# ! conceptual demo of semantic search
@app.get("/search/industries")
def search_industries_semantically(query: str):
    query_embedding = generate_embeddings([query])[0]

    industries = list(industries_collection.find({}, {"_id": 1, "name": 1, "slug": 1, "embedding": 1}))

    def cosine_sim(a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)) 

    for industry in industries:
        industry_embedding = industry.get("embedding")
        if industry_embedding:
            industry["similarity"] = cosine_sim(np.array(query_embedding), np.array(industry_embedding))
        else:
            industry["similarity"] = -1  # no embedding means lowest similarity

    industries.sort(key=lambda x: x["similarity"], reverse=True)

    # return top 5 results without embeddings
    for industry in industries:
        industry.pop("embedding", None)
        industry.pop("similarity", None)

    return industries[:5]

# filter articles by slug
@app.get("/articles/{industry_slug}")
def get_articles_by_industry(industry_slug: str):
    articles = list(
        articles_collection.find(
            {"industry": industry_slug},
            {"_id": 0}
        )
    )
    if not articles:
        return {"message": "There are no articles"}
    return articles