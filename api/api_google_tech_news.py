from fastapi import APIRouter, HTTPException
from core.web_scraping.google_tech_news import GoogleNewsScraper

router = APIRouter()

@router.get("/google_tech_news")
async def get_google_tech_news():
    """Fetch Google Tech News using `run()`, save it to CSV, and return response."""
    scraper = GoogleNewsScraper()
    news_items = scraper.run() 

    if not news_items:
        raise HTTPException(status_code=404, detail="No news found or API error.")

    # Extract required fields for response
    extracted_data = [
        {
            "Title": item.get("title", "N/A"),
            "Snippet": item.get("snippet", "N/A"),
            "URL": item.get("newsUrl", "N/A"),
            "Date": scraper.convert_timestamp(item.get("timestamp"))
        }
        for item in news_items
    ]

    return {"status": "success", "news": extracted_data}