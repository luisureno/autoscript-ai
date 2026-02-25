# AutoScript

Get YouTube video transcripts and AI-powered summaries in one place.

---

## Tech stack

- **Frontend:** React, TypeScript, Vite
- **Backend:** Flask (Python)
- **APIs:** [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api) (transcripts), Anthropic Claude (summaries)

---

## Run locally

**1. Backend**

- Open a terminal. Go to the project folder, then into the backend:
  - `cd backend`
  - 
- Create and activate a virtual environment:
  - Mac/Linux: `python3 -m venv venv` then `source venv/bin/activate`
  - Windows: `python -m venv venv` then `venv\Scripts\activate`
    
- Install dependencies: `pip install -r requirements.txt`
  
- Copy `backend/.env.example` to `backend/.env`. Edit `.env`:
  - To use real summaries: add your Anthropic API key as `ANTHROPIC_API_KEY` and set `USE_MOCK_SUMMARY=0` or remove it.
    
- Start the backend: `python3 app.py`  
  Leave this terminal open. Backend runs at **http://127.0.0.1:5000**.


**2. Frontend**

- Open a **new** terminal. From the project folder, go into the frontend:
  - `cd frontend`

- Install dependencies: `npm install`
  
- Start the app: `npm run dev`
  
- In the browser, open the URL shown (e.g. **http://localhost:5173**). The app talks to the backend at **http://127.0.0.1:5000**, so keep the backend running.

**3. Use the app**

Paste a YouTube URL, click **Get transcript**, then **Summarize**.
