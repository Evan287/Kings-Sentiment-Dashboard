import streamlit as st
import pandas as pd
import plotly.express as px
from transformers import pipeline
from apify_client import ApifyClient
import datetime

# -- PAGE CONFIG -- 
st.set_page_config(page_title="Kings Fan Sentiment", page_icon="🔦")

# -- LOAD AI MODEL --
@st.cache_resource 
def load_model():
    return pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment-latest")

analyzer = load_model()

# -- DATA LOADING LOGIC --
@st.cache_data
def load_all_data():
    try:
        # Try loading real data from Apify
        df = pd.read_csv("kings_data.csv")
        if 'fullText' in df.columns:
            df = df.rename(columns={'fullText': 'text'})
        
        df = df.dropna(subset=['text'])
        df['text'] = df['text'].astype(str)
        
        # Ensure we have a date column for the line chart
        if 'date' not in df.columns:
            df['date'] = pd.Timestamp.now().strftime('%Y-%m-%d')
            
        if 'is_win_day' not in df.columns:
            df['is_win_day'] = df['text'].str.contains('beam|win|victory', case=False)
        
        st.sidebar.success("✅ Loaded Real Fan Data")
        return df
    except:
        # Fallback to Mock Data if CSV is missing
        st.sidebar.warning("⚠️ CSV not found. Using Mock Data.")
        mock_data = {
            'text': ["The hot dogs were cold.", "Malik Monk is unstoppable!", "Light the beam!", "Long lines for beer.", "Sabonis double-double!", "Electric energy tonight!"],
            'is_win_day': [False, True, True, False, True, True],
            'date': ["2026-02-15", "2026-02-16", "2026-02-17", "2026-02-15", "2026-02-16", "2026-02-17"]
        }
        return pd.DataFrame(mock_data)

df = load_all_data()

# -- CATEGORIZATION & SENTIMENT --
def get_category(input_text):
    val = str(input_text).lower()
    if any(word in val for word in ["food", "hot dog", "beer", "lines"]): return "Food"
    if any(word in val for word in ["sabonis", "defense", "points", "monk", "demar", "keegan","lavine","derovan","westbrook"]): return "Performance"
    return "Atmosphere"

def get_sentiment(text):
    result = analyzer(text)[0]
    return result['label']

# Apply logic to the loaded dataframe
df['Category'] = df['text'].apply(get_category)
df['Sentiment'] = df['text'].apply(get_sentiment)

# -- DASHBOARD UI --
st.title("🔦 Sacramento Kings Fan Engagement")

beam_mode = st.toggle("Activate 'Light The Beam' Mode (Win Days Only)")

if beam_mode:
    display_df = df[df['is_win_day'] == True]
    st.subheader("💜 Victory Sentiment (Post-Win)")
else:
    display_df = df
    st.subheader("All Fan Mentions")

# --- VISUALIZATIONS ---

# 1. Pie Chart
fig = px.pie(display_df, names='Sentiment', color='Sentiment',
             color_discrete_map={'positive': '#5a2d81', 'neutral':'#63666a', 'negative':'#000000'},
             title=f"Sentiment Distribution: {len(display_df)} Posts")
st.plotly_chart(fig)

# 2. Category Breakdown
st.write('### Category Breakdown')
st.table(display_df.groupby('Category')['Sentiment'].value_counts())

# 3. Sentiment Over Time
st.subheader("📈 Sentiment Trends Over Time")
df['date'] = pd.to_datetime(df['date'])
trend_df = df.groupby([df['date'].dt.date, 'Sentiment']).size().reset_index(name='count')

fig_line = px.line(
    trend_df, x='date', y='count', color='Sentiment', markers=True,
    color_discrete_map={'positive': '#5a2d81', 'neutral':'#63666a', 'negative':'#000000'},
    template="plotly_white"
)
st.plotly_chart(fig_line, use_container_width=True)

# --- RAW DATA EXPLORER ---
st.divider()
st.subheader("🔦 Recent Fan Voices")

# Create a filter in the sidebar or right above the table
selected_sentiments = st.multiselect(
    "Filter by Sentiment:", 
    options=["positive", "neutral", "negative"], 
    default=["positive", "neutral", "negative"]
)

# Apply the filter to our display dataframe
filtered_voice_df = display_df[display_df['Sentiment'].isin(selected_sentiments)]

# Show the top 10 most recent posts
# We use st.dataframe for an interactive, scrollable table
st.dataframe(
    filtered_voice_df[['date', 'Sentiment', 'Category', 'text']].sort_values(by='date', ascending=False).head(15),
    use_container_width=True,
    hide_index=True
)

st.caption(f"Showing {len(filtered_voice_df.head(15))} posts matching your filters.")\

# -- APIFY Automatic Update --
#1 Initialize the client
apify_client = ApifyClient(st.secrets["APIFY_TOKEN"])

def fetch_live_data():
    with st.spinner("Fetching fresh data from the cloud..."):
        # 1. Clear the cache so Streamlit 'forgets' the old CSV
        st.cache_data.clear() 
        
        # 2. Run the Apify scraper
        run_input = {
            "searchTerms": ["#LightTheBeam", "Sacramento Kings"],
            "maxItems": 50,
            "sort": "Latest",
        }
        run = apify_client.actor("apidojo/tweet-scraper").call(run_input=run_input)
        
        # 3. Get results and convert to DataFrame
        items = list(apify_client.dataset(run["defaultDatasetId"]).iterate_items())
        live_df = pd.DataFrame(items)

        # 4. Standardize text column name (Apify often uses 'fullText')
        if 'fullText' in live_df.columns:
            live_df = live_df.rename(columns={'fullText': 'text'})
        
        # 5. Save locally
        live_df.to_csv("kings_data.csv", index=False)
        
        return live_df

# -- SIDEBAR CONTROLS --
with st.sidebar:
    st.header("Settings")
    if st.button("🔄 Sync Live Data"):
        fetch_live_data()
        # Record the current time
        st.session_state['last_update'] = datetime.datetime.now().strftime("%H:%M:%S")
        st.success("Data Updated!")
        st.rerun() 

    if 'last_update' in st.session_state:
        st.caption(f"Last synced at: {st.session_state['last_update']}")