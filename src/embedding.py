import os 
import pickle 
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
import openai 
from langchain_openai import OpenAIEmbeddings
import time


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


# Load your raw data from pickle
with open('../data/processed/raw_data.pkl', 'rb') as f:
    data = pickle.load(f)

# Extract just the texts for chunking
texts = [text for _, text in data]

# Creating chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=["\n\n", "\n", ".", " ", ""]
)

chunks = []
for _, text in data:
    chunks.extend(splitter.split_text(text))

print(f"✅ Split into {len(chunks)} chunks.")


embeddings_model = OpenAIEmbeddings()
all_vectors = []

batch_size = 100  # You can tune this to avoid hitting token limits
for i in range(0, len(chunks), batch_size):
    batch = chunks[i:i + batch_size]
    try:
        vectors = embeddings_model.embed_documents(batch)
        all_vectors.extend(vectors)
        print(f"Embedded batch {i // batch_size + 1}")
    except Exception as e:
        print(f"Failed on batch {i // batch_size + 1}: {e}")
        time.sleep(5)  # wait before retry or move on

output_path = "../data/processed/embeddings.pkl"
with open(output_path, "wb") as f:
    pickle.dump((chunks, all_vectors), f)

print(f"Saved {len(all_vectors)} embeddings to {output_path}")

