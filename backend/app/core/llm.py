from langchain_groq import ChatGroq
from app.core.config import settings

def get_llm():
    """inisialisasi Model Llama 3 via langchain_groq"""
    return ChatGroq(
        api_key=settings.GROQ_API_KEY,
        model="llama-3.3-70b-versatile",
        temperature=0.5
    )