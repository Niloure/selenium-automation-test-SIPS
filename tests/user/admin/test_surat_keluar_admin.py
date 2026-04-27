import uuid
import pytest
import random
from pages.menu_navbar import MenuNavbar
from pages.surat_keluar_page import SuratKeluarPage


@pytest.fixture(scope="session")
def surat_keluar_data():
    return {
        "no_agenda": str(random.randint(20, 999999)),
        "no_surat": f"SURAT-KELUAR-{uuid.uuid4().hex[:6]}",
        "kode_klasifikasi": "2",
        "tujuan_surat": "luar",
        "tgl_surat": "12/08/2025",
        "file_path": r"D:\Download\Agenda Surat Masuk.pdf",
        "ringkas": "Ringkasan awal",
        "ket": "Keterangan awal",
        "tujuan_surat_edit": "dalam",
        "tgl_surat_edit": "17/06/2025",
        "no_surat_edit": f"SURAT-KELUAR-EDIT-{uuid.uuid4().hex[:6]}",
        "file_path_edit": r"C:\Users\USER\Downloads\Pertemuan 1_Dasar_Sistem_Pakar.pdf",
        "ringkas_edit": "Ringkasan edit",
        "ket_edit": "Keterangan edit"
    }


@pytest.fixture
def admin_surat_keluar_page(login_as, base_url, driver, admin_creds):
    username, password = admin_creds
    login_as(username, password)
    menu = MenuNavbar(driver, base_url)
    menu.open_surat_keluar()
    return SuratKeluarPage(driver, base_url)


@pytest.mark.admin
@pytest.mark.surat_keluar
class TestAdminSuratKeluar:
    def test_create(self, admin_surat_keluar_page, surat_keluar_data):
        page = admin_surat_keluar_page
        data = surat_keluar_data
        
        page.click_tambah()
        page.create_surat_keluar(
            data["no_agenda"],
            data["kode_klasifikasi"],
            data["tujuan_surat"],
            data["tgl_surat"],
            data["no_surat"],
            data["file_path"],
            data["ringkas"],
            data["ket"]
        )
        page.search_user(data["no_surat"])
        
        assert page.is_user_exists(data["no_surat"])
    
    def test_detail(self, admin_surat_keluar_page, surat_keluar_data):
        page = admin_surat_keluar_page
        data = surat_keluar_data
        
        page.search_user(data["no_surat"])
        page.open_detail(data["no_surat"])
        page.click(page.BTN_KEMBALI)
    
    def test_edit(self, admin_surat_keluar_page, surat_keluar_data):
        page = admin_surat_keluar_page
        data = surat_keluar_data
        
        page.search_user(data["no_surat"])
        page.edit_surat_keluar(
            no_surat_search=data["no_surat"],
            tujuan_surat=data["tujuan_surat_edit"],
            tgl_surat=data["tgl_surat_edit"],
            no_surat=data["no_surat_edit"],
            file_path=data["file_path_edit"],
            ringkas=data["ringkas_edit"],
            ket=data["ket_edit"]
        )
        page.search_user(data["no_surat_edit"])
        
        assert page.is_user_exists(data["no_surat_edit"])
    
    def test_print(self, admin_surat_keluar_page, surat_keluar_data):
        page = admin_surat_keluar_page
        data = surat_keluar_data
        
        page.search_user(data["no_surat_edit"])
        page.print_surat(data["no_surat_edit"])
        page.click(page.BTN_KEMBALI_DIALOG)
    
    def test_delete(self, admin_surat_keluar_page, surat_keluar_data):
        page = admin_surat_keluar_page
        data = surat_keluar_data
        
        page.search_user(data["no_surat_edit"])
        page.hapus_surat(data["no_surat_edit"])
        page.search_user(data["no_surat_edit"])
        
        assert not page.is_user_exists(data["no_surat_edit"])