import pytest
from pages.menu_navbar import MenuNavbar
from pages.surat_keluar_page import SuratKeluarPage


@pytest.fixture
def sekretaris_surat_keluar_page(login_as, base_url, driver, sekretaris_creds):
    username, password = sekretaris_creds
    login_as(username, password)
    menu = MenuNavbar(driver, base_url)
    menu.open_surat_keluar()
    return SuratKeluarPage(driver, base_url)


@pytest.fixture
def surat_keluar_data_sekretaris():
    return {
        "no_surat": "SURAT-keluar-XYZ-2713",
        "file_paraf": r"C:\Users\USER\Pictures\Screenshots\Screenshot (11).png"
    }


@pytest.mark.sekretaris_badan
@pytest.mark.surat_keluar
class TestSekretarisSuratKeluar:
    def test_edit(self, sekretaris_surat_keluar_page, surat_keluar_data_sekretaris):
        page = sekretaris_surat_keluar_page
        data = surat_keluar_data_sekretaris
        
        page.search_user(data["no_surat"])
        assert page.is_user_exists(data["no_surat"])
        
        page.edit_surat_keluar(
            no_surat_search=data["no_surat"],
            paraf=data["file_paraf"]
        )
    
    def test_print(self, sekretaris_surat_keluar_page, surat_keluar_data_sekretaris):
        page = sekretaris_surat_keluar_page
        data = surat_keluar_data_sekretaris
        
        page.search_user(data["no_surat"])
        page.print_surat(data["no_surat"])
        page.click(page.BTN_KEMBALI_DIALOG)