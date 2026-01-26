from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import industries_collection, articles_collection
from embeddings import generate_embeddings
from ai_service import generate_insight
import numpy as np

app = FastAPI(title="Industry Insight Explorer API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your Vercel domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.post("/industries/{industry_slug}/insight")
def create_insight(industry_slug: str):
    articles = list(
        articles_collection.find(
            {"industry": industry_slug},
            {"_id": 0}
        )
    )

    content = generate_insight(articles)

    return {
        "industry": industry_slug,
        "content": content,
    }