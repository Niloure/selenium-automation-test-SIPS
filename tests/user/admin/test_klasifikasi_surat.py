import uuid
import pytest
import random
from pages.menu_navbar import MenuNavbar
from pages.klasifikasi_page import AdminKlasifikasi


@pytest.fixture(scope="session")
def klasifikasi_data():
    random_num = random.randint(1000, 9999)
    return {
        "kode": str(random_num),
        "kode_edit": str(random.randint(5000, 9999)),
        "nama": f"Klasifikasi-{uuid.uuid4().hex[:6]}",
        "nama_edit": f"Klasifikasi-Edit-{uuid.uuid4().hex[:6]}",
        "uraian": f"Uraian awal klasifikasi {random_num}",
        "uraian_edit": f"Uraian setelah diedit {random_num}"
    }


@pytest.fixture
def admin_klasifikasi_page(login_as, base_url, driver, admin_creds):
    username, password = admin_creds
    login_as(username, password)
    menu = MenuNavbar(driver, base_url)
    menu.open_klasifikasi_surat()
    return AdminKlasifikasi(driver, base_url)


@pytest.mark.admin
@pytest.mark.klasifikasi
class TestAdminKlasifikasi:
    def test_create(self, admin_klasifikasi_page, klasifikasi_data):
        page = admin_klasifikasi_page
        data = klasifikasi_data
        
        page.click_tambah()
        page.create_klasifikasi_surat(data["kode"], data["nama"], data["uraian"])
        page.search_user(data["nama"])
        
        assert page.is_user_exists(data["nama"])
    
    def test_detail(self, admin_klasifikasi_page, klasifikasi_data):
        page = admin_klasifikasi_page
        data = klasifikasi_data
        
        page.search_user(data["nama"])
        page.open_detail(data["nama"])
        page.click(page.BTN_KEMBALI)
    
    def test_edit(self, admin_klasifikasi_page, klasifikasi_data):
        page = admin_klasifikasi_page
        data = klasifikasi_data
        
        page.search_user(data["nama"])
        page.open_edit(data["nama"])
        page.edit_klasifikasi_surat(data["nama_edit"], data["uraian_edit"])
        page.search_user(data["nama_edit"])
        
        assert page.is_user_exists(data["nama_edit"])
    
    def test_delete(self, admin_klasifikasi_page, klasifikasi_data):
        page = admin_klasifikasi_page
        data = klasifikasi_data
        
        page.search_user(data["nama_edit"])
        page.delete_klasifikasi_surat(data["nama_edit"])
        page.search_user(data["nama_edit"])
        
        assert not page.is_user_exists(data["nama_edit"])