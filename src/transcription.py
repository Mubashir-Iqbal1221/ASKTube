from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs


class YouTubeTranscriptionService:

    def __extract_video_id_and_duration(self, youtube_url):
        """
        Extracts the video ID and duration from a YouTube URL.
        """
        # Parse the URL to extract query parameters
        parsed_url = urlparse(youtube_url)
        query_params = parse_qs(parsed_url.query)
        
        # Extract the video ID
        video_id = query_params.get("v", [None])[0]
        
        # Extract the duration parameter (if available)
        duration = query_params.get("t")
        if duration:
            # Remove the 's' (seconds) from the timestamp and convert to integer
            duration = int(duration[0].replace("s", ""))
        
        # Return both the video ID and duration
        return video_id, duration

    def __fetch_transcript(self, video_id):
        """
        Fetches the transcript of a YouTube video using the video ID.
        """
        try:
            # Fetch the transcript using YouTubeTranscriptApi
            transcript_data = YouTubeTranscriptApi.get_transcript(video_id)
            # Combine all lines of the transcript into a single string
            transcript = " ".join(line["text"] for line in transcript_data)
            return transcript
        except Exception as e:
            print(f"Error fetching transcript: {e}")
            return None

    def get_transcript_and_duration(self, youtube_url):
        """
        Public method to get the transcript and timestamp from a YouTube URL.
        """
        # Extract video ID and timestamp from the YouTube URL
        video_id, duration = self.__extract_video_id_and_duration(youtube_url)
        
        if not video_id:
            raise ValueError("Invalid YouTube URL: Video ID not found.")
        
        # Fetch the transcript using the video ID
        transcript = self.__fetch_transcript(video_id)
        print("Transcript: ")
        from pprint import pprint
        pprint(transcript)
        
        return transcript, duration
