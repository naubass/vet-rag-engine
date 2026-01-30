import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from app.core.config import settings

def get_retriever():
    """Load FAISS index dan kembalikan sebagai retriever"""
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

    if not os.path.exists(settings.FAISS_INDEX_PATH):
        raise Exception("FAISS index not found. Run 'python ingest.py' first.")
    
    vectorstore = FAISS.load_local(
        settings.FAISS_INDEX_PATH, 
        embeddings, 
        allow_dangerous_deserialization=True
    )

    return vectorstore.as_retriever(search_kwargs={"k": 7})