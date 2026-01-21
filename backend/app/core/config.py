import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    DATA_DIR = os.path.join(BASE_DIR, "data")
    FAISS_INDEX_PATH = os.path.join(DATA_DIR, "faiss_index")

settings = Settings()