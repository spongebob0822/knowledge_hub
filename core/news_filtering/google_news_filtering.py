import pandas as pd
from utils.llm import ChatGPT42API


class GoogleNewsFilter:
    """Class to filter news articles based on relevance to data-related tools and technologies."""

    def __init__(self):
        self.file_path = "database/data_web_scraping/data_google_tech_news.csv"
        self.full_output_path = "database/data_web_scraping/data_google_tech_news.csv"
        self.filtered_output_path = "database/data_web_scraping/data_google.csv"
        self.df = None

    def read_csv(self):
        """Reads CSV file and extracts necessary columns."""
        self.df = pd.read_csv(self.file_path)[['Title', 'Snippet', 'URL', 'Date']]

    @staticmethod
    def generate_prompt(title, snippet):
        """Generates a prompt for the LLM."""
        return (
            f"Title: {title}\n"
            f"Snippet: {snippet}\n\n"
            "Based on the title and snippet above, is this article about a new technology, tool, or framework "
            "that can be applied in the data world? Examples include programming tools, AI/ML models, "
            "data engineering frameworks, or cloud-based solutions. Your response should be either 'Yes' or 'No'."
        )

    @staticmethod
    def process_results(response):
        """Processes the LLM response to return a clear 'Yes' or 'No' output."""
        # Ensure response is a dictionary
        if isinstance(response, dict):
            return response.get("result", "No")  # Default to "No" if key is missing
        return "No"  # Default case if response is not a dictionary

    def filter_news(self):
        """Filters news articles using LLM."""
        self.read_csv()
        chatgpt = ChatGPT42API()
        
        pure_results = []
        processed_results = []
        
        for _, row in self.df.iterrows():
            prompt = self.generate_prompt(row['Title'], row['Snippet'])
            response = chatgpt.send_message(prompt)
            pure_llm_result = response
            llm_result = self.process_results(response)
            
            pure_results.append(pure_llm_result)
            processed_results.append(llm_result)
        
        self.df['pure_llm_result'] = pure_results
        self.df['llm_result'] = processed_results

    def save_to_csv(self):
        """Saves results to CSV files."""
        self.df.to_csv(self.full_output_path, index=False)

        filtered_df = self.df[self.df['llm_result'] == "Yes"]
        filtered_df[['Title', 'Snippet', 'URL', 'Date']].to_csv(self.filtered_output_path, index=False)

        return self.full_output_path, self.filtered_output_path

    def run(self):
        """Executes the filtering process."""
        self.filter_news()
        return self.save_to_csv()


if __name__ == "__main__":
    news_filter = GoogleNewsFilter()
    news_filter.run()
