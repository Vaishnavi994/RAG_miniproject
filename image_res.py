import streamlit as st
from functions.data_vectors import create_vectorstore
from functions.llm_com import llm_communication
from functions.image_ocr import extract_text_from_image  # your tesseract OCR


def rag_image(uploaded_file, question):
    """
    RAG pipeline for IMAGE files using offline Tesseract OCR
    """

    # 1️⃣ OCR image ONCE
    if "img_text" not in st.session_state:
        text = extract_text_from_image(uploaded_file)

        # reset pointer (important!)
        uploaded_file.seek(0)

        st.session_state.img_text = text

        print("\n🖼️ Processing IMAGE File (OCR)...\n")
        print(text)

    text = st.session_state.img_text

    # 2️⃣ Create vectorstore ONCE
    if "vectorstore_img" not in st.session_state:
        st.session_state.vectorstore_img = create_vectorstore(
            text,
            "img_store_chroma"
        )

    vectorstore = st.session_state.vectorstore_img

    # 3️⃣ Print stored chunks ONCE
    if "chunks_printed_img" not in st.session_state:
        st.session_state.chunks_printed_img = True
        print("\n🧩 STORED CHUNKS (IMAGE OCR):\n")
        for i, doc in enumerate(vectorstore._collection.get()["documents"]):
            print(f"Chunk {i + 1}:\n{doc}\n{'-' * 40}")

    # 4️⃣ RAG / Query
    retrieval_chain = llm_communication(vectorstore)

    if question:
        response = retrieval_chain.invoke({"input": question})

        last_q = st.session_state.get("last_img_question")
        if last_q != question:
            print(f"\n❓ QUESTION:\n{question}")
            print(f"\n🧠 ANSWER:\n{response['answer']}\n")
            st.session_state.last_img_question = question

        return response["answer"]

    return "No question provided"
