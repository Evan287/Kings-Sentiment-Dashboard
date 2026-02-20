🔦 Sacramento Kings Fan Sentiment Dashboard
An AI-powered dashboard that analyzes real-time social media sentiment from the Sacramento Kings fan base. This project bridges the gap between Natural Language Processing (NLP) and Sports Analytics to visualize how the "Beam" affects fan engagement.

🚀 Key Features
Live Data Pipeline: Automated cloud scraping using Apify to ingest real-time fan discussions.

Advanced NLP: Implements the cardiffnlp/twitter-roberta-base-sentiment-latest model to categorize sentiment into Positive, Neutral, and Negative.

Dynamic Visualizations: Interactive Pie and Line charts built with Plotly to track sentiment trends over time.

"Beam Mode" Filter: A custom toggle to isolate sentiment on victory days (Light the Beam!).

Automated Categorization: Smart keyword mapping for player performance (Sabonis, DeRozan, LaVine), stadium food, and arena atmosphere.

🛠️ Tech Stack
Language: Python 3.10+

Framework: Streamlit (Web UI)

AI/ML: Hugging Face Transformers (RoBERTa Model)

Data Orchestration: Apify (Twitter/X Scraper Actor)

Visuals: Plotly Express & Pandas
# Kings-Sentiment-Dashboard
