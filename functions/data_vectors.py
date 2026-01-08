from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_chroma import Chroma
from transformers import AutoTokenizer, AutoModel
import chromadb
import torch
import uuid
import streamlit as st

import torch
from transformers import AutoTokenizer, AutoModel

class HFTransformerEmbeddings:
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        self.device = torch.device("cpu")

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

        # We set low_cpu_mem_usage=False to prevent the 'meta' device bug
        # and explicitly move to CPU
        self.model = AutoModel.from_pretrained(
            model_name,
            device_map=None,
            low_cpu_mem_usage=False
        ).to(self.device)
        
        self.model.eval()

    def _embed(self, texts):
        # Ensure all tokenizer outputs are on the CPU
        inputs = self.tokenizer(
            texts,
            padding=True,
            truncation=True,
            return_tensors="pt"
        ).to(self.device)

        with torch.no_grad():
            # Standard model call
            outputs = self.model(**inputs)
            
            # Mean Pooling: Average the sequence embeddings
            embeddings = outputs.last_hidden_state.mean(dim=1)
            return embeddings.cpu().numpy().tolist()

    def embed_documents(self, texts):
        return self._embed(texts)

    def embed_query(self, text):
        return self._embed([text])[0]

def create_vectorstore(text, store):
    # Clear Chroma cache to avoid tenant issues
    try:
        chromadb.api.client.SharedSystemClient.clear_system_cache()
    except Exception:
        pass

    print("📄 Data loaded")

    # Convert text to Document objects
    if isinstance(text, str):
        documents = [Document(page_content=text)]
    else:
        documents = [Document(page_content=t) for t in text]

    # Chunk documents
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=200
    )
    docs_chunks = splitter.split_documents(documents)

    # Create embeddings
    embeddings = HFTransformerEmbeddings()

    # Create Chroma vectorstore
    vectorstore = Chroma.from_documents(
        documents=docs_chunks,
        embedding=embeddings,
        persist_directory=store,
        collection_name=f"col_{uuid.uuid4().hex}"
    )

    print(f"✅ Stored {len(docs_chunks)} chunks in ChromaDB")
    return vectorstore
