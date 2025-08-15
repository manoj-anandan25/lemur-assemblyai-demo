import assemblyai as aai

aai.settings.api_key = "your_API_KEY"

transcriber = aai.Transcriber()
transcript = transcriber.transcribe("meeting.mp3")

print("\n=== TRANSCRIPT ===")
print(transcript.text)

print("\n=== SUMMARY ===")
for sentence in transcript.text.split(".")[:5]:
    print("-", sentence.strip())
