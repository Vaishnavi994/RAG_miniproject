import streamlit as st
from PyPDF2 import PdfReader
from functions.data_vectors import create_vectorstore
from functions.llm_com import llm_communication


def rag_pdf(file_path, question):
    """
    RAG pipeline for PDF files:
    1️⃣ Reads PDF once
    2️⃣ Creates vectorstore once per session
    3️⃣ Prints stored chunks once
    4️⃣ Answers questions using LLM
    """

    # 1️⃣ Read PDF content ONCE
    if "pdf_text" not in st.session_state:
        reader = PdfReader(file_path)
        text = ""

        print("\n📄 Processing PDF File...\n")

        for page_num, page in enumerate(reader.pages):
            page_text = page.extract_text()
            if page_text:
                # print(f"\n--- Page {page_num + 1} ---\n")
                # print(page_text)
                text += page_text + "\n"

        st.session_state.pdf_text = text

    text = st.session_state.pdf_text

    # 2️⃣ Create vectorstore ONCE
    if "vectorstore_pdf" not in st.session_state:
        st.session_state.vectorstore_pdf = create_vectorstore(
            text, "pdf_store_chroma"
        )

    vectorstore = st.session_state.vectorstore_pdf

    # 3️⃣ Print stored chunks ONCE per file
    file_chunk_key = f"pdf_chunks_printed_{file_path.name}"
    if not st.session_state.get(file_chunk_key, False):
        st.session_state[file_chunk_key] = True
        print("\n🧩 STORED CHUNKS:\n")
        try:
            for i, doc in enumerate(vectorstore._collection.get()["documents"]):
                print(f"Chunk {i+1}:\n{doc}\n{'-'*40}")
        except Exception as e:
            print(f"⚠️ Error printing chunks: {e}")

    # 4️⃣ RAG / Question Answering
    retrieval_chain = llm_communication(vectorstore)

    if question:
        response = retrieval_chain.invoke({"input": question})

        last_q_key = "last_pdf_question"
        last_q = st.session_state.get(last_q_key)

        if last_q != question:
            print(f"\n❓ QUESTION:\n{question}")
            print(f"\n🧠 ANSWER:\n{response['answer']}\n")
            st.session_state[last_q_key] = question

        return response["answer"]

    return "No question provided"
