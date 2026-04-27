import uuid
import pytest
import random
from pages.menu_navbar import MenuNavbar
from pages.manage_user_page import MasterAdmin


@pytest.fixture(scope="session")
def user_data():
    unique_id = uuid.uuid4().hex[:6]
    return {
        "username": f"user_{unique_id}",
        "email": f"user_{unique_id}@mail.com",
        "nama": f"User {unique_id}",
        "nama_edit": f"User Edit {unique_id}",
        "nip": str(random.randint(1000, 9999)),
        "nip_edit": str(random.randint(10000, 99999)),
        "password": "Password123!",
        "konfirmasi_password": "Password123!",
        "level": "Admin",
        "level_edit": "Admin"
    }


@pytest.fixture
def master_admin_user_page(login_as, base_url, driver, master_admin_creds):
    username, password = master_admin_creds
    login_as(username, password)
    menu = MenuNavbar(driver, base_url)
    menu.open_manage_user()
    return MasterAdmin(driver, base_url)


@pytest.mark.master_admin
@pytest.mark.manage_user
class TestMasterAdminManageUser:
    def test_create(self, master_admin_user_page, user_data):
        page = master_admin_user_page
        data = user_data
        
        page.click_tambah()
        page.create_user(
            username=data["username"],
            email=data["email"],
            nama=data["nama"],
            nip=data["nip"],
            password=data["password"],
            konfirmasi_password=data["konfirmasi_password"],
            level_name=data["level"]
        )
        page.search_user(data["nama"], search_by="nama")
        
        assert page.is_user_exists(data["email"])
    
    def test_detail(self, master_admin_user_page, user_data):
        page = master_admin_user_page
        data = user_data
        
        page.search_user(data["email"], search_by="email")
        page.open_detail(data["email"])
        page.click(page.BTN_KEMBALI)
    
    def test_edit(self, master_admin_user_page, user_data):
        page = master_admin_user_page
        data = user_data
        
        page.search_user(data["nip"], search_by="nip")
        page.open_edit(data["email"])
        page.edit_user(data["nama_edit"], data["nip_edit"], data["level_edit"])
        page.search_user(data["email"], search_by="email")
        
        assert page.is_user_exists(data["email"])
    
    def test_delete(self, master_admin_user_page, user_data):
        page = master_admin_user_page
        data = user_data
        
        page.search_user(data["email"], search_by="email")
        page.delete_user(data["email"])
        page.search_user(data["email"], search_by="email")
        
        assert not page.is_user_exists(data["email"])