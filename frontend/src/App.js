import React, { useEffect, useState } from "react";

const App = () => {
  const [articles, setArticles] = useState(null); // Start as null
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/api/medium_scraper") // Adjust if needed
      .then((response) => response.json())
      .then((data) => {
        if (data && data.data) {
          setArticles(data.data);
        } else {
          setError("No data received");
        }
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
        setError("Failed to fetch data");
        setLoading(false);
      });
  }, []);

  return (
    <div style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>
      <h2>Medium Articles</h2>
      {loading ? (
        <p>Loading...</p>
      ) : error ? (
        <p style={{ color: "red" }}>{error}</p>
      ) : articles && Object.keys(articles).length > 0 ? (
        Object.keys(articles).map((category) => (
          <div key={category}>
            <h3>{category}</h3>
            <table
              border="1"
              cellPadding="10"
              style={{ width: "100%", borderCollapse: "collapse" }}
            >
              <thead>
                <tr>
                  <th>Title</th>
                  <th>Date</th>
                </tr>
              </thead>
              <tbody>
                {articles[category].map((article, index) => (
                  <tr key={index}>
                    <td>{article.title}</td>
                    <td>{article.date}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ))
      ) : (
        <p>No articles found.</p>
      )}
    </div>
  );
};

export default App;
