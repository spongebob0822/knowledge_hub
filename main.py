from fastapi import FastAPI
from api.api_google_tech_news import router as google_tech_news_router
from api.api_medium import router as medium_router

app = FastAPI()

# Include Google Tech News API
app.include_router(google_tech_news_router, prefix="/api", tags=["Google Tech News"])

# Include Medium Scraper API
app.include_router(medium_router, prefix="/api", tags=["Medium Scraper"])

@app.get("/")
def home():
    return {"message": "Welcome to the FastAPI Web Scraper!"}
