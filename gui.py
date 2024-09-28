# GUI.py
import os
import streamlit as st
import requests


# Backend API URL
API_URL = os.getenv('API_URL', 'http://localhost:8000')

# Streamlit App
st.set_page_config(page_title="YouTube Video QA", page_icon="🎥", layout="wide")
st.title("🎥 YouTube Video QA")
st.markdown("This app allows you to ask questions about the content of an **English** YouTube video. Please enter a video link to get started.")

# Session state to store whether the transcript is loaded
if "transcript_loaded" not in st.session_state:
    st.session_state["transcript_loaded"] = False

if "video_link" not in st.session_state:
    st.session_state["video_link"] = ""

# Input for YouTube video link
st.header("Step 1: Provide a YouTube Video Link")
video_link_input = st.text_input("Enter a YouTube video link (English videos only):", value=st.session_state["video_link"])

if st.button("Load Video"):
    if video_link_input:
        st.session_state["video_link"] = video_link_input
        # Call the backend API to load the transcript
        try:
            with st.spinner("Loading and processing the video transcript..."):
                response = requests.post(f"{API_URL}/load_transcript", json={"url": video_link_input})
                if response.status_code == 200:
                    st.session_state["transcript_loaded"] = True
                    st.success("Transcript loaded successfully!")
                else:
                    st.session_state["transcript_loaded"] = False
                    st.error(f"Error loading transcript: {response.json()['detail']}")
        except Exception as e:
            st.session_state["transcript_loaded"] = False
            st.error(f"Error connecting to backend: {e}")
    else:
        st.warning("Please enter a valid YouTube video link.")

# QA Section
if st.session_state["transcript_loaded"]:
    st.header("Step 2: Ask Questions about the Video")
    question_input = st.text_input("Enter your question:")
    if st.button("Get Answer"):
        if question_input:
            with st.spinner("Generating answer..."):
                # Call the backend API to get the answer
                try:
                    response = requests.post(f"{API_URL}/ask_question", json={"question": question_input})
                    if response.status_code == 200:
                        answer = response.json()["answer"]
                        st.write(f"**Question:** {question_input}")
                        st.write(f"**Answer:** {answer}")
                    else:
                        st.error(f"Error getting answer: {response.json()['detail']}")
                except Exception as e:
                    st.error(f"Error connecting to backend: {e}")
        else:
            st.warning("Please enter a question.")

    st.markdown("---")
    if st.button("Load a Different Video"):
        # Reset the session state
        st.session_state["transcript_loaded"] = False
        st.session_state["video_link"] = ""
        st.experimental_rerun()
else:
    st.info("Please load a video to start asking questions.")

# Footer
st.markdown("---")
st.markdown("**Note:** This app currently supports English videos only.")
