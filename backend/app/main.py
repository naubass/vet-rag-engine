import os
import uvicorn
import webbrowser
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles 
from pydantic import BaseModel
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

class QueryRequest(BaseModel):
    symptoms: str

@app.post("/diagnose")
async def diagnose(req: QueryRequest):
    inputs = {"question": req.symptoms}
    results = rag_graph.invoke(inputs)

    return {"diagnosis": results["generation"]}

base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
frontend_path = os.path.join(base_dir, "frontend")

app.mount("/", StaticFiles(directory=frontend_path, html=True), name="ui")

if __name__ == "__main__":
    print("Membuka browser...")
    webbrowser.open("http://localhost:8000")

    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)