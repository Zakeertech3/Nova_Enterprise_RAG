import os
from langchain_qdrant import QdrantVectorStore
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from parsers import load_all_documents

QDRANT_PATH = os.path.join("data", "qdrant_db")
COLLECTION_NAME = "nova_assist_docs"

def index_documents():
    docs = load_all_documents()
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    
    chunked_docs = text_splitter.split_documents(docs)
    
    embeddings = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")
    
    QdrantVectorStore.from_documents(
        documents=chunked_docs,
        embedding=embeddings,
        path=QDRANT_PATH,
        collection_name=COLLECTION_NAME,
        force_recreate=True 
    )
    
    return len(chunked_docs)

if __name__ == "__main__":
    num_chunks = index_documents()
    print(f"Successfully indexed {num_chunks} document chunks into local Qdrant database.")