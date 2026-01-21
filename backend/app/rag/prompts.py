from langchain_core.prompts import ChatPromptTemplate

# Prompt Grader (Tetap sama)
grader_prompt = ChatPromptTemplate.from_template(
    """Anda adalah sistem validasi medis.
    Dokumen: {document}
    Pertanyaan: {question}
    Apakah dokumen ini memuat informasi penyakit atau gejala yang relevan? 
    Jawab 'yes' atau 'no'."""
)

# Prompt Diagnosa (DIPERBARUI MENJADI LEBIH SPESIFIK)
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