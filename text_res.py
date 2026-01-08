import streamlit as st
from functions.data_vectors import create_vectorstore
from functions.llm_com import llm_communication


def rag(uploaded_file, question):
    """
    RAG pipeline for TXT files using Streamlit UploadedFile
    """

    # 1️⃣ Read TXT content ONCE
    if "txt_text" not in st.session_state:
        file_bytes = uploaded_file.read()
        text = file_bytes.decode("utf-8")

        # reset pointer (important!)
        uploaded_file.seek(0)

        st.session_state.txt_text = text

        print("\n📄 Processing TXT File...\n")
        print(text)

    text = st.session_state.txt_text

    # 2️⃣ Create vectorstore ONCE
    if "vectorstore_txt" not in st.session_state:
        st.session_state.vectorstore_txt = create_vectorstore(
            text,
            "txt_store_chroma"
        )

    vectorstore = st.session_state.vectorstore_txt

    # 3️⃣ Print stored chunks ONCE
    if "chunks_printed_txt" not in st.session_state:
        st.session_state.chunks_printed_txt = True
        print("\n🧩 STORED CHUNKS:\n")
        for i, doc in enumerate(vectorstore._collection.get()["documents"]):
            print(f"Chunk {i + 1}:\n{doc}\n{'-' * 40}")

    # 4️⃣ RAG / Query
    retrieval_chain = llm_communication(vectorstore)

    if question:
        response = retrieval_chain.invoke({"input": question})

        last_q = st.session_state.get("last_txt_question")
        if last_q != question:
            print(f"\n❓ QUESTION:\n{question}")
            print(f"\n🧠 ANSWER:\n{response['answer']}\n")
            st.session_state.last_txt_question = question

        return response["answer"]

    return "No question provided"
