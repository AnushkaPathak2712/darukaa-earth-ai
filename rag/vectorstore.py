import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# Centralized configuration
VECTORSTORE_DIR = "data/vectorstore"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

def get_embeddings():
    """Returns the HuggingFace embeddings model."""
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

def get_vectorstore():
    """Loads an existing ChromaDB vectorstore from disk."""
    if not os.path.exists(VECTORSTORE_DIR):
        print(f"Warning: Vectorstore not found at {VECTORSTORE_DIR}. Run ingest.py first.")
        return None
    embeddings = get_embeddings()
    return Chroma(persist_directory=VECTORSTORE_DIR, embedding_function=embeddings)

def create_vectorstore(chunks):
    """Creates a new ChromaDB vectorstore from document chunks and saves it."""
    embeddings = get_embeddings()
    print(f"Generating embeddings for {len(chunks)} chunks...")
    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=VECTORSTORE_DIR
    )
    vectordb.persist()
    return vectordb