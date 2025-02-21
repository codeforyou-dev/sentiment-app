import streamlit as st
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
nltk.download('vader_lexicon')

sid = SentimentIntensityAnalyzer()

def get_sentiment(text):
    scores = sid.polarity_scores(text)
    compound = scores['compound']
    if compound >= 0.05:
        return "Positive"
    elif compound <= -0.05:
        return "Negative"
    else:
        return "Neutral"

st.title("Sentiment Analysis App")
st.write("Enter a comment below to see its sentiment!")

# Session state for history
if 'history' not in st.session_state:
    st.session_state.history = []

comment = st.text_input("Your Comment:")
if comment.strip():
    sentiment = get_sentiment(comment)
    scores = sid.polarity_scores(comment)
    
    # Color-coded sentiment
    if sentiment == "Positive":
        st.markdown(f"**Sentiment:** <span style='color:green'>{sentiment}</span>", unsafe_allow_html=True)
    elif sentiment == "Negative":
        st.markdown(f"**Sentiment:** <span style='color:red'>{sentiment}</span>", unsafe_allow_html=True)
    else:
        st.markdown(f"**Sentiment:** <span style='color:gray'>{sentiment}</span>", unsafe_allow_html=True)
    
    st.write(f"**Details:** {scores}")
    
    # Add to history
    st.session_state.history.append((comment, sentiment))
else:
    st.write("Please enter a comment to analyze.")

# Show history
if st.session_state.history:
    st.subheader("Comment History")
    for i, (past_comment, past_sentiment) in enumerate(st.session_state.history):
        st.write(f"{i+1}. '{past_comment}' - {past_sentiment}")