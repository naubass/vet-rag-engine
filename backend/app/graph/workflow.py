from langgraph.graph import END, StateGraph
from app.graph.nodes import generate, retrieve, grade_documents
from app.graph.state import GraphState
from app.graph.nodes import analyze_image

def get_app_graph():
    workflow = StateGraph(GraphState)

    # add nodes
    workflow.add_node("analyze_image", analyze_image)
    workflow.add_node("retrieve", retrieve)
    workflow.add_node("grade_documents", grade_documents)
    workflow.add_node("generate", generate)

    # add edges
    workflow.set_entry_point("analyze_image")
    workflow.add_edge("analyze_image", "retrieve")
    workflow.add_edge("retrieve", "grade_documents")
    workflow.add_edge("grade_documents", "generate")
    workflow.add_edge("generate", END)

    return workflow.compile()