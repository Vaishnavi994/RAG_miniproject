import openai

openai.api_key = "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"

audio_file = open("audio.mp3", "rb")

transcript = openai.audio.transcriptions.create(
    file=audio_file,
    model="gpt-4o-mini-transcribe"  # or "whisper-1"
)

print(transcript.text)
