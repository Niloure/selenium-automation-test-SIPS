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
    python -m venv venv
    venv\Scripts\activate  # Untuk Windows

3. Install Library:
    Install Library:

4. Konfigurasi Environment (.env):
    PENTING: File .env asli tidak di-upload demi keamanan.

    - Copy file .env.example dan ubah namanya menjadi .env

    - Buka file .env tersebut dan isi dengan URL serta kredensial kamu sendiri.

🧪 Menjalankan Pengujian
Jalankan perintah ini di terminal (pastikan venv sudah aktif):
- Menjalankan seluruh test:
pytest -v

- Menjalankan test spesifik file (contoh: Disposisi):
pytest -v tests/user/kepala_badan/test_disposisi.py

- menjalankan test spesifik testing (contoh: TestCetakAgendaKeluar::test_dengan_data):
pytest -m "tests/user/sekretaris_badan/test_cetak_agenda_surat_keluar_sekretaris.py::TestCetakAgendaKeluar::test_tanpa_data"

- Melihat hasil capture jika gagal:
Cek folder screenshots/ jika ada test yang failed.