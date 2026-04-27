from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import logging

logger = logging.getLogger(__name__)


class AdminKlasifikasi(BasePage):
    BTN_TAMBAH = (By.XPATH, "//button[.//span[contains(normalize-space(), 'Tambah')]]")
    BTN_SIMPAN = (By.XPATH, "//button[.//span[contains(normalize-space(), 'Simpan')]]")
    BTN_KEMBALI = (By.XPATH, "//button[.//span[contains(normalize-space(), 'Kembali')]]")
    
    INPUT_KODE = (By.ID, "input-detail-klasifikasi-kode")
    INPUT_NAMA = (By.ID, "input-detail-klasifikasi-nama")
    INPUT_URAIAN = (By.ID, "input-detail-klasifikasi-uraian")
    
    BTN_DETAIL = (By.XPATH, "//button[@aria-label='Detail']")
    BTN_UBAH = (By.XPATH, "//button[@aria-label='Ubah']")
    BTN_HAPUS = (By.XPATH, "//button[@aria-label='Hapus']")
    
    DIALOG_DELETE = (By.XPATH, "//div[contains(@class,'p-dialog') and .//span[contains(@class,'p-dialog-title') and text()='Delete']]")
    BTN_HAPUS_DIALOG = (By.XPATH, "//div[contains(@class,'p-dialog')]//button[@aria-label='Hapus']")
    BTN_KEMBALI_DIALOG = (By.XPATH, "//div[contains(@class,'p-dialog')]//button[@aria-label='Kembali']")
    
    SEARCH_INPUT = (By.XPATH, "//input[@placeholder='Search']")
    
    def click_tambah(self) -> None:
        self.click(self.BTN_TAMBAH, scroll=True)
        self.wait_for_element(self.INPUT_KODE)
    
    def search_user(self, keyword: str) -> None:
        self.input_text(self.SEARCH_INPUT, keyword, clear_first=True)
    
    def get_row_by_text(self, text: str):
        xpath = f"//tbody/tr[.//td[normalize-space()='{text}']]"
        return self.wait_for_element((By.XPATH, xpath), timeout=self.MEDIUM_TIMEOUT)
    
    def open_detail(self, nama: str) -> None:
        row = self.get_row_by_text(nama)
        row.find_element(*self.BTN_DETAIL).click()
        self.wait_for_element(self.INPUT_NAMA)
    
    def open_edit(self, nama: str) -> None:
        row = self.get_row_by_text(nama)
        row.find_element(*self.BTN_UBAH).click()
        self.wait_for_element(self.INPUT_NAMA)
    
    def create_klasifikasi_surat(self, kode: str, nama: str, uraian: str) -> None:
        self.wait_for_element(self.INPUT_KODE)
        
        self.input_text(self.INPUT_KODE, kode)
        self.input_text(self.INPUT_NAMA, nama)
        self.input_text(self.INPUT_URAIAN, uraian)
        
        self.click(self.BTN_SIMPAN)
        self.click(self.BTN_KEMBALI)
        
        self.wait_for_element(self.BTN_TAMBAH)
    
    def edit_klasifikasi_surat(self, nama: str, uraian: str) -> None:
        self.wait_for_element(self.INPUT_NAMA)
        
        self.input_text(self.INPUT_NAMA, nama, clear_first=True)
        self.input_text(self.INPUT_URAIAN, uraian, clear_first=True)
        
        self.click(self.BTN_SIMPAN)
        self.click(self.BTN_KEMBALI)
        
        self.wait_for_element(self.BTN_TAMBAH)
    
    def delete_klasifikasi_surat(self, nama: str) -> None:
        row = self.get_row_by_text(nama)
        row.find_element(*self.BTN_HAPUS).click()
        
        self.wait_for_element(self.DIALOG_DELETE)
        self.click(self.BTN_HAPUS_DIALOG)
        self.wait_for_invisibility(self.DIALOG_DELETE)
    
    def is_user_exists(self, nama: str) -> bool:
        try:
            xpath = f"//tbody/tr[.//td[normalize-space()='{nama}']]"
            self.wait_for_element((By.XPATH, xpath), timeout=self.MEDIUM_TIMEOUT)
            return True
        except:
            return False