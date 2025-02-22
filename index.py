import streamlit as st
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk
nltk.download('vader_lexicon')
sid = SentimentIntensityAnalyzer()
def get_sentiment(text):
    scores = sid.polarity_scores(text)
    compound = scores['compound']
    return "Positive" if compound >= 0.05 else "Negative" if compound <= -0.05 else "Neutral"

st.title("Sentiment Analysis App")
st.write("Enter a comment below to see its sentiment!")

# Session state for history
if 'history' not in st.session_state:
    st.session_state.history = []
if 'input_text' not in st.session_state:
    st.session_state.input_text = ""
if 'form_key' not in st.session_state:
    st.session_state.form_key = 0

# Form
with st.form(key=f"comment_form_{st.session_state.form_key}"):
    comment = st.text_input("Your Comment:", value=st.session_state.input_text)
    submit = st.form_submit_button("Analyze")

# Process submission
if submit and comment.strip():
    sentiment = get_sentiment(comment)
    scores = sid.polarity_scores(comment)
    if sentiment == "Positive":
        st.markdown(f"**Sentiment:** <span style='color:green'>{sentiment}</span>", unsafe_allow_html=True)
    elif sentiment == "Negative":
        st.markdown(f"**Sentiment:** <span style='color:red'>{sentiment}</span>", unsafe_allow_html=True)
    else:
        st.markdown(f"**Sentiment:** <span style='color:gray'>{sentiment}</span>", unsafe_allow_html=True)
    st.write(f"**Details:** {scores}")
    st.session_state.history.append((comment, sentiment))
    st.session_state.input_text = ""
    st.session_state.form_key += 1  # Reset form
    st.rerun()
elif submit:
    st.write("Please enter a comment.")

# History
if st.session_state.history:
    st.subheader("Comment History")
    for i, (past_comment, past_sentiment) in enumerate(st.session_state.history):
        st.write(f"{i+1}. '{past_comment}' - {past_sentiment}")

#Buttons
if st.session_state.history:
    if st.button("Clear History"):
        st.session_state.history = []
        st.session_state.input_text = ""
        st.session_state.form_key += 1
        st.rerun()
    if st.button("Export History"):
        df = pd.DataFrame(st.session_state.history, columns=["Comment", "Sentiment"])
        csv = df.to_csv(index=False)
        st.download_button("Download CSV", csv, "sentiment_history.csv", "text/csv")