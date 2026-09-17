import os
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

VECTORSTORE_DIR = "data/vectorstore"
DOCS_CHUNKS_FILE = os.path.join(VECTORSTORE_DIR, "chunks.json")

def retrieve(query: str, k: int = 3):
    """
    Lightweight RAG retrieval using TF-IDF.
    No heavy ML models are loaded, making it safe for free-tier hosting.
    """
    try:
        if not os.path.exists(DOCS_CHUNKS_FILE):
            print("No chunk file found. Run ingest.py to create it.")
            return []

        with open(DOCS_CHUNKS_FILE, 'r') as f:
            chunks = json.load(f)

        if not chunks:
            return []

        # Create a TF-IDF vectorizer and fit it on the chunks
        vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = vectorizer.fit_transform(chunks)

        # Transform the query and calculate similarity
        query_vec = vectorizer.transform([query])
        similarities = cosine_similarity(query_vec, tfidf_matrix).flatten()

        # Get the top k results
        top_indices = similarities.argsort()[-k:][::-1]

        results = []
        for idx in top_indices:
            if similarities[idx] > 0.01:  # Only return relevant results
                results.append({"content": chunks[idx], "metadata": {}})

        return results

    except Exception as e:
        print(f"RAG Retrieval failed: {e}")
        return []