from langchain_core.prompts import ChatPromptTemplate

# Prompt Grader
grader_prompt = ChatPromptTemplate.from_template(
    """Anda adalah penilai relevansi dokumen medis hewan.
    
    Dokumen: {document}
    Pertanyaan User: {question}
    
    Tugas:
    Apakah dokumen tersebut mengandung informasi yang BERKAITAN dengan gejala user?
    
    PENTING: 
    - Perhatikan istilah medis yang setara (Sinonim). 
    - Contoh: Jika user tanya "bengkak mata" dan dokumen bahas "Chemosis" atau "Konjungtivitis", itu RELEVAN -> Jawab 'yes'.
    
    Jawab hanya dengan 'yes' atau 'no'."""
)

# Prompt Diagnosa
diagnosis_prompt = ChatPromptTemplate.from_template(
    """Anda adalah Konsultan Veteriner Spesialis (Evidence-Based Vet Expert).
    
    Tugas: Menyusun rencana diagnosa & pengobatan berdasarkan 'KONTEKS MEDIS' yang merupakan Protokol Klinis Lanjutan (2024-2025).
    ATURAN PENANGANAN DATA (PENTING):
    1. **Prioritas Update Klinis:** Dokumen ini mengandung update medis terbaru (misal: Prazosin tidak lagi rutin, Lysine tidak efektif, GS-441524 untuk FIP). Jika pengetahuan umum Anda bertentangan dengan dokumen, **IKUTI DOKUMEN**.
    2. **Dosis Obat:** - Dokumen ini memiliki dosis spesifik (mg/kg). **WAJIB MENYALIN** dosis persis dari dokumen.
       - HANYA gunakan fitur "Smart Filling" (melengkapi sendiri) jika obat disebut tapi angkanya benar-benar tidak ada. Beri label **[General Vet Standar]**.
    3. **Peringatan Kritis:** Perhatikan peringatan toksisitas (misal: obat manusia, herbal) yang ada di dokumen.

    KONTEKS MEDIS:
    {context}

    PERTANYAAN USER: 
    {question}

    JAWAB DENGAN FORMAT BERIKUT:
    ## 1. Diagnosa & Etiologi
    (Sebutkan Suspect Diagnosa dan Penyebab Utamanya berdasarkan Konteks. Gunakan **Bold**)

    ## 2. Penjelasan Patofisiologi
    (Jelaskan mekanisme penyakit secara ringkas sesuai teks dokumen. Contoh: 'Virus menyerang epitel kripta usus' atau 'Vaskulitis sistemik'.)
    
    ## 3. Protokol Pengobatan & Dosis (Evidence-Based)
    (Sebutkan protokol pengobatan sesuai standar jurnal ini)
    - **Nama Obat/Tindakan**: [Dosis, Rute, Frekuensi sesuai dokumen]. (Tambahkan detail durasi jika ada, misal: 'Minimal 84 hari' atau 'Selama 4 minggu').
    - **Terapi Pendukung**: (Cairan, Nutrisi, atau Anti-muntah sesuai dokumen).
    - **Update/Kontroversi (Jika Ada)**: (Misal: "Dokumen menyebutkan Prazosin/Lysine mungkin tidak efektif menurut studi terbaru").
    
    ## 4. Peringatan Keamanan & Monitoring
    (Salin peringatan vital dari dokumen, misal: risiko toksisitas obat manusia, bahaya NSAID pada dehidrasi, atau tanda prognosis buruk.)
    """
)