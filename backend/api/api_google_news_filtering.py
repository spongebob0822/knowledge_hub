from fastapi import APIRouter
import pandas as pd
from core.news_filtering.google_news_filtering import GoogleNewsFilter

router = APIRouter()

@router.post("/filter-google-news")
def filter_google_news():
    """Runs the Google News filtering process and returns the filtered articles."""
    news_filter = GoogleNewsFilter()
    _, filtered_output_path = news_filter.run()

    # Read the filtered CSV
    try:
        df = pd.read_csv(filtered_output_path)
        articles = df.to_dict(orient="records")  # Convert to list of dictionaries

        return {
            "message": "Google News filtering completed.",
            "filtered_articles": articles
        }

    except Exception as e:
        return {
            "message": "Error reading filtered news data.",
            "error": str(e)
        }
