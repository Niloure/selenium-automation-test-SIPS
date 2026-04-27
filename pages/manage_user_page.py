from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class MasterAdmin(BasePage):
    BTN_TAMBAH = (By.XPATH, "//button[.//span[contains(normalize-space(), 'Tambah')]]")
    BTN_SIMPAN = (By.XPATH, "//button[.//span[contains(normalize-space(), 'Simpan')]]")
    BTN_KEMBALI = (By.XPATH, "//button[.//span[contains(normalize-space(), 'Kembali')]]")
    
    INPUT_USERNAME = (By.ID, "input-create-user-username")
    INPUT_EMAIL = (By.ID, "input-create-user-email")
    INPUT_PASSWORD = (By.ID, "input-create-user-password")
    INPUT_VALIDATION_PASSWORD = (By.ID, "input-create-user-konfirmasi-password")
    
    SELECT_LEVEL = (By.XPATH, "//div[@data-pc-name='dropdown' and not(contains(@class,'p-disabled'))]//span[@data-pc-section='input']")
    DROPDOWN_PANEL = (By.XPATH, "//div[contains(@class,'p-dropdown-panel')]")
    
    ROWS_PER_PAGE_DROPDOWN = (By.XPATH, "//div[contains(@class,'p-paginator-rpp-options')]")
    ROWS_PER_PAGE_PANEL = (By.XPATH, "//div[contains(@class,'p-dropdown-panel')]")
    
    BTN_DETAIL = (By.XPATH, ".//a[contains(@href,'/user/detail/')]")
    BTN_EDIT = (By.XPATH, ".//a[contains(@href,'/user/edit/')]")
    BTN_DELETE = (By.XPATH, ".//button[contains(@class,'p-button-warning')]")
    
    DIALOG_DELETE = (By.XPATH, "//div[contains(@class,'p-dialog') and .//span[text()='Delete']]")
    BTN_HAPUS_DIALOG = (By.XPATH, "//div[contains(@class,'p-dialog') and .//span[text()='Delete']]//button[.//span[text()='Hapus']]")
    BTN_KEMBALI_DIALOG = (By.XPATH, "//div[contains(@class,'p-dialog') and .//span[text()='Delete']]//button[.//span[text()='Kembali']]")
    
    BUTTON_SEARCH_BY = (By.XPATH, "//input[@placeholder='Search']/ancestor::form//div[contains(@class,'p-dropdown')]")
    SEARCH_INPUT = (By.XPATH, "//input[@placeholder='Search']")
    
    INPUT_NAMA_ID_TEMPLATE = "input-{}-user-nama"
    INPUT_NIP_ID_TEMPLATE = "input-{}-user-nip"
    
    def _get_nama_input(self, mode: str):
        return (By.ID, self.INPUT_NAMA_ID_TEMPLATE.format(mode))
    
    def _get_nip_input(self, mode: str):
        return (By.ID, self.INPUT_NIP_ID_TEMPLATE.format(mode))
    
    def click_tambah(self) -> None:
        self.click(self.BTN_TAMBAH, scroll=True)
        self.wait_for_element(self.INPUT_USERNAME)
    
    def select_level(self, level_name: str) -> None:
        self.click(self.SELECT_LEVEL, scroll=True)
        self.wait_for_element(self.DROPDOWN_PANEL)
        
        option_locator = (By.XPATH, f"//div[contains(@class,'p-dropdown-panel')]//li[normalize-space()='{level_name}']")
        self.click(option_locator, use_js=True)
    
    def set_search_by(self, value: str) -> None:
        dropdown = self.wait_for_element(self.BUTTON_SEARCH_BY, timeout=self.MEDIUM_TIMEOUT)
        
        if "p-disabled" in dropdown.get_attribute("class"):
            return
        
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", dropdown)
        dropdown.click()
        
        option_locator = (By.XPATH, f"//li[@role='option' and normalize-space()='{value}']")
        self.click(option_locator, use_js=True)
    
    def search_user(self, keyword: str, search_by: Optional[str] = None) -> None:
        if search_by:
            self.set_search_by(search_by)
        
        self.input_text(self.SEARCH_INPUT, keyword, clear_first=True)
    
    def get_row_by_email(self, email: str):
        xpath = f"//tbody/tr[.//td[normalize-space()='{email}']]"
        return self.wait_for_element((By.XPATH, xpath), timeout=self.MEDIUM_TIMEOUT)
    
    def open_detail(self, email: str) -> None:
        row = self.get_row_by_email(email)
        row.find_element(*self.BTN_DETAIL).click()
        self.wait_for_element(self._get_nama_input("detail"))
    
    def open_edit(self, email: str) -> None:
        row = self.get_row_by_email(email)
        row.find_element(*self.BTN_EDIT).click()
        self.wait_for_element(self._get_nama_input("create"))
    
    def create_user(
        self,
        username: str,
        email: str,
        nama: str,
        nip: str,
        password: str,
        konfirmasi_password: str,
        level_name: str
    ) -> None:
        self.wait_for_element(self.INPUT_USERNAME)
        
        self.input_text(self.INPUT_USERNAME, username)
        self.input_text(self.INPUT_EMAIL, email)
        self.input_text(self._get_nama_input("create"), nama)
        self.input_text(self._get_nip_input("create"), nip)
        self.input_text(self.INPUT_PASSWORD, password)
        self.input_text(self.INPUT_VALIDATION_PASSWORD, konfirmasi_password)
        
        self.select_level(level_name)
        
        self.click(self.BTN_SIMPAN)
        self.wait_for_element(self.BTN_TAMBAH)
    
    def edit_user(self, nama: str, nip: str, level_name: str) -> None:
        self.wait_for_element(self._get_nama_input("create"))
        
        self.input_text(self._get_nama_input("create"), nama, clear_first=True)
        self.input_text(self._get_nip_input("create"), nip, clear_first=True)
        
        self.select_level(level_name)
        
        self.click(self.BTN_SIMPAN)
    
    def delete_user(self, email: str) -> None:
        row = self.get_row_by_email(email)
        row.find_element(*self.BTN_DELETE).click()
        
        self.wait_for_element(self.DIALOG_DELETE)
        self.click(self.BTN_HAPUS_DIALOG)
        self.wait_for_invisibility(self.DIALOG_DELETE)
    
    def is_user_exists(self, email: str) -> bool:
        try:
            xpath = f"//tbody/tr[.//td[normalize-space()='{email}']]"
            self.wait_for_element((By.XPATH, xpath), timeout=self.MEDIUM_TIMEOUT)
            return True
        except:
            return False