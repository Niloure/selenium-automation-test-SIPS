from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class MenuNavbar(BasePage):
    MENU_CATATAN_SURAT = (By.XPATH, "//li[@aria-label='Catat Surat']")
    MENU_SURAT_MASUK = (By.XPATH, "//li[@aria-label='Catat Surat']//a[@href='/surat/masuk']")
    MENU_SURAT_KELUAR = (By.XPATH, "//li[@aria-label='Catat Surat']//a[@href='/surat/keluar']")
    MENU_KLASIFIKASI_SURAT = (By.XPATH, "//span[normalize-space()='Klasifikasi Surat']")
    MENU_MANAGE_USER = (By.XPATH, "//span[normalize-space()='Manage User']")
    MENU_BUKU_AGENDA = (By.XPATH, "//li[@aria-label='Buku Agenda']")
    MENU_CK_SURAT_MASUK = (By.XPATH, "//li[@aria-label='Cetak Agenda Surat Masuk']//a[@href='/cetakagenda/masuk']")
    MENU_CK_SURAT_KELUAR = (By.XPATH, "//li[@aria-label='Cetak Agenda Surat Keluar']//a[@href='/cetakagenda/keluar']")
    
    def _open_submenu(self, parent_locator, child_locator) -> None:
        self.click(parent_locator, scroll=True)
        self.click(child_locator, scroll=True)
    
    def open_surat_masuk(self) -> None:
        self._open_submenu(self.MENU_CATATAN_SURAT, self.MENU_SURAT_MASUK)
    
    def open_surat_keluar(self) -> None:
        self._open_submenu(self.MENU_CATATAN_SURAT, self.MENU_SURAT_KELUAR)
    
    def open_klasifikasi_surat(self) -> None:
        self.click(self.MENU_KLASIFIKASI_SURAT, scroll=True)
    
    def open_manage_user(self) -> None:
        self.click(self.MENU_MANAGE_USER, scroll=True)
    
    def open_agenda_surat_keluar(self) -> None:
        self._open_submenu(self.MENU_BUKU_AGENDA, self.MENU_CK_SURAT_KELUAR)
    
    def open_agenda_surat_masuk(self) -> None:
        self._open_submenu(self.MENU_BUKU_AGENDA, self.MENU_CK_SURAT_MASUK)
    
    def is_menu_visible(self, menu_locator) -> bool:
        return self.is_element_visible(menu_locator, timeout=self.FAST_TIMEOUT)