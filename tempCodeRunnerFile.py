from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import os
import warnings

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
warnings.filterwarnings("ignore")

# Step 1: Read file
file = open(r"C:\Users\sampa\OneDrive\Desktop\Btech\MP\multimodel_rag\data\sample.txt", "r")
text = file.read()
file.close()

# Step 2: Clean text
clean_text = text.lower().strip().replace("\n", " ")

# Step 3: Chunking
words = clean_text.split(" ")
chunk_size = 5

chunks = []
for i in range(0, len(words), chunk_size):
    chunk = " ".join(words[i:i+chunk_size])
    chunks.append(chunk)

# Step 4: Load model & create embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")
chunk_embeddings = model.encode(chunks)

# Step 5: Ask a question
query = "What talks about funding?"
query_embedding = model.encode([query])

# Step 6: Semantic similarity
scores = cosine_similarity(query_embedding, chunk_embeddings)[0]

# Step 7: Find best match
best_index = np.argmax(scores)

print("\nUser Query:", query)
print("Best Matching Chunk:", chunks[best_index])
print("Similarity Score:", scores[best_index])
