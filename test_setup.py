import streamlit as st
from transformers import pipeline

#Test 1: Checl if AI model loads
print("Loading Sentiment Model...")
analyzer = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment-latest")
result = analyzer("The Kinds lit the beam tonight! What a game.")[0]

# Test 2: Basic Streamlit UI
st.title("Kings Dashboard Test")
st.write(f"Sentiment Test: {result['label']} (Score: {round(result['score'], 2)})")
st.success("Setup complete! Everything is working.")