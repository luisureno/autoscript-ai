import './App.css'
import {useState, type ChangeEvent, type MouseEvent} from 'react'

function App() {
  const [url, setURL] = useState<string>("")
  const API_KEY_NAME = 'url'

  type Snippet = {
    text: string,
    start?: number,
    duration?: number
  }

  const [transcriptData, setTranscriptData] = useState<Snippet[]>([])

  const [summary, setSummary] = useState<string>("")
  const [isSummarizing, setIsSummarizing] = useState(false)
  const handleURL = (event: ChangeEvent<HTMLInputElement>) => {
    setURL(event.target.value)

  }

  const fetchTranscript = (_event: MouseEvent<HTMLButtonElement>) => {
    const backendURL = `http://127.0.0.1:5000/api/transcript?${API_KEY_NAME}=${encodeURIComponent(url)}`
    fetch(backendURL)
    .then((res: Response) => res.json())
    .then(data => {
      console.log(data)
      setTranscriptData(data.snippets)
    })
    

  }

  const handleSummarize = (_event: MouseEvent<HTMLButtonElement>) => {
    setIsSummarizing(true)
    const transcriptString = transcriptData.map((item) => item.text).join(" ")
    const summarizeURL = `http://127.0.0.1:5000/api/summarize`
    fetch(summarizeURL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ transcript: transcriptString })
    })
      .then(res => {
        if (!res.ok) {
          throw new Error("Server went kaboom")
        }
        return res.json()
      })
      .then(data => {
        setSummary(data.summary)
      })
      .catch(error => {
        setSummary("Error:" + error.message)
      })
      .finally(() => {
        setIsSummarizing(false)
      })
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>AutoScript</h1>
        <p className="app-tagline">AI-powered video transcripts & summaries</p>
      </header>
      <section className="youtube-url">
        <input
          type="url"
          value={url}
          onChange={handleURL}
          placeholder="Paste a YouTube video URL"
          aria-label="YouTube video URL"
        />
        <button type="button" onClick={fetchTranscript}>Get transcript</button>
      </section>
      {transcriptData.length > 0 && (
        <>
          <details className="transcript-section">
            <summary>Transcript ({transcriptData.length} snippets)</summary>
            <div className="transcript-content">
              {transcriptData.map((item, index) => (
                <p key={index}>{item.text.replace('>>', '')}</p>
              ))}
            </div>
          </details>
          <button type="button" onClick={handleSummarize} disabled={isSummarizing}>
            {isSummarizing ? 'Summarizing…' : 'Summarize'}
          </button>
        </>
      )}
      {(summary || isSummarizing) && (
        <section className="summary-results" aria-live="polite">
          <h2>Summary</h2>
          <div className="summary-text">
            {isSummarizing ? 'Please wait…' : summary}
          </div>
        </section>
      )}
    </div>
  )
}

export default App
