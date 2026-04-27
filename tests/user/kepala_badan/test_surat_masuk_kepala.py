import pytest
from pages.menu_navbar import MenuNavbar
from pages.surat_masuk_page import SuratMasukPage


@pytest.fixture
def kepala_surat_masuk_page(login_as, base_url, driver, kepala_badan_creds):
    username, password = kepala_badan_creds
    login_as(username, password)
    menu = MenuNavbar(driver, base_url)
    menu.open_surat_masuk()
    return SuratMasukPage(driver, base_url)


@pytest.fixture(scope="session")
def surat_masuk_data_kepala():
    return {
        "no_surat": "SURAT-MASUK-2ad1c9",
        "no_agenda": "892866"
    }


@pytest.mark.kepala_badan
@pytest.mark.surat_masuk
class TestKepalaSuratMasuk:
    def test_detail(self, kepala_surat_masuk_page, surat_masuk_data_kepala):
        page = kepala_surat_masuk_page
        data = surat_masuk_data_kepala
        
        page.search_user(data["no_surat"])
        page.open_detail(data["no_surat"])
        page.click(page.BTN_KEMBALI)
    
    def test_disposisi(self, kepala_surat_masuk_page, surat_masuk_data_kepala):
        page = kepala_surat_masuk_page
        data = surat_masuk_data_kepala
        
        page.search_user(data["no_agenda"])
        page.open_disposisi()
        page.wait_for_element(page.BTN_KEMBALI)
        page.click(page.BTN_KEMBALI)
    
    def test_print(self, kepala_surat_masuk_page, surat_masuk_data_kepala):
        page = kepala_surat_masuk_page
        data = surat_masuk_data_kepala
        
        page.search_user(data["no_agenda"])
        page.print_surat(data["no_agenda"])
        page.click(page.BTN_KEMBALI_DIALOG)