from transformers import pipeline

insight_summarizer = pipeline(
    "summarization",
    model="facebook/bart-large-cnn"
)

def generate_insight(industry_slug: str, context: str) -> str:
    prompt = f"""
    Industry: {industry_slug}
    Context: {context}
    """
    
    result = insight_summarizer(
        prompt,
        max_length=150,
        min_length=20,
        num_return_sequences=1,
    )

    return result[0]["text"]
