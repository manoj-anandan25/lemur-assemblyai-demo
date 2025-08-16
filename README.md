Lemur AssemblyAI Transcription Example

This project shows how to:
- Upload an audio file to [AssemblyAI](https://www.assemblyai.com)
- Get a transcription
- Display a short summary

It’s designed to be **beginner-friendly** for freshers and **developer-friendly** for quick API integration.

---

## What is Lemur? (Non-Technical Explanation)

Think of **Lemur** as a helper monkey 🐒 that listens to your audio and writes down exactly what was said.  
It can take an audio file — like a meeting recording, an interview, or a voice note — and turn it into text you can read.  

In this example:
1. You give Lemur your audio file.
2. Lemur sends it to **AssemblyAI**, which is a smart service that understands speech.
3. Lemur waits until AssemblyAI finishes writing everything down.
4. You get the full text **and** a short bullet-point summary.


---

 Overview

AssemblyAI lets you:
- Convert speech to text with high accuracy
- Summarize, detect sentiment, and more
- Use either REST API or the official Python SDK

This example demonstrates **both** approaches:
1. Using `requests` to call the REST API directly
2. Using the official Python SDK (simpler for developers)

---

Installation

1. **Clone the repo**
```bash
git clone https://github.com/yourusername/lemur-assemblyai-demo.git
cd lemur-assemblyai-demo
````

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Add your API key**

* Open `main.py` and replace:

```python
API_KEY = "your_API_KEY"
```

with your key from your AssemblyAI account.

---

## ▶️ Usage (REST API Method)

1. Place an audio file (e.g., `meeting.mp3`) in the same folder.
2. Run:

```bash
python main.py
```

3. You’ll see:

```
Uploading audio file to AssemblyAI...
Upload complete!
Transcription started! Job ID: <id>
Waiting for transcription to finish...
Transcription complete!

=== TRANSCRIPT ===
Hello everyone, welcome to today's meeting...

=== SUMMARY ===
- Hello everyone, welcome to today's meeting
- We discussed project updates
- Marketing launch next week
```

---

## 💻 Developer SDK Example

If you prefer using the **official Python SDK**:

```python
import assemblyai as aai

aai.settings.api_key = "your_API_KEY"

transcriber = aai.Transcriber()
transcript = transcriber.transcribe("meeting.mp3")

print("\n=== TRANSCRIPT ===")
print(transcript.text)

print("\n=== SUMMARY ===")
for sentence in transcript.text.split(".")[:5]:
    print("-", sentence.strip())
```

Install SDK (already in requirements.txt):

```bash
pip install assemblyai
```

Run:

```bash
python sdk_demo.py
```

---

## 🔗 Useful Links

* [AssemblyAI API Docs](https://www.assemblyai.com/docs)
* [Python SDK Guide](https://www.assemblyai.com/docs/getting-started)

---

## 📝 Notes

* Audio can be in MP3, WAV, or M4A formats.
* Longer audio takes more time to transcribe.
* You can extend the script for summarization, topic detection, or sentiment analysis.

---

## Need an Even Simpler Example?

Gotcha — here’s the **quickest way to get a transcript with “Lemur” (AssemblyAI)**. 
Three options:
Super-simple Python (fresher-friendly), 
SDK (even simpler), 
and raw REST/cURL.

---

### 1) Fresher-friendly Python (single file)

```python
# lemur_transcript.py
import requests, time

API_KEY = "your_API_KEY"           # <-- put your key here
BASE = "https://api.assemblyai.com/v2"
HEADERS = {"authorization": API_KEY}

def upload_audio(path):
    with open(path, "rb") as f:
        r = requests.post(f"{BASE}/upload", headers=HEADERS, data=f)
    return r.json()["upload_url"]

def start_transcription(audio_url):
    r = requests.post(f"{BASE}/transcript", headers=HEADERS, json={"audio_url": audio_url})
    return r.json()["id"]

def wait_for_text(tid):
    while True:
        r = requests.get(f"{BASE}/transcript/{tid}", headers=HEADERS)
        data = r.json()
        if data["status"] == "completed":
            return data["text"]
        if data["status"] == "error":
            raise RuntimeError(data["error"])
        time.sleep(5)

if __name__ == "__main__":
    audio_url = upload_audio("meeting.mp3")   # replace with your file
    tid = start_transcription(audio_url)
    text = wait_for_text(tid)
    print("\n=== TRANSCRIPT ===\n" + text)
```

Run:

```bash
pip install requests
python lemur_transcript.py
```

---

### 2) Using the official Python SDK (shortest)

```python
# lemur_sdk_transcript.py
import os, assemblyai as aai

aai.settings.api_key = os.getenv("AAI_API_KEY") or "your_API_KEY"

t = aai.Transcriber().transcribe("meeting.mp3")  # or a public URL
if t.error:
    raise RuntimeError(t.error)

print("\n=== TRANSCRIPT ===\n" + (t.text or ""))
```

Run:

```bash
pip install assemblyai
python lemur_sdk_transcript.py
```

---

### 3) Raw REST (cURL) — upload → transcribe → get result

```bash
# 1) Upload
curl -X POST "https://api.assemblyai.com/v2/upload" \
  -H "authorization: YOUR_API_KEY" \
  --data-binary @meeting.mp3
# => copy the "upload_url" from the JSON response
```

```bash
# 2) Start transcription
curl -X POST "https://api.assemblyai.com/v2/transcript" \
  -H "authorization: YOUR_API_KEY" \
  -H "content-type: application/json" \
  -d '{"audio_url":"PASTE_UPLOAD_URL_HERE"}'
# => copy the "id" (transcript id)
```

```bash
# 3) Poll for completion
curl -X GET "https://api.assemblyai.com/v2/transcript/TRANSCRIPT_ID" \
  -H "authorization: YOUR_API_KEY"
# When "status":"completed", read the "text" field for your transcript
```

---

## Example transcript output:

```
=== TRANSCRIPT ===
Hello everyone, thanks for joining today. We reviewed the sprint goals...
```


