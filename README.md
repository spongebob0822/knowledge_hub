# Knowledge_Hub

## Overview
`Knowledge_Hub` is a web scraping project designed to crawl and collect news and articles related to Data Science and AI. It fetches relevant content from Google Tech News, Google News Filtering, and Medium, storing the output for further analysis.

## Installation and Setup

### Prerequisites
Ensure you have Python installed on your system. You also need `uvicorn` and FastAPI for running the application.

### Steps to Install
1. Clone the repository:
   ```sh
   git clone https://github.com/your-username/Knowledge_Hub.git
   cd Knowledge_Hub
   ```

2. Install dependencies using `uv` (or `pip` if preferred):
   ```sh
   uv add
   ```

3. Create a `.env` file inside the `backend` folder and add your RapidAPI key:
   ```sh
   RAPIDAPI_KEY=your_rapidapi_key_here
   ```
   You can obtain the API key from the [RapidAPI website](https://rapidapi.com/).

## API Endpoints
The application exposes the following API endpoints via `main.py`:

1. **Google Tech News Scraper**
   - **Endpoint:** `/api/google_tech_news`
   - **Description:** Retrieves all tech-related news from Google Tech News.

2. **Google News Filtering**
   - **Endpoint:** `/api/google_news_filtering`
   - **Description:** Filters Google News articles specifically related to Data Science and AI.

3. **Medium Scraper**
   - **Endpoint:** `/api/medium`
   - **Description:** Scrapes relevant articles from Medium.

## Running the Application
To start the FastAPI application, navigate to the project directory and run:
```sh
uvicorn main:app --reload
```

## Data Storage
The collected data is stored in the following directory:
```
database/data_web_scraping/
```

## Contributing
Feel free to fork the repository and submit pull requests with improvements or new features.

## License
This project is licensed under the MIT License.

