from typing import List, TypedDict, Any

class GraphState(TypedDict):
    question: str
    generation: str
    documents: List[Any] 
    image_path: str