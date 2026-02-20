import streamlit as st
import pandas as pd
import plotly.express as px
from transformers import pipeline
from apify_client import ApifyClient
import datetime
import os

# -- PAGE CONFIG -- 
st.set_page_config(page_title="Kings Fan Sentiment", page_icon="🔦", layout="wide")

# -- LOAD AI MODEL --
@st.cache_resource 
def load_model():
    return pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment-latest")

analyzer = load_model()

# -- DATA LOADING LOGIC --
@st.cache_data
def load_all_data():
    try:
        # Load from the local CSV that Apify updates
        df = pd.read_csv("kings_data.csv")
        
        # Standardize Apify's column names
        if 'fullText' in df.columns:
            df = df.rename(columns={'fullText': 'text'})
        
        df = df.dropna(subset=['text'])
        df['text'] = df['text'].astype(str)
        
        # Ensure date column exists and is formatted
        if 'date' not in df.columns:
            df['date'] = pd.Timestamp.now().strftime('%Y-%m-%d')
        
        # Win-Day detection for the 'Beam Mode' toggle
        if 'is_win_day' not in df.columns:
            df['is_win_day'] = df['text'].str.contains('beam|win|victory', case=False)
        
        return df
    except:
        # Fallback Mock Data if CSV is missing
        mock_data = {
            'text': ["Light the beam!", "Malik Monk is unstoppable!", "The hot dogs were cold.", "Long lines for beer."],
            'is_win_day': [True, True, False, False],
            'date': [str(datetime.date.today())] * 4
        }
        return pd.DataFrame(mock_data)

# -- CLOUD SCRAPER FUNCTION --
def fetch_live_data():
    with st.spinner("Connecting to Apify Cloud..."):
        # Clear specific cache so app reads the new CSV
        load_all_data.clear()
        
        # Use secret token for security
        client = ApifyClient(st.secrets["APIFY_TOKEN"])
        
        run_input = {
            "searchTerms": ["#LightTheBeam", "Sacramento Kings"],
            "maxItems": 50,
            "sort": "Latest",
        }
        
        run = client.actor("apidojo/tweet-scraper").call(run_input=run_input)
        items = list(client.dataset(run["defaultDatasetId"]).iterate_items())
        
        live_df = pd.DataFrame(items)
        live_df.to_csv("kings_data.csv", index=False)
        
        return live_df

# -- DATA PROCESSING --
df = load_all_data()

def get_category(text):
    val = str(text).lower()
    if any(word in val for word in ["food", "hot dog", "beer", "lines"]): return "Food"
    if any(word in val for word in ["sabonis", "monk", "derozan", "lavine", "points"]): return "Performance"
    return "Atmosphere"

def get_sentiment(text):
    # RoBERTa returns 'positive', 'neutral', or 'negative'
    return analyzer(text)[0]['label']

# Apply AI to the dataframe
df['Category'] = df['text'].apply(get_category)
df['Sentiment'] = df['text'].apply(get_sentiment)

# -- SIDEBAR & HEADER --
st.title("🔦 Sacramento Kings Fan Engagement")

with st.sidebar:
    st.header("Control Center")
    if st.button("🔄 Sync Live Data"):
        fetch_live_data()
        st.session_state['last_sync'] = datetime.datetime.now().strftime("%H:%M:%S")
        st.rerun()
    
    if 'last_sync' in st.session_state:
        st.caption(f"Last synced: {st.session_state['last_sync']}")

    st.divider()
    beam_mode = st.toggle("🟣 Activate 'Beam Mode' (Wins Only)")

# Filter data for Beam Mode
display_df = df[df['is_win_day'] == True] if beam_mode else df

# -- DASHBOARD VISUALS --
col1, col2 = st.columns(2)

with col1:
    fig_pie = px.pie(display_df, names='Sentiment', color='Sentiment',
                 color_discrete_map={'positive': '#5a2d81', 'neutral':'#63666a', 'negative':'#000000'},
                 title="Current Fan Sentiment")
    st.plotly_chart(fig_pie)

with col2:
    st.write("### Category Analysis")
    category_summary = display_df.groupby('Category')['Sentiment'].value_counts().unstack().fillna(0)
    st.bar_chart(category_summary)

# -- TREND CHART --
st.subheader("📈 Sentiment Trends Over Time")
df['date'] = pd.to_datetime(df['date'])
trend_df = df.groupby([df['date'].dt.date, 'Sentiment']).size().reset_index(name='count')

fig_line = px.line(trend_df, x='date', y='count', color='Sentiment', markers=True,
                  color_discrete_map={'positive': '#5a2d81', 'neutral':'#63666a', 'negative':'#000000'},
                  template="plotly_white")
st.plotly_chart(fig_line, use_container_width=True)

# --- RAW DATA EXPLORER ---
st.divider()
st.subheader("💬 Recent Fan Voices")

# 1. Create the filter
selected = st.multiselect("Filter Sentiment:", ["positive", "neutral", "negative"], default=["positive", "negative"])

# 2. CREATE THE VARIABLE (This is the line that's missing or broken)
voice_df = display_df[display_df['Sentiment'].isin(selected)]

# 3. Use the variable
st.dataframe(
    voice_df[['date', 'Sentiment', 'text']].sort_values(by='date', ascending=False), 
    use_container_width=True, 
    hide_index=True,
    row_height=100,
    column_config={
        "text": st.column_config.TextColumn("Tweet Content", width="large")
    }
)