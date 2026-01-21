from app.graph.state import GraphState
from app.core.llm import get_llm
from app.rag.vectorstore import get_retriever
from app.rag.prompts import grader_prompt, diagnosis_prompt
from langchain_core.output_parsers import StrOutputParser

llm = get_llm()
retriever = get_retriever()

def retrieve(state: GraphState):
    print("---NODE: RETRIEVE---")
    question = state["question"]
    documents = retriever.invoke(question)
    return {"documents": documents, "question": question}

def grade_documents(state: GraphState):
    print("---NODE: GRADE DOCUMENTS---")
    question = state["question"]
    documents = state["documents"]

    filtered_docs = []

    grader_chain = grader_prompt | llm | StrOutputParser()

    for doc in documents:
        score = grader_chain.invoke({"question": question, "document": doc.page_content})
        if "yes" in score.lower():
            filtered_docs.append(doc)

    return {"filtered_docs": filtered_docs, "question": question}

def generate(state: GraphState):
    print("---NODE: GENERATE---")
    question = state["question"]
    documents = state["documents"]

    if not documents:
        return {"generation": "Maaf, database kami belum memiliki informasi spesifik mengenai gejala tersebut."}
    
    context_text = "\n\n".join([doc.page_content for doc in documents])

    rag_chain = diagnosis_prompt | llm | StrOutputParser()
    generation = rag_chain.invoke({"context": context_text, "question": question})

    return {"generation": generation}