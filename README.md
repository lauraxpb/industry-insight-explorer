# Industry Insight Explorer

An intelligent web application that delivers AI-powered industry insights, trends, and article summaries to help businesses make informed decisions faster.

## What it does

Industry Insight Explorer allows a user to:

1. Ask a question or type a topic
2. The system detects the most relevant industry using semantic search (embeddings)
3. The user can generate an AI-powered insight based on real industry articles stored in MongoDB

## The Problem

Companies struggle to:

- Understand trends across different industries
- Process large volumes of scattered information quickly
- Identify patterns and extract actionable insights

## The Solution

Industry Insight Explorer centralizes industry-specific content and uses AI to:

- Summarize articles and news automatically
- Extract key insights and trends
- Enable rapid exploration of industry developments

## Key Features

### Semantic Industry Detection
The system uses embeddings to map both:
- the user query
- industry descriptions

into vector space and computes similarity to detect the best matching industry.

### AI Insight Generation
After selecting an industry, the app generates a concise AI insight based on the stored articles for that industry.

### MongoDB-backed Data
The app stores:
- industry metadata (name, slug, description, embeddings)
- article data (title, summary, industry, etc.)

This proves that MongoDB allows flexible schemas and fast retrieval.

## How It Works

1. **Select an industry** (finance, retail, media, etc.)
2. **Backend queries** MongoDB for relevant articles
3. **AI generates** summaries and insights
4. **Results displayed** in an intuitive UI

## Getting Started

### 1. Clone the repo

```bash
git clone <repo-url>
cd industry-insight-explorer
```

### 2. Backend Setup

Create a .env file inside backend/ with:

MONGODB_URI=<your mongodb connection string>
DB_NAME=industry_insights
OPENAI_API_KEY=<your openai key>


#### Install dependencies:

cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt


#### Run the server:

uvicorn main:app --reload

### 3. Seed industry embeddings (one-time)
python seed_industries_embeddings.py

### 4. Frontend Setup
cd ../frontend
npm install
npm run dev