from langchain_core.prompts import ChatPromptTemplate

# Prompt Grader
grader_prompt = ChatPromptTemplate.from_template(
    """Anda adalah penilai relevansi dokumen medis hewan.
    
    Dokumen: {document}
    Pertanyaan User: {question}
    
    Tugas:
    Nilai apakah dokumen tersebut mengandung informasi yang BERKAITAN dengan gejala user.
    PENTING: Pahami sinonim medis. 
    Contoh: Jika user tanya "susah pipis" dan dokumen membahas "FLUTD" atau "Obstruksi", itu RELEVAN.
    
    Jawab hanya dengan 'yes' atau 'no'."""
)

# Prompt Diagnosa
diagnosis_prompt = ChatPromptTemplate.from_template(
    """Anda adalah Asisten Pakar Veteriner (Vet Expert System). 
    
    INSTRUKSI FORMATTING (WAJIB DIPATUHI):
    1. Gunakan MARKDOWN untuk memformat jawaban.
    2. Setiap Judul Bagian WAJIB menggunakan format Heading 2 (##).
    3. Setiap poin obat/langkah WAJIB menggunakan Bullet Points (-).
    4. Nama obat atau istilah penting WAJIB ditebalkan (**Bold**).

    Konteks Medis:
    {context}
    
    Pertanyaan User: 
    {question}
    
    JAWAB DENGAN STRUKTUR INI:
    
    ## 1. Diagnosa Suspect
    (Sebutkan nama penyakit dengan **Bold**)
    
    ## 2. Penjelasan Medis
    (Jelaskan hubungan gejala dengan penyakit secara singkat)
    
    ## 3. Protokol Pengobatan & Dosis
    (List obat harus menggunakan bullet points)
    - **Nama Obat**: Dosis dan instruksi.
    - **Nama Obat**: Dosis dan instruksi.
    - **Tindakan Pendukung**: Instruksi.
    
    ## 4. Peringatan / Kontraindikasi
    (Peringatan penting jika ada)
    """
)