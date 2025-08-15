import requests  # For making API calls to AssemblyAI
import time      # For waiting between polling requests


# 1. SETUP


# Replace this with your real API key from https://app.assemblyai.com
API_KEY = "your_API_KEY"

# Base URL for AssemblyAI API
BASE_URL = "https://api.assemblyai.com/v2"

# Headers sent with every request (for authentication)
headers = {"authorization": API_KEY}


# 2. UPLOAD AUDIO FILE

def upload_audio(filename):
    """
    Uploads an audio file to AssemblyAI's servers.
    Returns the upload URL which is needed to start transcription.
    """
    print("Uploading audio file to AssemblyAI...")
    with open(filename, "rb") as f:
        response = requests.post(f"{BASE_URL}/upload", headers=headers, data=f)
    upload_url = response.json()["upload_url"]
    print("Upload complete!")
    return upload_url


# 3. START TRANSCRIPTION

def start_transcription(audio_url):
    """
    Sends a transcription request to AssemblyAI using the uploaded audio URL.
    Returns the transcript ID for tracking job progress.
    """
    data = {"audio_url": audio_url}
    response = requests.post(f"{BASE_URL}/transcript", headers=headers, json=data)
    transcript_id = response.json()["id"]
    print(f"Transcription started! Job ID: {transcript_id}")
    return transcript_id



# 4. POLL FOR TRANSCRIPT

def get_transcription(transcript_id):
    """
    Polls AssemblyAI until the transcription job is completed.
    Returns the full transcript text.
    """
    print("Waiting for transcription to finish...")
    while True:
        response = requests.get(f"{BASE_URL}/transcript/{transcript_id}", headers=headers)
        result = response.json()

        if result["status"] == "completed":
            print("Transcription complete!")
            return result["text"]

        elif result["status"] == "error":
            return f"Error: {result['error']}"

        time.sleep(5)  # Wait 5 seconds before checking again


# 5. SIMPLE SUMMARY

def simple_summary(text):
    """
    Creates a short summary by taking the first 5 sentences.
    """
    sentences = text.split(".")
    return [s.strip() for s in sentences if s.strip()][:5]



# 6. MAIN PROGRAM

if __name__ == "__main__":
    # Change 'meeting.mp3' to your own audio file name
    audio_url = upload_audio("meeting.mp3")
    transcript_id = start_transcription(audio_url)
    transcript_text = get_transcription(transcript_id)

    print("\n=== TRANSCRIPT ===")
    print(transcript_text)

    print("\n=== SUMMARY ===")
    for sentence in simple_summary(transcript_text):
        print("-", sentence)
