from app.graph.state import GraphState
from app.core.llm import get_llm
from app.rag.vectorstore import get_retriever
from app.rag.prompts import grader_prompt, diagnosis_prompt
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

llm = get_llm()
retriever = get_retriever()

def retrieve(state: GraphState):
    print("---NODE: RETRIEVE---")
    question = state["question"]

    print(f"Original Query: {question}")
    
    transform_prompt = ChatPromptTemplate.from_template(
        """Kamu adalah asisten medis veteriner yang cerdas. 
        Tugasmu adalah memformulasikan ulang pertanyaan user agar lebih cocok untuk pencarian di jurnal medis/akademis.
        
        Pertanyaan User: {question}
        
        Instruksi:
        1. Identifikasi gejala utama.
        2. Tambahkan istilah medis veteriner yang relevan (misal: "muntah" -> "vomiting/emesis", "susah pipis" -> "dysuria/stranguria/obstruction").
        3. Gabungkan pertanyaan asli dengan istilah medis tersebut.
        4. HANYA berikan hasil formulasi ulang, jangan ada basa-basi.
        
        Contoh:
        Input: "Kucing jantan tidak bisa pipis"
        Output: "Kucing jantan tidak bisa pipis feline lower urinary tract disease FLUTD urethral obstruction dysuria hematuria"
        """
    )
    
    # Chain untuk transform
    transform_chain = transform_prompt | llm | StrOutputParser()
    better_question = transform_chain.invoke({"question": question})
    
    print(f"Transformed Query: {better_question}")

    # earch ke FAISS menggunakan pertanyaan yang SUDAH DITERJEMAHKAN
    documents = retriever.invoke(better_question)
    
    # Kita kembalikan documents, tapi tetap simpan pertanyaan asli user untuk generate jawaban akhir
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