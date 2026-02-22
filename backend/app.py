from flask import Flask, request, jsonify
from flask_cors import CORS
from transcript import get_transcript_for_url 
from dotenv import load_dotenv
import os
from anthropic import Anthropic

#https://www.youtube.com/watch?v=DVnJqq1vx-Q

load_dotenv()
app = Flask(__name__)
CORS(app)

api_key = os.getenv("ANTHROPIC_API_KEY")
client = Anthropic(api_key=api_key)

prompt_instructions = """You are a helpful assistant. 
I will provide a YouTube transcript. Please: Write a 
2-sentence executive summary. Create 3-5 sections with 
bold headings based on the main topics. List the 3 
most important Takeaways as bullet points."""


@app.route('/')
def home():
    return "The YouTube transcript is working!"

@app.route('/api/transcript', methods=['GET'])
def get_transcript_api():
    #'url' is the key name, while the value of it is the link the user submits
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "Missing URL"}), 400
    try:
        transcript_data = get_transcript_for_url(url)
        return jsonify(transcript_data), 200
    except ValueError:
        return jsonify({"error": "No transcript available"}), 400

    
@app.route('/api/summarize', methods=['POST'])
def summarize_api():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({"error": "The server recieved invalid or empty JSON"}), 400
    transcript = body.get('transcript')
    if not transcript:
        return jsonify({"error": "No trancript text provided in the request"}), 400
        
        
        # Test without API: set USE_MOCK_SUMMARY=1 in .env to return a fake summary
    # if os.getenv("USE_MOCK_SUMMARY", "").lower() in ("1", "true", "yes"):
    #     mock_summary = """**Executive summary:** This is a mock summary for testing without the Anthropic API. You can develop the frontend and Phase 5 markdown rendering.

    #     ## Section 1: Getting Started
    #     Content for the first section.

    #     ## Section 2: Main Topics
    #     Content for the second section.

    #     ## Section 3: Takeaways
    #     - First important takeaway.
    #     - Second important takeaway.
    #     - Third important takeaway.
    #     """
    #     return jsonify({"summary": mock_summary}), 200


    if not api_key:
        return jsonify({"error":"Server is missing API key"}), 500

    client = Anthropic(api_key=api_key)

    try:
        message = client.messages.create(
        max_tokens=1024,
        system=prompt_instructions,
            messages=[
                {
                "role": "user",
                "content": transcript,
                }
            ],
            model="claude-sonnet-4-5-20250929", 
        )
        message_text = message.content[0].text
        

        return jsonify({"summary": message_text}), 200
    except Exception as e:
        print(e)
        return jsonify({"error":"Summarization failed!"}), 500


if __name__ == "__main__":
    app.run()