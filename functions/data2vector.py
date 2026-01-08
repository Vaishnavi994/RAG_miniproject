from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

def process_text_to_docs(text, chunk_size=1000, chunk_overlap=200):
    """
    Takes raw text and converts it into manageable chunks for the Vector Store.
    """
    # 1. Initialize the splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        is_separator_regex=False,
    )

    # 2. Create document objects
    # We wrap the text in a Document object so metadata can be added if needed
    # docs = [Document(page_content=text, metadata={"source": "user_upload"})]
    docs = [Document(page_content=t, metadata={"source": "user_upload"}) for t in text]
    
    # 3. Split the documents into chunks
    split_docs = text_splitter.split_documents(docs)
    
    print(f"✂️ Split text into {len(split_docs)} chunks.")
    return split_docs