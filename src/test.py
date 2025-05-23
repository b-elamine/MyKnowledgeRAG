from vector_store import query_index
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import openai 
import os 

# Initialize the embeddings model
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
embeddings_model = OpenAIEmbeddings()

# Your query text
query_text = "is this person good at reactjs"

# Convert query text to vector
query_vector = embeddings_model.embed_query(query_text)

# Use the query_index function to get similar chunks and distances
distances, results = query_index(query_vector, k=5)

print("Top 5 similar chunks:")
for dist, chunk in zip(distances, results):
    print(f"Distance: {dist:.4f}\nText snippet: {chunk[:300]}...\n")
