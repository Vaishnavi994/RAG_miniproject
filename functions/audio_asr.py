from vosk import Model, KaldiRecognizer
import wave
import json
# Load Vosk model (download small model first, e.g., vosk-model-small-en-us-0.15)
def speech_to_text(input_file):
    from vosk import Model

    model_path = r"C:\Users\sampa\Desktop\Btech\MP\multimodel_rag\models\vosk-model-small-en-us-0.15"
    model = Model(model_path)

    # Open WAV file
    wf = wave.open(input_file, "rb")
    rec = KaldiRecognizer(model, wf.getframerate())

    text = ""
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            res = json.loads(rec.Result())
            text += res.get("text", "") + " "

    # Get final part
    res = json.loads(rec.FinalResult())
    text += res.get("text", "")
    return text
