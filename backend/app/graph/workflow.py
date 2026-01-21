from langgraph.graph import END, StateGraph
from app.graph.nodes import generate, retrieve, grade_documents
from app.graph.state import GraphState

def get_app_graph():
    workflow = StateGraph(GraphState)

    # add nodes
    workflow.add_node("retrieve", retrieve)
    workflow.add_node("grade_documents", grade_documents)
    workflow.add_node("generate", generate)

    # add edges
    workflow.set_entry_point("retrieve")
    workflow.add_edge("retrieve", "grade_documents")
    workflow.add_edge("grade_documents", "generate")
    workflow.add_edge("generate", END)

    return workflow.compile()