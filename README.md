🔦 Sacramento Kings Fan Sentiment Dashboard
An AI-powered dashboard that analyzes real-time social media sentiment from the Sacramento Kings fan base. This project bridges the gap between Natural Language Processing (NLP) and Sports Analytics to visualize how the "Beam" affects fan engagement.
-----------------------------------------------------------------------
🚀 Key Features
Live Data Pipeline: Automated cloud scraping using Apify to ingest real-time fan discussions.

Advanced NLP: Implements the cardiffnlp/twitter-roberta-base-sentiment-latest model to categorize sentiment into Positive, Neutral, and Negative.

Dynamic Visualizations: Interactive Pie and Line charts built with Plotly to track sentiment trends over time.

"Beam Mode" Filter: A custom toggle to isolate sentiment on victory days (Light the Beam!).

Automated Categorization: Smart keyword mapping for player performance (Sabonis, DeRozan, LaVine), stadium food, and arena atmosphere.


🛠️ Tech Stack
-----------------------------------------------------------------------
Language: Python 3.10+

Framework: Streamlit (Web UI)

AI/ML: Hugging Face Transformers (RoBERTa Model)

Data Orchestration: Apify (Twitter/X Scraper Actor)

Visuals: Plotly Express & Pandas

📦 Installation & Setup
-----------------------------------------------------------------------
Clone the repo:
git clone https://github.com/YOUR_USERNAME/kings-sentiment-analysis.git
cd kings-sentiment-analysis

Install dependencies:
pip install streamlit pandas plotly transformers torch apify-client

API Configuration:
Create a secrets.toml file in a .streamlit folder or replace the ApifyClient token in app.py with your personal key.

Run the app:
streamlit run app.py

📊 Data Insights
-----------------------------------------------------------------------
Sentiment Drift: The dashboard tracks how specific roster moves (like the 2026 trade deadline) impact fan optimism.
Performance Metrics: Analyzes which players drive the most positive engagement vs. who receives the most "Performance" based criticism.

🔒 Safety & Privacy
-----------------------------------------------------------------------
This tool adheres to Reddit and X/Twitter's developer policies by utilizing official API endpoints via Apify. All data is anonymized and used strictly for sentiment analysis purposes.

💡 Why this belongs in a Portfolio
-----------------------------------------------------------------------
This project demonstrates the ability to handle unstructured data, manage API integrations, and deploy a Machine Learning model into a production-ready web interface. It solves the real-world problem of monitoring brand health in the sports industry.

👑 Credits
-----------------------------------------------------------------------
Data provided by the Sacramento Kings fan community.

Model by Cardiff NLP.

Built with 💜 in Sacramento.
