import vosk
import tempfile
import os
import json
import io
import wave
from pydub import AudioSegment

# Load Vosk model ONCE (offline)
MODEL_PATH = "vosk-model-small-en-us-0.15"
model = vosk.Model(MODEL_PATH)


def extract_text_from_audio(uploaded_file):
    """
    Accepts MP3 or WAV (Streamlit UploadedFile)
    Returns OFFLINE transcribed text using Vosk
    """

    # 1️⃣ Convert MP3 → WAV if needed
    if hasattr(uploaded_file, "type") and uploaded_file.type in [
        "audio/mpeg",
        "audio/mp3",
        "audio/wav",
    ]:
        audio = AudioSegment.from_file(uploaded_file)
    else:
        audio = AudioSegment.from_file(uploaded_file)

    # 2️⃣ Force 16kHz mono (VERY IMPORTANT for Vosk)
    audio = audio.set_channels(1).set_frame_rate(16000)

    # 3️⃣ Save temp WAV
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        audio.export(tmp.name, format="wav")
        wav_path = tmp.name

    # 4️⃣ Speech Recognition
    wf = wave.open(wav_path, "rb")
    recognizer = vosk.KaldiRecognizer(model, wf.getframerate())

    text = ""

    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if recognizer.AcceptWaveform(data):
            res = json.loads(recognizer.Result())
            text += res.get("text", "") + " "

    final_res = json.loads(recognizer.FinalResult())
    text += final_res.get("text", "")

    wf.close()
    os.remove(wav_path)

    return text.strip()
