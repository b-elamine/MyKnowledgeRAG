import os
import pickle
import faiss 
import numpy as np

# paths
EMBEDDINGS_PATH = "../data/processed/embeddings.pkl"
VECTOR_STORE_PATH = "../data/vector_store/faiss_index.bin"
METADATA_PATH = "../data/vector_store/metadata.pkl"

def load_embeddings(embeddings_path=EMBEDDINGS_PATH):
   
    """
    loading embeddings and chunks tuples (chunks, vectors)
    """

    with open(embeddings_path, "rb") as f:
        data = pickle.load(f)
    chunks, vectors = data
    print(f"Loaded {len(chunks)} chunks and {len(vectors)} vectors.")
    return chunks, vectors

def build_faiss_index(vectors):
    
    # Dimension of faiss index
    dimension = len(vectors[0])
    index = faiss.IndexFlatL2(dimension)
    np_vectors = np.array(vectors).astype("float32")
    index.add(np_vectors)
    print(f"Added {index.ntotal} vectors to the FAISS index.")
    return index

def save_faiss_index(index, index_path=VECTOR_STORE_PATH):

    # Here we save the FAISS index to disk for future use

    os.makedirs(os.path.dirname(index_path), exist_ok=True)
    faiss.write_index(index, index_path)
    print(f"FAISS index saved to {index_path}")

def load_faiss_index(index_path=VECTOR_STORE_PATH):

    # Loading faiss index from disk
    if not os.path.exists(index_path):
        raise FileNotFoundError(f"FAISS index file not found at {index_path}")
    index = faiss.read_index(index_path)
    print(f"Loaded FAISS index from {index_path} with {index.ntotal} vectors.")
    return index


def save_metadata(chunks, metadata_path=METADATA_PATH):
    
    """
    Saving the chunks metadata (texts) associated with the embeddings.
    This is necessary to map from vector results back to the original text.
    """

    os.makedirs(os.path.dirname(metadata_path), exist_ok=True)
    with open(metadata_path, "wb") as f:
        pickle.dump(chunks, f)
    print(f"Saved chunks metadata to {metadata_path}")


def load_metadata(metadata_path=METADATA_PATH):
    if not os.path.exists(metadata_path):
        raise FileNotFoundError(f"Metadata file not found at {metadata_path}")
    with open(metadata_path, "rb") as f:
        chunks = pickle.load(f)
    print(f"Loaded {len(chunks)} chunks metadata from {metadata_path}")
    return chunks

def create_save_index():

    # building and saving everything

    chunks, vectors = load_embeddings()
    index = build_faiss_index(vectors)
    save_faiss_index(index)
    save_metadata(chunks)

    print("Vector Store Creation Completed !")


def query_index(query_vector, k=5):
    
    """
    Query the FAISS index for the k most similar vectors to the query vector.

    Returns:
      - indices of nearest neighbors
      - distances to nearest neighbors
    """

    index = load_faiss_index()
    chunks = load_metadata()

    query_vector = np.array(query_vector).astype("float32").reshape(1, -1)
    distance, indices = index.search(query_vector, k)

    # Map the actual text chunk of the found indices
    results = []
    for idx in indices[0]:
    
    # Why indices[0] ? indices is a list of lists because FAISS supports batch queries.
    # Since we only query one vector, we access indices[0].
        
        results.append(chunks[idx])
    return distance[0], results

if __name__ == "__main__":
    create_save_index()