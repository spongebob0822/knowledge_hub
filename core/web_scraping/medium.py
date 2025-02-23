import os
import csv
import logging
import requests
from bs4 import BeautifulSoup
from datetime import datetime


class MediumScraper:
    """Scrapes article titles and dates from Medium for given tags."""

    BASE_URL = "https://medium.com"
    CSV_PATH = "database/data_web_scraping/data_medium.csv"
    TAGS = ["AI", "Machine Learning", "Programming", "Data Science"]

    def __init__(self):
        """Initializes the scraper."""
        self.today_date = datetime.today().strftime("%Y-%m-%d")

        # Configure logging
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    def fetch_page(self, tag: str) -> str:
        """Fetches the HTML content of the Medium tag page."""
        url = f"{self.BASE_URL}/tag/{tag.replace(' ', '-').lower()}"
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            )
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise error for bad responses
        return response.text

    def parse_articles(self, html: str, tag: str) -> list:
        """Parses Medium articles from HTML and extracts title and date."""
        soup = BeautifulSoup(html, "html.parser")
        articles = soup.find_all("article")[:10]  # Limit to 10 articles per tag

        extracted_data = []
        for article in articles:
            title_tag = article.find("h2")
            title = title_tag.text.strip() if title_tag else "No Title"

            extracted_data.append({"title": title, "date": self.today_date, "category": tag})

        return extracted_data

    def remove_duplicates(self, articles: list) -> list:
        """Removes duplicate articles based on title."""
        unique_articles = {article["title"]: article for article in articles}.values()
        return list(unique_articles)

    def save_to_csv(self, all_articles: list) -> None:
        """Saves extracted articles to a CSV file."""
        os.makedirs(os.path.dirname(self.CSV_PATH), exist_ok=True)
        file_exists = os.path.isfile(self.CSV_PATH)

        try:
            with open(self.CSV_PATH, mode="a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                if not file_exists:
                    writer.writerow(["Title", "Date", "Category"])  # Header

                for item in all_articles:
                    writer.writerow([item["title"], item["date"], item["category"]])

            logging.info(f"Data saved successfully at {self.CSV_PATH}")

        except Exception as e:
            logging.error(f"Error writing to CSV: {e}")

    def run(self) -> dict:
        """Fetches articles for multiple tags, removes duplicates, saves them to CSV, and returns results."""
        all_articles = []

        for tag in self.TAGS:
            try:
                html = self.fetch_page(tag)
                articles = self.parse_articles(html, tag)
                all_articles.extend(articles)

            except Exception as e:
                logging.error(f"Error fetching articles for {tag}: {e}")

        # Remove duplicates before saving
        unique_articles = self.remove_duplicates(all_articles)
        self.save_to_csv(unique_articles)

        return {tag: [a for a in unique_articles if a["category"] == tag] for tag in self.TAGS}
