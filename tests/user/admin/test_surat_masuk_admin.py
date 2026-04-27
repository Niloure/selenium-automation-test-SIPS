import uuid
import pytest
import random
from pages.menu_navbar import MenuNavbar
from pages.surat_masuk_page import SuratMasukPage


@pytest.fixture(scope="session")
def surat_masuk_data():
    return {
        "no_agenda": str(random.randint(20, 999999)),
        "kode_klasifikasi": "2",
        "kode_klasifikasi_edit": "1",
        "asal_surat": "luar",
        "asal_surat_edit": "dalam",
        "tgl_surat": "12/08/2025",
        "tgl_surat_edit": "17/06/2025",
        "no_surat": f"SURAT-MASUK-{uuid.uuid4().hex[:6]}",
        "no_surat_edit": f"SURAT-MASUK-EDIT-{uuid.uuid4().hex[:6]}",
        "file_path": r"D:\Download\Jadwal_Lari_2_Minggu_Dengan_Laporan.xlsx",
        "file_path_edit": r"C:\Users\USER\Downloads\Pertemuan 1_Dasar_Sistem_Pakar.pdf",
        "ringkas": "Ringkasan awal surat masuk",
        "ringkas_edit": "Ringkasan edit surat masuk",
        "ket": "Keterangan awal",
        "ket_edit": "Keterangan edit"
    }


@pytest.fixture
def admin_surat_masuk_page(login_as, base_url, driver, admin_creds):
    username, password = admin_creds
    login_as(username, password)
    menu = MenuNavbar(driver, base_url)
    menu.open_surat_masuk()
    return SuratMasukPage(driver, base_url)


@pytest.mark.admin
@pytest.mark.surat_masuk
class TestAdminSuratMasuk:
    def test_create(self, admin_surat_masuk_page, surat_masuk_data):
        page = admin_surat_masuk_page
        data = surat_masuk_data
        
        page.click_tambah()
        page.create_surat_masuk(
            data["no_agenda"],
            data["kode_klasifikasi"],
            data["asal_surat"],
            data["tgl_surat"],
            data["no_surat"],
            data["file_path"],
            data["ringkas"],
            data["ket"],
            double_click_choose=True
        )
        page.search_user(data["no_surat"])
        
        assert page.is_user_exists(data["no_surat"])
    
    def test_detail(self, admin_surat_masuk_page, surat_masuk_data):
        page = admin_surat_masuk_page
        data = surat_masuk_data
        
        page.search_user(data["no_surat"])
        page.open_detail(data["no_surat"])
        page.click(page.BTN_KEMBALI)
    
    def test_edit(self, admin_surat_masuk_page, surat_masuk_data):
        page = admin_surat_masuk_page
        data = surat_masuk_data
        
        page.search_user(data["no_surat"])
        page.edit_surat_masuk(
            no_surat_search=data["no_surat"],
            kode_klasifikasi=data["kode_klasifikasi_edit"],
            asal_surat=data["asal_surat_edit"],
            tgl_surat=data["tgl_surat_edit"],
            no_surat=data["no_surat_edit"],
            file_path=data["file_path_edit"],
            ringkas=data["ringkas_edit"],
            ket=data["ket_edit"]
        )
        page.search_user(data["no_agenda"])
        
        assert page.is_user_exists(data["no_agenda"])
    
    def test_print(self, admin_surat_masuk_page, surat_masuk_data):
        page = admin_surat_masuk_page
        data = surat_masuk_data
        
        page.search_user(data["no_agenda"])
        page.print_surat(data["no_agenda"])
        page.click(page.BTN_KEMBALI_DIALOG)
    
    def test_delete(self, admin_surat_masuk_page, surat_masuk_data):
        page = admin_surat_masuk_page
        data = surat_masuk_data
        
        page.search_user(data["no_agenda"])
        page.hapus_surat(data["no_agenda"])
        page.search_user(data["no_agenda"])
        
        assert not page.is_user_exists(data["no_agenda"])