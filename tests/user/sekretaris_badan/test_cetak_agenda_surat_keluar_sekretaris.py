import pytest
from pages.menu_navbar import MenuNavbar
from pages.cetak_agenda_surat_keluar import CetakanAgendaKeluar


@pytest.fixture
def agenda_keluar_page(login_as, base_url, driver, sekretaris_creds):
    username, password = sekretaris_creds
    login_as(username, password)
    menu = MenuNavbar(driver, base_url)
    menu.open_agenda_surat_keluar()
    return CetakanAgendaKeluar(driver, base_url)


@pytest.fixture(scope="session")
def agenda_keluar_data():
    return {
        "tgl_start_ada_data": "12/02/2026",
        "tgl_end_ada_data": "12/03/2026",
        "tgl_start_tidak_ada_data": "20/03/2025",
        "tgl_end_tidak_ada_data": "30/03/2025"
    }


@pytest.mark.sekretaris_badan
@pytest.mark.cetak_agenda
class TestCetakAgendaKeluar:
    def test_dengan_data(self, agenda_keluar_page, agenda_keluar_data):
        page = agenda_keluar_page
        data = agenda_keluar_data

        page.cetak_agenda(
            data["tgl_start_ada_data"],
            data["tgl_end_ada_data"]
        )

        assert not page.is_data_visible("Data tidak ditemukan")

        page.wait_for_element(page.DIALOG_CETAK)
        page.klik_print_dialog()
        page.wait_for_download_complete()
        page.tutup_dialog_cetak()
        assert page.wait_for_invisibility(page.DIALOG_CETAK)
    
    def test_tanpa_data(self, agenda_keluar_page, agenda_keluar_data):
        page = agenda_keluar_page
        data = agenda_keluar_data
        
        page.cetak_agenda(data["tgl_start_tidak_ada_data"], data["tgl_end_tidak_ada_data"])
        assert page.is_data_visible("Data tidak ditemukan")
        page.klik_print_dialog()
        page.wait_for_download_complete()
        page.tutup_dialog_cetak()
        assert page.wait_for_invisibility(page.DIALOG_CETAK)