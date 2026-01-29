import streamlit as st
import pyttsx3
from functions.audio_asr import speech_to_text
from functions.data_vectors import create_vectorstore
from functions.llm_com import llm_communication


def rag(uploaded_file, question):
    # 1️⃣ Speech to text (run once)
    if "audio_text" not in st.session_state:
        print("\n🎤 Processing AUDIO File...\n")
        st.write("🎤 Processing Audio File...")
        text = speech_to_text(uploaded_file)
        st.session_state.audio_text = text
        print(text)

    text = st.session_state.audio_text

    # 2️⃣ Create vectorstore once
    if "vectorstore_audio" not in st.session_state:
        st.session_state.vectorstore_audio = create_vectorstore(
            text,
            "audio_store_chroma"
        )

    vectorstore = st.session_state.vectorstore_audio

    # 3️⃣ Print stored chunks ONCE (same pattern as CSV)
    file_chunk_key = "chunks_printed_audio"
    if not st.session_state.get(file_chunk_key, False):
        st.session_state[file_chunk_key] = True
        print("\n🧩 STORED CHUNKS (AUDIO):\n")
        try:
            for i, doc in enumerate(vectorstore._collection.get()["documents"]):
                print(f"Chunk {i + 1}:\n{doc}\n{'-' * 40}")
        except Exception as e:
            print(f"⚠️ Error printing chunks: {e}")

    # 4️⃣ Retrieval chain
    retrieval_chain = llm_communication(vectorstore)

    # 5️⃣ Ask question
    if question:
        response = retrieval_chain.invoke({"input": question})

        last_q_key = "last_audio_question"
        last_q = st.session_state.get(last_q_key)

        if last_q != question:
            print(f"\n❓ QUESTION:\n{question}")
            print(f"\n🧠 ANSWER:\n{response['answer']}\n")
            st.session_state[last_q_key] = question
        return response["answer"]

    return "No question provided"
