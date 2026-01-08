import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq 
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain

# Load environment variables from .env file
load_dotenv()

def llm_communication(vectorstore):
    # --- SAFETY CHECK ---
    api_key = os.getenv("GROQ_API_KEY")
    
    # If the key is missing or just says "gsk", this will stop the crash 
    # and tell you exactly what is wrong.
    if not api_key or len(api_key) < 10:
        raise ValueError(
            "❌ GROQ_API_KEY is missing or invalid in your .env file. "
            "It should look like: GROQ_API_KEY=gsk_XXXXX..."
        )

    # Initialize ChatGroq (Replaces ChatOpenAI)
    llm = ChatGroq(
        temperature=0, 
        model_name="llama-3.3-70b-versatile",
        groq_api_key=api_key
    )
    system_prompt = """You are an assistant for question-answering tasks.
Use the following pieces of retrieved context to answer the question: {context}

You are a precise document QA assistant.
Answer the user's question ONLY using the provided context.
Keep your response short, factual, and directly to the point.
Do NOT add extra explanations, summaries, or outside knowledge.

If the answer is not in the context, reply exactly:
"The information required to answer this question was not found in the provided document."
"""


    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])
    
    # Create the internal chain (How docs are formatted)
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    
    # Create the final RAG chain (Connecting retrieval to generation)
    return create_retrieval_chain(vectorstore.as_retriever(), question_answer_chain)