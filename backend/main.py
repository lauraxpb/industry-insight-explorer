from fastapi import FastAPI
from database import industries_collection, articles_collection
from backend.ai_service import generate_insight

app = FastAPI(title="Industry Insight Explorer API")

@app.get("/")
def root():
    return {"message": "API running"}

@app.get("/industries")
def get_industries():
    industries = list(industries_collection.find({}, {"_id": 0}))
    return industries

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