
# AskTube

AskTube is a web application that allows users to ask questions about the content of YouTube videos. It leverages FastAPI for the backend, GPT4All for question answering, and Streamlit for the frontend.

## Features

- Load YouTube video transcripts.
- Ask questions about the content of the video and get concise answers.
- Supports English videos only.
- Easy-to-use Streamlit-based user interface.

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.8+
- [YouTube Transcript API](https://pypi.org/project/youtube-transcript-api/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Streamlit](https://streamlit.io/)
- [Langchain](https://langchain.com/)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Mubashir-Iqbal1221/ASKTube.git
   cd AskTube
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file to store environment variables:
   ```bash
   touch .env
   ```

   Inside the `.env` file, add the following:
   ```bash
   GROQ_API_KEY=your_groq_api_key
   API_URL=http://localhost:8000
   ```

4. Ensure that the `configs/configs.yaml` file contains the correct configuration for the embeddings, language model, and other parameters.

## Running the Application

1. Start the FastAPI backend:
   ```bash
   uvicorn app:app --reload
   ```

2. In a new terminal, start the Streamlit frontend:
   ```bash
   streamlit run gui.py
   ```

3. Access the application:
   - The backend will be available at: `http://localhost:8000`
   - The frontend will be available at: `http://localhost:8501`

## Usage

1. **Load YouTube Video Transcript:**
   - Paste a valid YouTube video URL into the input field and click "Load Video."
   - The backend will fetch the transcript and load it for processing.

2. **Ask Questions:**
   - Once the transcript is loaded, you can ask questions about the video's content.
   - Type a question in the input field and click "Get Answer" to receive a concise response.

3. **Reset:**
   - If you want to load a different video, click "Load a Different Video" to reset the session.

## Project Structure

```plaintext
.
├── app.py                 # FastAPI backend
├── gui.py                 # Streamlit frontend
├── configs/
│   └── configs.yaml       # Configuration for embeddings and model
├── models/                # Model files
├── src/
│   ├── chatbot.py         # Handles question-answering logic
│   ├── transcription.py   # Fetches YouTube transcripts
│   └── utils.py           # Utility functions
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
└── README.md              # Project documentation
```

## Technologies Used

- **FastAPI**: For building the backend API.
- **Streamlit**: For creating the frontend UI.
- **Langchain**: To handle text processing and embeddings.
- **GPT4All**: For generating answers based on the transcript.
- **Chroma**: Vector store for similarity search.
- **YouTube Transcript API**: To extract transcripts from YouTube videos.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Acknowledgements

- [Langchain](https://langchain.com/)
- [Streamlit](https://streamlit.io/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [YouTube Transcript API](https://pypi.org/project/youtube-transcript-api/)
```