import os
import json
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

DOCS_DIR = "data/documents"
VECTORSTORE_DIR = "data/vectorstore"

def load_documents():
    docs = []
    if not os.path.exists(DOCS_DIR):
        os.makedirs(DOCS_DIR)
        return docs
    for file in os.listdir(DOCS_DIR):
        path = os.path.join(DOCS_DIR, file)
        if file.endswith(".pdf"):
            docs.extend(PyPDFLoader(path).load())
        elif file.endswith(".txt"):
            docs.extend(TextLoader(path).load())
    return docs

def ingest():
    print("Loading documents...")
    documents = load_documents()
    if not documents:
        print("No documents found. Add files to data/documents/")
        return

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)
    
    # Extract just the text content from the chunks
    chunk_texts = [chunk.page_content for chunk in chunks]
    
    os.makedirs(VECTORSTORE_DIR, exist_ok=True)
    output_file = os.path.join(VECTORSTORE_DIR, "chunks.json")
    
    with open(output_file, 'w') as f:
        json.dump(chunk_texts, f)
    
    print(f"Successfully ingested {len(chunk_texts)} chunks into {output_file}.")

if __name__ == "__main__":
    ingest()