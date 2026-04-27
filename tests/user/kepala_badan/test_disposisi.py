import pytest
import uuid
import random
from datetime import datetime, timedelta
from pages.menu_navbar import MenuNavbar
from pages.surat_masuk_page import SuratMasukPage
from pages.disposisi_page import DisposisiPage


@pytest.fixture(scope="session")
def disposisi_data():
    batas_waktu = (datetime.now() + timedelta(days=30)).strftime("%d/%m/%Y")
    batas_waktu_edit = (datetime.now() + timedelta(days=60)).strftime("%d/%m/%Y")
    return {
        "tujuan": f"Tujuan Disposisi {uuid.uuid4().hex[:4]}",
        "tujuan_edit": f"Tujuan Edit {uuid.uuid4().hex[:4]}",
        "sifat": "Biasa",
        "sifat_edit": "Segera",
        "isi": f"Isi disposisi {uuid.uuid4().hex[:6]}",
        "isi_edit": f"Isi disposisi edit {uuid.uuid4().hex[:6]}",
        "catatan": f"Catatan disposisi {uuid.uuid4().hex[:4]}",
        "catatan_edit": f"Catatan edit {uuid.uuid4().hex[:4]}",
        "batas_waktu": batas_waktu,
        "batas_waktu_edit": batas_waktu_edit
    }


@pytest.fixture
def kepala_disposisi_page(login_as, base_url, driver, kepala_badan_creds):
    username, password = kepala_badan_creds
    login_as(username, password)
    menu = MenuNavbar(driver, base_url)
    menu.open_surat_masuk()
    
    surat_page = SuratMasukPage(driver, base_url)
    surat_page.search_user("892866")
    surat_page.open_disposisi()
    
    disposisi_page = DisposisiPage(driver, base_url)
    disposisi_page.wait_for_element(disposisi_page.SEARCH_INPUT, timeout=10)
    
    return disposisi_page


@pytest.mark.kepala_badan
@pytest.mark.disposisi
class TestKepalaDisposisi:
    def test_create(self, kepala_disposisi_page, disposisi_data):
        page = kepala_disposisi_page
        data = disposisi_data
        
        page.click_tambah_disposisi()
        page.create_disposisi(
            data["tujuan"],
            data["sifat"],
            data["isi"],
            data["catatan"],
            data["batas_waktu"]
        )
        page.search_disposisi(data["tujuan"], "tujuan")
        
        assert page.is_disposisi_exists(data["tujuan"])
    
    def test_detail(self, kepala_disposisi_page, disposisi_data):
        page = kepala_disposisi_page
        data = disposisi_data
        
        # 1. Cari dan Klik Detail
        page.search_disposisi(data["tujuan"], "tujuan")
        page.click_detail_disposisi(data["tujuan"])
        
        # 2. ASSERTION: Cek apakah elemen detail tujuan muncul dan teksnya benar
        # Kita tunggu sampai locator detail muncul di layar
        detail_element = page.wait_for_element(page.INPUT_TUJUAN_DETAIL)
        
        # Ambil nilai dari input (biasanya pakai get_attribute('value') untuk input read-only)
        actual_text = detail_element.get_attribute("value") 
        
        assert actual_text == data["tujuan"], f"Ekspektasi: {data['tujuan']}, tapi muncul: {actual_text}"
        
        # 3. Kembali
        page.click_kembali_dari_detail()
    
    def test_edit(self, kepala_disposisi_page, disposisi_data):
        page = kepala_disposisi_page
        data = disposisi_data
        
        page.search_disposisi(data["tujuan"], "tujuan")
        page.click_edit_disposisi(data["tujuan"])
        page.wait_for_element(page.INPUT_TUJUAN)
        
        page.update_disposisi(
            tujuan=data["tujuan_edit"],
            sifat=data["sifat_edit"],
            isi=data["isi_edit"],
            catatan=data["catatan_edit"],
            batas_waktu=data["batas_waktu_edit"]
        )
        
        page.search_disposisi(data["tujuan_edit"], "tujuan")
        assert page.is_disposisi_exists(data["tujuan_edit"])
    
    def test_delete(self, kepala_disposisi_page, disposisi_data):
        page = kepala_disposisi_page
        data = disposisi_data
        
        page.search_disposisi(data["tujuan_edit"], "tujuan")
        assert page.is_disposisi_exists(data["tujuan_edit"])
        
        page.click_delete_disposisi(data["tujuan_edit"])
        page.confirm_delete()
        
        page.search_disposisi(data["tujuan_edit"], "tujuan")
        assert not page.is_disposisi_exists(data["tujuan_edit"])
    
    def test_kembali_ke_surat_masuk(self, kepala_disposisi_page):
        page = kepala_disposisi_page
        
        page.wait_for_element(page.BTN_KEMBALI_KE_SURAT_MASUK)
        page.click_kembali_ke_surat_masuk()