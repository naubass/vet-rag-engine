import os
import uvicorn
import webbrowser
from typing import Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles 
from pydantic import BaseModel
import shutil
from app.graph.workflow import get_app_graph

app = FastAPI(title="Vet RAG Engine")

# middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

rag_graph = get_app_graph()

UPLOAD_DIR = "temp_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class QueryRequest(BaseModel):
    symptoms: str

@app.post("/diagnose")
async def diagnose(symptoms: str = Form(...), image: Optional[UploadFile] =File(None)):
    image_path = None

    if image:
        try:
            image_path = os.path.join(UPLOAD_DIR, image.filename)
            with open(image_path, "wb") as buffer:
                shutil.copyfileobj(image.file, buffer)
            
            print(f"Gambar diupload: {image_path}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Gagal upload gambar: {str(e)}")
    
    inputs = {
        "question": symptoms,
        "image_path": image_path 
    }

    try:
        results = rag_graph.invoke(inputs)
        return {"diagnosis": results["generation"]}
    except Exception as e:
        return {"diagnosis": f"Terjadi kesalahan sistem: {str(e)}"}

base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
frontend_path = os.path.join(base_dir, "frontend")

app.mount("/", StaticFiles(directory=frontend_path, html=True), name="ui")

if __name__ == "__main__":
    print("Membuka browser...")
    # webbrowser.open("http://localhost:8000")

    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)