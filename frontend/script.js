async function analyzeSymptoms() {
    const symptoms = document.getElementById('symptomsInput').value;
    const btnText = document.getElementById('btnText');
    const btnIcon = document.getElementById('btnIcon'); // Icon panah
    const loadingIcon = document.getElementById('loadingIcon');
    const btnAnalyze = document.getElementById('btnAnalyze');
    const resultArea = document.getElementById('resultArea');
    const resultText = document.getElementById('resultText');

    if (!symptoms.trim()) {
        alert("Mohon isi deskripsi gejala hewan terlebih dahulu.");
        return;
    }

    // 1. UI Loading State
    btnText.innerText = "Sedang Menganalisa...";
    btnIcon.classList.add('hidden'); // Sembunyikan panah
    loadingIcon.classList.remove('hidden'); // Munculkan spinner
    
    btnAnalyze.disabled = true;
    btnAnalyze.classList.add('opacity-75', 'cursor-not-allowed');
    resultArea.classList.add('hidden'); // Sembunyikan hasil lama jika ada

    try {
        // 2. Tembak API Backend
        const response = await fetch('http://localhost:8000/diagnose', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ symptoms: symptoms })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        
        // 3. Render Hasil dengan Marked.js (Markdown -> HTML)
        // Pastikan marked.parse() dipanggil
        resultText.innerHTML = marked.parse(data.diagnosis);
        
        // 4. Tampilkan Area Hasil
        resultArea.classList.remove('hidden');
        
        // Scroll otomatis ke bagian hasil agar user langsung lihat
        resultArea.scrollIntoView({ behavior: 'smooth', block: 'start' });

    } catch (error) {
        console.error('Error:', error);
        alert("Gagal menghubungi server AI. Pastikan backend (main.py) sedang berjalan.");
    } finally {
        // 5. Reset UI ke semula
        btnText.innerText = "Analisa Kasus";
        btnIcon.classList.remove('hidden');
        loadingIcon.classList.add('hidden');
        btnAnalyze.disabled = false;
        btnAnalyze.classList.remove('opacity-75', 'cursor-not-allowed');
    }
}