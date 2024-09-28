from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import os
import logging

from src.transcription import YouTubeTranscriptionService
from src.chatbot import YouTubeQA
from src.utils import load_config
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
os.environ["CUDA_VISIBLE_DEVICES"] = ""



# Initialize logging
logging.basicConfig(level=logging.INFO)

# Load configuration
CONFIG_FILE_PATH = "configs/configs.yaml"
config = load_config(CONFIG_FILE_PATH)


api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("GROQ_API_KEY is not set in the environment variables.")


youtube_qa = YouTubeQA(config["Models"])
app = FastAPI(title="YouTube QA API")

# Data models for request and response bodies
class VideoLink(BaseModel):
    url: str

class Question(BaseModel):
    question: str

class Answer(BaseModel):
    answer: str

transcription_service = YouTubeTranscriptionService()

@app.post("/load_transcript", response_model=dict)
def load_transcript(video_link: VideoLink):
    """
    Load the transcript of a YouTube video and prepare it for question answering.
    """
    try:
        transcript, duration = transcription_service.get_transcript_and_duration(video_link.url)
        youtube_qa.load_transcript(transcript)
        return {"message": "Transcript loaded successfully.", "transcript": transcript}
    except Exception as e:
        logging.error(f"Error loading transcript: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask_question", response_model=Answer)
def ask_question(question: Question):
    """
    Ask a question based on the loaded transcript.
    """
    try:
        answer = youtube_qa.get_answer(question.question)
        return {"answer": answer}
    except ValueError as ve:
        logging.error(f"Value error: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logging.error(f"Error getting answer: {e}")
        raise HTTPException(status_code=500, detail=str(e))
