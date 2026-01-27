from app.graph.state import GraphState
from app.core.llm import get_llm
from app.rag.vectorstore import get_retriever
from app.rag.prompts import grader_prompt, diagnosis_prompt
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage
from app.core.llm import get_vision_llm
import base64

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
    
    for d in documents:
        # Jalankan Grader
        grade = grader_chain.invoke({"question": question, "document": d.page_content})
        
        # Debugging: Lihat apa jawaban AI sebenarnya
        print(f"Grade Result: {grade}") 
        
        # Bersihkan spasi/huruf besar kecil biar aman
        if "yes" in grade.lower():
            print("---DOC RELEVANT---")
            filtered_docs.append(d)
        else:
            print("---DOC NOT RELEVANT---")
            continue
            
    return {"documents": filtered_docs, "question": question}

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

def encode_image(image_path): 
    """Helper untuk ubah gambar jadi format yang bisa dibaca AI"""
    with open(image_path, "rb") as image_file: 
        return base64.b64encode(image_file.read()).decode("utf-8")
    
def analyze_image(state: GraphState):
    print("---NODE: ANALYZE IMAGE---")
    question = state.get("question", "")
    image_path = state.get("image_path", None)

    if not image_path:
        return {"question": question} 

    print(f"Analyzing Image: {image_path}")
    
    base64_image = encode_image(image_path) 
    vision_llm = get_vision_llm()
    
    msg = HumanMessage(
        content=[
            {"type": "text", "text": "Describe the clinical symptoms in this image for a vet diagnosis. Focus on lesions, swelling, or abnormalities."}, # Sedikit saya perbaiki prompt-nya
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
        ]
    )
    
    response = vision_llm.invoke([msg])
    image_description = response.content
    
    print(f"Vision Result: {image_description}") 
    
    enhanced_question = f"{question} . [Visual Findings: {image_description}]"
    
    # Return Dictionary (Sudah Benar)
    return {"question": enhanced_question}
