from typing import List
from transformers import pipeline

# summarization model
# happens when the service starts and not per request
summarizer = pipeline(
    "summarization",
    model="facebook/bart-large-cnn"
)

def generate_insight(articles: List[dict]) -> str:
    """
    Generates insight from a list of articles
    
    Args:
        articles (List[dict]): Articles from MongoDB
    
    Returns:
        str: AI-generated summary
    """

    # Combine article contents to create context for the model
    combined_articles = " ".join(
        article["content"] for article in articles
        if "content" in article
    )

    if len(combined_articles) > 2000:
        combined_articles = combined_articles[:2000]

    # Generate summary using the pre-trained model
    summary = summarizer(
        combined_articles,
        max_length=130,
        min_length=40,
        do_sample=False
    )

    # extract + return generated text
    return summary[0]["summary_text"]
