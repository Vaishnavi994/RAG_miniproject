# import pandas as pd
# from functions.data_vectors import create_vectorstore
# from functions.llm_com import llm_communication
# import streamlit as st

# def rag_csv(file_path, question):
#     """
#     RAG pipeline for CSV files.
#     Reads CSV, creates vectorstore, prints chunks, answers question.
#     """
#     # 1️⃣ Read CSV content
#     if "csv_text" not in st.session_state:
#         df = pd.read_csv(file_path)
#         text = df.to_csv(index=False)
#         st.session_state.csv_text = text

#         # ✅ Print CSV content once
#         print("\n📄 Processing CSV File...\n")
#         print(text)
    
#     text = st.session_state.csv_text

#     # 2️⃣ Create vectorstore once
#     if "vectorstore_csv" not in st.session_state:
#         st.session_state.vectorstore_csv = create_vectorstore(text, "csv_store_chroma")
    
#     vectorstore = st.session_state.vectorstore_csv
#     file_chunk_key = f"chunks_printed_{file_path.name}"

#     if not st.session_state.get(file_chunk_key, False):
#         st.session_state[file_chunk_key] = True
#     # 3️⃣ Print stored chunks once
#     if "chunks_printed_csv" not in st.session_state:
#         st.session_state.chunks_printed_csv = True
#         print("\n🧩 STORED CHUNKS:\n")
#         for i, doc in enumerate(vectorstore._collection.get()["documents"]):
#             print(f"Chunk {i+1}:\n{doc}\n{'-'*40}")

#     # 4️⃣ RAG / Query
#     retrieval_chain = llm_communication(vectorstore)
#     if question:
#         response = retrieval_chain.invoke({"input": question})

#         # ✅ Print Q&A once per question
#         last_q = st.session_state.get("last_csv_question")
#         if last_q != question:
#             print(f"\n❓ QUESTION:\n{question}")
#             print(f"\n🧠 ANSWER:\n{response['answer']}\n")
#             st.session_state.last_csv_question = question

#         return response["answer"]

#     return "No question provided"
import pandas as pd
import streamlit as st
from functions.data_vectors import create_vectorstore
from functions.llm_com import llm_communication

def rag_csv(file_path, question):
    """
    RAG pipeline for CSV files:
    1️⃣ Reads CSV
    2️⃣ Creates vectorstore (once per session)
    3️⃣ Prints chunks (once per file)
    4️⃣ Answers question using LLM
    """

    # 1️⃣ Read CSV content once
    if "csv_text" not in st.session_state:
        df = pd.read_csv(file_path)
        text = df.to_csv(index=False)
        st.session_state.csv_text = text

        print("\n📄 Processing CSV File...\n")
        print(text)
    
    text = st.session_state.csv_text

    # 2️⃣ Create vectorstore once
    if "vectorstore_csv" not in st.session_state:
        st.session_state.vectorstore_csv = create_vectorstore(text, "csv_store_chroma")
    
    vectorstore = st.session_state.vectorstore_csv

    # 3️⃣ Print stored chunks once per file
    file_chunk_key = f"chunks_printed_{file_path.name}"
    if not st.session_state.get(file_chunk_key, False):
        st.session_state[file_chunk_key] = True
        print("\n🧩 STORED CHUNKS:\n")
        try:
            for i, doc in enumerate(vectorstore._collection.get()["documents"]):
                print(f"Chunk {i+1}:\n{doc}\n{'-'*40}")
        except Exception as e:
            print(f"⚠️ Error printing chunks: {e}")

    # 4️⃣ RAG / Query
    retrieval_chain = llm_communication(vectorstore)

    if question:
        response = retrieval_chain.invoke({"input": question})

        # Print Q&A once per question
        last_q_key = "last_csv_question"
        last_q = st.session_state.get(last_q_key)
        if last_q != question:
            print(f"\n❓ QUESTION:\n{question}")
            print(f"\n🧠 ANSWER:\n{response['answer']}\n")
            st.session_state[last_q_key] = question

        return response["answer"]

    return "No question provided"

