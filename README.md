# SIPS - Otomatisasi Testing Selenium Python

**SIPS (Sistem Informasi Pengarsipan Surat)** – Proyek ini berisi skrip otomatisasi fungsional menggunakan Selenium WebDriver dan pytest.

## 📋 Prasyarat
- Python 3.12+
- Browser Chrome
- ChromeDriver (Otomatis dikelola oleh webdriver-manager)

## 🚀 Instalasi & Persiapan

1. **Clone repositori:**
   ```bash
   git clone [https://github.com/Niloure/selenium-automation-test-SIPS.git](https://github.com/Niloure/selenium-automation-test-SIPS.git)
   cd selenium-automation-test-SIPS

2. Buat & Aktifkan Virtual Environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    venv\Scripts\activate     # Windows

3. Install Library:
    ```bash
    pip install -r requirements.txt

4. Konfigurasi Environment (.env):
    - PENTING: File .env asli tidak di-upload demi keamanan.

    - Copy file .env.example dan ubah namanya menjadi .env

    - Buka file .env tersebut dan isi dengan URL serta kredensial kamu sendiri.

🧪 Menjalankan Pengujian
- Jalankan perintah ini di terminal (pastikan venv sudah aktif):
    1. Menjalankan seluruh test:
        ```bash
        pytest -v

    2. Menjalankan test spesifik file (contoh: Disposisi):
        ```bash
        pytest -v tests/user/kepala_badan/test_disposisi.py

    3. menjalankan test spesifik testing (contoh: TestCetakAgendaKeluar::test_dengan_data):
        ```bash
        pytest -m "tests/user/sekretaris_badan/test_cetak_agenda_surat_keluar_sekretaris.py::TestCetakAgendaKeluar::test_tanpa_data"

    4. Melihat hasil capture jika gagal:
        - Cek folder screenshots/ jika ada test yang failed.