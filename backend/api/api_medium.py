from fastapi import APIRouter
from core.web_scraping.medium import MediumScraper

router = APIRouter()

@router.get("/medium_scraper")
def get_medium_articles():
    """Fetches and returns the latest Medium articles based on predefined tags."""
    scraper = MediumScraper()
    articles = scraper.run()
    return {"message": "Medium Articles Retrieved", "data": articles}
