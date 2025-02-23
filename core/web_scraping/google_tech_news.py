import requests
import csv
import os
import logging
from datetime import datetime
from dotenv import load_dotenv

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class GoogleNewsScraper:
    load_dotenv()  # Load environment variables
    BASE_URL = "https://google-news13.p.rapidapi.com"
    HEADERS = {
        "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY"),
        "X-RapidAPI-Host": "google-news13.p.rapidapi.com"
    }
    CSV_PATH = "database/data_web_scraping/data_google_tech_news.csv"

    def __init__(self, language_region="en-US"):
        self.language_region = language_region
        self.api_key = os.getenv("RAPIDAPI_KEY")

        if not self.api_key:
            logging.error("API Key is missing! Check your .env file.")
            raise ValueError("Missing API Key. Please set RAPIDAPI_KEY in the .env file.")

    def fetch_technology_news(self):
        """Fetches technology news from the API."""
        endpoint = f"{self.BASE_URL}/technology"
        params = {"lr": self.language_region}

        try:
            response = requests.get(endpoint, headers=self.HEADERS, params=params)
            response.raise_for_status()
            data = response.json()

            if "status" in data and data["status"] == "success":
                return data.get("items", [])
            else:
                logging.warning("Unexpected API response format: %s", data)
                return []
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching technology news: {e}")
            return []

    @staticmethod
    def convert_timestamp(epoch_time):
        """Converts Epoch timestamp to 'dd-mm-yyyy' format."""
        try:
            return datetime.utcfromtimestamp(int(epoch_time) / 1000).strftime('%d-%m-%Y')
        except (ValueError, TypeError) as e:
            logging.warning(f"Invalid timestamp {epoch_time}: {e}")
            return "N/A"

    def save_to_csv(self, news_data):
        """Saves the extracted news data to a CSV file."""
        os.makedirs(os.path.dirname(self.CSV_PATH), exist_ok=True)
        file_exists = os.path.isfile(self.CSV_PATH)

        try:
            with open(self.CSV_PATH, mode="a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                if not file_exists:  # Write headers if the file is newly created
                    writer.writerow(["Title", "Snippet", "URL", "Date"])

                for item in news_data:
                    writer.writerow([
                        item.get("title", "N/A"),
                        item.get("snippet", "N/A"),
                        item.get("newsUrl", "N/A"),
                        self.convert_timestamp(item.get("timestamp"))
                    ])

            logging.info(f"Data saved successfully at {self.CSV_PATH}")

        except Exception as e:
            logging.error(f"Error writing to CSV: {e}")

    # def run(self):
    #     """Main execution function."""
    #     news_items = self.fetch_technology_news()

    #     if news_items:
    #         self.save_to_csv(news_items)
    #     else:
    #         logging.info("No data available or API response error.")

    def run(self):
        """Fetches technology news, saves it to CSV, and returns the data."""
        news_items = self.fetch_technology_news()
    
        if news_items:
            self.save_to_csv(news_items)
            return news_items  # ✅ Return the data instead of just saving
        else:
            logging.info("No data available or API response error.")
            return []  # ✅ Always return a list



# Run the script
# if __name__ == "__main__":
#     scraper = GoogleNewsScraper()
#     scraper.run()
