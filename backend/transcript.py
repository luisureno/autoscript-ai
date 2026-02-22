from url_utils import is_valid_youtube_url, url_to_video_id
from youtube_transcript_api import YouTubeTranscriptApi

def get_transcript_for_url(url):
    video_id = url_to_video_id(url)
    if not video_id:
        raise ValueError("Invalid URL/ No video ID")

    try:
        
        ytt_api = YouTubeTranscriptApi().fetch(video_id)
        return ytt_api
        
    except Exception:
        raise ValueError("No transcript available")

    