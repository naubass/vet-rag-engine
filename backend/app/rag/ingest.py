import os
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from app.core.config import settings

def ingest_docs():
    print(f"Loading PDFs from {settings.DATA_DIR}...")
    loader = PyPDFDirectoryLoader(settings.DATA_DIR)
    docs = loader.load()

    if not docs:
        print("No PDFs found in data directory.")
        return

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=80,
    )
    splits = text_splitter.split_documents(docs)
    print(f"Loaded {len(splits)} documents chunks.")

    embeddings = HuggingFaceEmbeddings(model_name="Qwen/Qwen3-Embedding-0.6B")

    print("Creating FAISS index...")
    vectorstore = FAISS.from_documents(splits, embeddings)

    vectorstore.save_local(settings.FAISS_INDEX_PATH)
    print("FAISS index saved to", settings.FAISS_INDEX_PATH)

if __name__ == "__main__":
    ingest_docs()
