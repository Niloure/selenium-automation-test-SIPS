# SIPS - Automated Functional Testing

**SIPS (Sistem Informasi Pengarsipan Surat)** adalah proyek otomasi pengujian fungsional berbasis web. Proyek ini dibangun untuk memastikan alur kerja persuratan (Surat Masuk, Keluar, hingga Disposisi) berjalan dengan benar di berbagai role pengguna.

## 🚀 Fitur Utama
- **End-to-End Testing:** Mencakup skenario login hingga cetak agenda.
- **Role-Based Access Control (RBAC):** Validasi akses untuk Admin, Kepala Badan, Sekretaris, dan Master Admin.
- **Smart Waiting:** Penanganan loading overlay otomatis menggunakan Selenium Explicit Wait.
- **Auto-Screenshot:** Menangkap gambar secara otomatis jika test gagal (tersimpan di folder `/screenshots`).

## 🛠️ Tech Stack & Library
- **Python 3.12.2**
- **Selenium:** Driver interaksi browser.
- **Pytest:** Test runner dan assertion.
- **Python-Decouple:** Manajemen environment (.env).
- **Webdriver-Manager:** Otomatisasi update driver Chrome/Edge.

## 📋 Panduan Instalasi (Step-by-Step)

1. **Clone & Masuk ke Folder:**
   ```bash
   git clone [https://github.com/Niloure/selenium-automation-test-SIPS.git](https://github.com/Niloure/selenium-automation-test-SIPS.git)
   cd selenium-automation-test-SIPS