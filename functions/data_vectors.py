from langchain_text_splitters import RecursiveCharacterTextSplitter
#from langchain_huggingface import HuggingFaceEmbeddings
from sentence_transformers import SentenceTransformer
from langchain.embeddings.base import Embeddings

from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
import uuid
class SafeSentenceEmbeddings(Embeddings):
    def __init__(self):
        self.model = SentenceTransformer(
            "sentence-transformers/all-MiniLM-L6-v2",
            device="cpu"
        )

    def embed_documents(self, texts):
        return self.model.encode(
            texts,
            convert_to_numpy=True,
            show_progress_bar=False
        ).tolist()

    def embed_query(self, text):
        return self.model.encode(
            text,
            convert_to_numpy=True,
            show_progress_bar=False
        ).tolist()

# def create_vectorstore(text, store):
#     print("📄 Data loaded")

#     # Handle both string and list input
#     if isinstance(text, str):
#         documents = [Document(page_content=text)]
#     else:
#         documents = [Document(page_content=t) for t in text]

#     # Chunk text
#     text_splitter = RecursiveCharacterTextSplitter(
#         chunk_size=500,
#         chunk_overlap=200
#     )
#     docs_chunks = text_splitter.split_documents(documents)
#     # Embeddings (NO meta tensor issues)
#     embeddings = HuggingFaceEmbeddings(
#         model_name="sentence-transformers/all-MiniLM-L6-v2"
#     )

#     # Chroma vectorstore
#     vectorstore = Chroma.from_documents(
#         documents=docs_chunks,
#         embedding=embeddings,
#         persist_directory=store,
#         # collection_name=f"col_{uuid.uuid4().hex}"
#     )

#     print(f"✅ Stored {len(docs_chunks)} chunks in ChromaDB")
#     return vectorstore

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
import uuid

def create_vectorstore(text, store):
    print("📄 Data loaded")

    # Normalize input (works for pdf, image, txt, csv, wav transcripts)
    if isinstance(text, str):
        documents = [Document(page_content=text)]
    else:
        documents = [Document(page_content=t) for t in text]

    # Chunking (universal)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=200
    )
    docs_chunks = text_splitter.split_documents(documents)

    # SAFE embeddings (no meta tensor)
    embeddings = SafeSentenceEmbeddings()

    # Chroma vector store
    vectorstore = Chroma.from_documents(
        documents=docs_chunks,
        embedding=embeddings,
        persist_directory=store
    )

    print(f"✅ Stored {len(docs_chunks)} chunks in ChromaDB")
    return vectorstore

