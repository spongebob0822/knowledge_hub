from fastapi import FastAPI
from api.api_google_tech_news import router as google_tech_news_router

app = FastAPI()

# Include the Google Tech News route
app.include_router(google_tech_news_router, prefix="/api", tags=["Google Tech News"])

@app.get("/")
def home():
    return {"message": "Welcome to the FastAPI Web Scraper!"}
