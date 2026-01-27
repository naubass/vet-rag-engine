// --- 1. Fungsi Preview Gambar (Saat user pilih file) ---
function previewImage(event) {
    const fileInput = event.target;
    const file = fileInput.files[0];
    const previewContainer = document.getElementById('imagePreviewContainer');
    const previewImage = document.getElementById('imagePreview');
    const fileNameDisplay = document.getElementById('fileName');

    if (file) {
        // Tampilkan nama file
        fileNameDisplay.innerText = file.name;
        fileNameDisplay.classList.add("text-vet-dark", "font-semibold");

        // Buat URL sementara untuk preview gambar
        const objectUrl = URL.createObjectURL(file);
        previewImage.src = objectUrl;
        
        // Munculkan container preview
        previewContainer.classList.remove('hidden');
    }
}

// --- 2. Fungsi Hapus Gambar (Tombol X kecil) ---
function removeImage() {
    const fileInput = document.getElementById('imageInput');
    const previewContainer = document.getElementById('imagePreviewContainer');
    const fileNameDisplay = document.getElementById('fileName');

    // Reset value input file
    fileInput.value = "";
    
    // Sembunyikan preview
    previewContainer.classList.add('hidden');
    
    // Reset teks nama file
    fileNameDisplay.innerText = "Belum ada foto dipilih";
    fileNameDisplay.classList.remove("text-vet-dark", "font-semibold");
}

// --- 3. Fungsi Utama: Kirim Data ke Backend ---
async function analyzeSymptoms() {
    const symptoms = document.getElementById('symptomsInput').value;
    const fileInput = document.getElementById('imageInput');
    
    // UI Elements
    const btnText = document.getElementById('btnText');
    const btnIcon = document.getElementById('btnIcon');
    const loadingIcon = document.getElementById('loadingIcon');
    const btnAnalyze = document.getElementById('btnAnalyze');
    const resultArea = document.getElementById('resultArea');
    const resultText = document.getElementById('resultText');

    // Validasi Sederhana: Harus ada Teks ATAU Gambar
    if (!symptoms.trim() && fileInput.files.length === 0) {
        alert("Mohon isi deskripsi gejala atau upload foto klinis hewan terlebih dahulu.");
        return;
    }

    // --- UI: Set Loading State ---
    btnText.innerText = "Sedang Menganalisa...";
    btnIcon.classList.add('hidden');
    loadingIcon.classList.remove('hidden');
    
    btnAnalyze.disabled = true;
    btnAnalyze.classList.add('opacity-75', 'cursor-not-allowed');
    resultArea.classList.add('hidden'); // Sembunyikan hasil lama

    try {
        // --- PERUBAHAN PENTING: Gunakan FormData ---
        const formData = new FormData();
        
        // 1. Masukkan Teks Gejala
        formData.append('symptoms', symptoms);

        // 2. Masukkan Gambar (Jika ada)
        if (fileInput.files.length > 0) {
            formData.append('image', fileInput.files[0]);
        }

        // --- Fetch ke Backend ---
        // PENTING: Jangan set 'Content-Type': 'application/json' manual!
        // Biarkan browser mengaturnya otomatis menjadi 'multipart/form-data'
        const response = await fetch('http://localhost:8000/diagnose', {
            method: 'POST',
            body: formData 
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        
        // Render Hasil Markdown ke HTML
        resultText.innerHTML = marked.parse(data.diagnosis);
        
        // Tampilkan Area Hasil
        resultArea.classList.remove('hidden');
        resultArea.scrollIntoView({ behavior: 'smooth', block: 'start' });

    } catch (error) {
        console.error('Error:', error);
        alert("Gagal menghubungi server AI. Pastikan backend (main.py) sedang berjalan.");
    } finally {
        // --- UI: Reset ke Semula ---
        btnText.innerText = "Analisa Kasus";
        btnIcon.classList.remove('hidden');
        loadingIcon.classList.add('hidden');
        btnAnalyze.disabled = false;
        btnAnalyze.classList.remove('opacity-75', 'cursor-not-allowed');
    }
}