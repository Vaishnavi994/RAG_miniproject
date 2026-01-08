# live_audio_recorder.py
import streamlit as st
import tempfile
import numpy as np
import soundfile as sf
import whisper
from functions.data_vectors import create_vectorstore
from functions.llm_com import llm_communication
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase

st.subheader("🎤 Live Audio Question Answering")

class CompactAudioProcessor(AudioProcessorBase):
    def __init__(self):
        self.frames = []

    def recv(self, frame):
        self.frames.append(frame.to_ndarray())
        return frame

webrtc_ctx = webrtc_streamer(
    key="compact-audio",
    audio_processor_factory=CompactAudioProcessor,
    media_stream_constraints={"audio": True, "video": False},
    async_processing=True
)

if webrtc_ctx and webrtc_ctx.audio_processor:
    query = st.text_input("Type your question about live audio:")

    if query and st.button("🟢 Get Answer"):
        frames = webrtc_ctx.audio_processor.frames
        if len(frames) == 0:
            st.warning("No audio captured. Please speak first.")
        else:
            tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
            audio_data = np.concatenate(frames, axis=0)
            sf.write(tmp_file.name, audio_data, 16000)

            model = whisper.load_model("base")
            transcription = model.transcribe(tmp_file.name)["text"]
            st.markdown(f"**Transcribed Audio:** {transcription}")

            vectorstore = create_vectorstore(transcription, "live_audio_chroma")
            retrieval_chain = llm_communication(vectorstore)
            response = retrieval_chain.invoke({"input": query})
            st.markdown(f"**Answer:** {response['answer']}")
