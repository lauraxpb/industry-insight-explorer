from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import industries_collection, articles_collection
from embeddings import generate_embeddings
from ai_service import generate_insight

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
def search_industries_semantically(query: str, limit: int = 5):
    query_embedding = generate_embeddings([query])[0]
    try:
        pipeline = [
            {
                "$vectorSearch": {
                    "index": "vector_index",  # Name of your Atlas Vector Search index
                    "path": "embedding",
                    "queryVector": query_embedding,
                    "numCandidates": limit * 10,  # Number of candidates to consider
                    "limit": limit,
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "name": 1,
                    "slug": 1,
                    "description": 1,
                    "score": {"$meta": "vectorSearchScore"},
                }
            },
        ]
        
        results = list(industries_collection.aggregate(pipeline))
        return results
        
    except Exception as e:
        print(f"Vector search failed: {e}. Falling back to text search.")
        query_lower = query.lower()
        results = list(
            industries_collection.find(
                {
                    "$or": [
                        {"name": {"$regex": query_lower, "$options": "i"}},
                        {"slug": {"$regex": query_lower, "$options": "i"}},
                        {"description": {"$regex": query_lower, "$options": "i"}},
                    ]
                },
                {"_id": 0, "name": 1, "slug": 1, "description": 1},
            ).limit(limit)
        )
        return results

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