import pytest
from pages.menu_navbar import MenuNavbar
from pages.surat_keluar_page import SuratKeluarPage


@pytest.fixture
def kepala_surat_keluar_page(login_as, base_url, driver, kepala_badan_creds):
    username, password = kepala_badan_creds
    login_as(username, password)
    menu = MenuNavbar(driver, base_url)
    menu.open_surat_keluar()
    return SuratKeluarPage(driver, base_url)


@pytest.fixture
def surat_keluar_data_kepala():
    return {
        "no_surat": "SURAT-keluar-XYZ-2712",
        "file_ttd": r"C:\Users\USER\Pictures\Screenshots\Screenshot (11).png"
    }


@pytest.mark.kepala_badan
@pytest.mark.surat_keluar
class TestKepalaSuratKeluar:
    def test_edit(self, kepala_surat_keluar_page, surat_keluar_data_kepala):
        page = kepala_surat_keluar_page
        data = surat_keluar_data_kepala
        
        page.search_user(data["no_surat"])
        assert page.is_user_exists(data["no_surat"])
        
        page.edit_surat_keluar(
            no_surat_search=data["no_surat"],
            ttd=data["file_ttd"]
        )
    
    def test_print(self, kepala_surat_keluar_page, surat_keluar_data_kepala):
        page = kepala_surat_keluar_page
        data = surat_keluar_data_kepala
        
        page.search_user(data["no_surat"])
        page.print_surat(data["no_surat"])
        page.click(page.BTN_KEMBALI_DIALOG)