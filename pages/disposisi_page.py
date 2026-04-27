from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from datetime import datetime
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class DisposisiPage(BasePage):
    BTN_TAMBAH_DISPOSISI = (By.XPATH, "//a[contains(@href, '/disposisi/create')]//span[contains(text(), 'Tambah')]")
    BTN_KEMBALI_KE_SURAT_MASUK = (By.XPATH, "//a[contains(@href, '/surat/masuk')]//span[contains(text(), 'Kembali')]")
    
    SEARCH_INPUT = (By.XPATH, "//form[contains(@class, 'flex gap-2')]//input[@placeholder='Search']")
    DROPDOWN_SEARCH_BY = (By.XPATH, "//div[contains(@class, 'p-dropdown') and contains(@class, 'p-inputwrapper')]")
    DROPDOWN_SEARCH_PANEL = (By.XPATH, "//div[contains(@class, 'p-dropdown-panel')]//ul[contains(@class, 'p-dropdown-items')]")
    
    SEARCH_OPTIONS = {
        "tujuan": (By.XPATH, "//li[@role='option' and @aria-label='tujuan']"),
        "isi_disposisi": (By.XPATH, "//li[@role='option' and @aria-label='isi_disposisi']"),
        "catatan": (By.XPATH, "//li[@role='option' and @aria-label='catatan']"),
        "batas_waktu": (By.XPATH, "//li[@role='option' and @aria-label='batas_waktu']"),
        "sifat": (By.XPATH, "//li[@role='option' and @aria-label='sifat']")
    }
    
    BTN_DETAIL_DISPOSISI = (By.XPATH, ".//button[contains(@class, 'p-button-info')]//span[contains(@class, 'pi-file')]/ancestor::button")
    BTN_EDIT_DISPOSISI = (By.XPATH, ".//button[contains(@class, 'p-button-help')]//span[contains(@class, 'pi-file-edit')]/ancestor::button")
    BTN_DELETE_DISPOSISI = (By.XPATH, ".//button[contains(@class, 'p-button-warning')]//span[contains(@class, 'pi-trash')]/ancestor::button")
    
    DIALOG_DELETE = (By.XPATH, "//div[@role='dialog' and .//span[contains(text(), 'Delete')]]")
    BTN_HAPUS_FINAL = (By.XPATH, "//button[.//span[normalize-space()='Hapus']]")
    
    INPUT_TUJUAN = (By.ID, "input-tambah-disposisi-tujuan-disposisi")
    INPUT_TUJUAN_DETAIL = (By.ID, "input-detail-disposisi-tujuan-disposisi")
    DROPDOWN_SIFAT = (By.XPATH, "//label[contains(text(), 'Sifat')]/following::div[@data-pc-name='dropdown'][1]")
    DROPDOWN_SIFAT_PANEL = (By.XPATH, "//div[contains(@class, 'p-dropdown-panel')]")
    
    SIFAT_OPTIONS = {
        "Biasa": (By.XPATH, "//li[@role='option' and @aria-label='Biasa']"),
        "Segera": (By.XPATH, "//li[@role='option' and @aria-label='Segera']"),
        "Perlu Perhatian Khusus": (By.XPATH, "//li[@role='option' and @aria-label='Perlu Perhatian Khusus']"),
        "Perhatian Batas Waktu": (By.XPATH, "//li[@role='option' and @aria-label='Perhatian Batas Waktu']")
    }
    
    TEXTAREA_ISI = (By.XPATH, "//label[contains(text(), 'Isi Disposisi')]/following::textarea[1]")
    TEXTAREA_CATATAN = (By.XPATH, "//label[contains(text(), 'Catatan')]/following::textarea[1]")
    CALENDAR_WRAPPER = (By.XPATH, "//span[contains(@class, 'p-calendar')]")
    INPUT_BATAS_WAKTU = (By.XPATH, "//label[contains(text(), 'Batas Waktu')]/following::input[@type='text']")
    BTN_CALENDAR = (By.XPATH, "//button[contains(@class, 'p-datepicker-trigger')]")
    DATEPICKER_PANEL = (By.XPATH, "//div[contains(@class,'p-datepicker') and contains(@class,'p-component')]")
    
    BTN_SIMPAN = (By.XPATH, "//button[@type='submit' and contains(@aria-label, 'Simpan')]")
    BTN_KEMBALI_FORM = (By.XPATH, "//button[.//span[normalize-space(text())='Kembali']]")
    BTN_KEMBALI_DETAIL = (By.XPATH, "//button[@type='button' and contains(@aria-label, 'Kembali')]")
    
    MONTHS_ID = {
        1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
        7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"
    }

    LOADER_OVERLAY = (By.CSS_SELECTOR, ".p-datatable-loading-overlay")
    
    def click_tambah_disposisi(self):
        self.click(self.BTN_TAMBAH_DISPOSISI, scroll=True)
        self.wait_for_element(self.INPUT_TUJUAN)
        return self
    
    def click_kembali_ke_surat_masuk(self):
        self.click(self.BTN_KEMBALI_KE_SURAT_MASUK, scroll=True)
        return self
    
    def select_search_by(self, search_by: str):
        if search_by not in self.SEARCH_OPTIONS:
            raise ValueError(f"Search by '{search_by}' tidak valid")
        
        self.click(self.DROPDOWN_SEARCH_BY, scroll=True)
        self.wait_for_element(self.DROPDOWN_SEARCH_PANEL)
        self.click(self.SEARCH_OPTIONS[search_by], use_js=True)
        return self
    
    def search_disposisi(self, keyword: str, search_by: str = "tujuan"):
        self.select_search_by(search_by)
        self.input_text(self.SEARCH_INPUT, keyword, clear_first=True)
        return self
    
    def get_row_by_text(self, text: str):
        xpath = f"//tbody/tr[.//descendant::*[contains(normalize-space(), '{text}')]]"
        return self.wait_for_element((By.XPATH, xpath), timeout=self.MEDIUM_TIMEOUT)
    
    def click_detail_disposisi(self, text: str):
        self.wait_for_invisibility(self.LOADER_OVERLAY, timeout=7)
        row = self.get_row_by_text(text)
        btn_detail = row.find_element(*self.BTN_DETAIL_DISPOSISI)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn_detail)
        btn_detail.click()
        self.wait_for_element(self.INPUT_TUJUAN_DETAIL)
        
        return self
    
    def click_edit_disposisi(self, text: str):
        row = self.get_row_by_text(text)
        btn_edit = row.find_element(*self.BTN_EDIT_DISPOSISI)
        self.driver.execute_script("arguments[0].click();", btn_edit)
        self.wait_for_element(self.INPUT_TUJUAN)
        return self
    
    def click_delete_disposisi(self, text: str):
        row = self.get_row_by_text(text)
        btn_delete = row.find_element(*self.BTN_DELETE_DISPOSISI)
        self.driver.execute_script("arguments[0].click();", btn_delete)
        return self
    
    def confirm_delete(self):
        self.wait_for_element(self.DIALOG_DELETE)
        self.click(self.BTN_HAPUS_FINAL)
        self.wait_for_invisibility(self.DIALOG_DELETE)
        return self
    
    def is_disposisi_exists(self, text: str) -> bool:
        try:
            self.get_row_by_text(text)
            return True
        except:
            return False
    
    def verify_on_disposisi_page(self) -> bool:
        return self.is_element_visible(self.SEARCH_INPUT, timeout=self.MEDIUM_TIMEOUT)
    
    def input_tujuan(self, tujuan: str):
        self.input_text(self.INPUT_TUJUAN, tujuan, clear_first=True)
        return self
    
    def select_sifat(self, sifat: str):
        if sifat not in self.SIFAT_OPTIONS:
            raise ValueError(f"Sifat '{sifat}' tidak valid")
        
        dropdown = self.wait_for_element(self.DROPDOWN_SIFAT, timeout=self.MEDIUM_TIMEOUT)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dropdown)
        
        for attempt in range(self.RETRY_COUNT):
            try:
                self.driver.execute_script("arguments[0].click();", dropdown)
                self.wait_for_element(self.DROPDOWN_SIFAT_PANEL, timeout=self.MEDIUM_TIMEOUT)
                break
            except Exception:
                if attempt == self.RETRY_COUNT - 1:
                    raise
                logger.warning(f"Retry select_sifat, attempt {attempt + 1}")
        
        self.click(self.SIFAT_OPTIONS[sifat], use_js=True)
        return self
    
    def input_isi(self, isi: str):
        self.input_text(self.TEXTAREA_ISI, isi, clear_first=True)
        return self
    
    def input_catatan(self, catatan: str):
        self.input_text(self.TEXTAREA_CATATAN, catatan, clear_first=True)
        return self
    
    def select_batas_waktu(self, tgl_batas: str):
        input_batas = self.wait_for_element(self.INPUT_BATAS_WAKTU, timeout=self.MEDIUM_TIMEOUT)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", input_batas)
        self.driver.execute_script("arguments[0].click();", input_batas)
        
        self.wait_for_element(self.DATEPICKER_PANEL)
        
        dt = datetime.strptime(tgl_batas, "%d/%m/%Y")
        month_str = self.MONTHS_ID[dt.month]
        
        year_btn = self.wait_for_element((By.CLASS_NAME, "p-datepicker-year"), timeout=self.MEDIUM_TIMEOUT)
        self.driver.execute_script("arguments[0].click();", year_btn)
        
        xpath_year = f"//*[contains(@class, 'p-yearpicker-year') and normalize-space()='{dt.year}']"
        self.click((By.XPATH, xpath_year), use_js=True)
        
        xpath_month = f"//*[contains(@class, 'p-monthpicker-month') and normalize-space()='{month_str}']"
        self.click((By.XPATH, xpath_month), use_js=True)
        
        xpath_day = f"//td[not(contains(@class,'p-datepicker-other-month'))]//span[normalize-space()='{dt.day}']"
        self.click((By.XPATH, xpath_day), use_js=True)
        
        return self
    
    def click_simpan(self):
        self.click(self.BTN_SIMPAN, scroll=True, use_js=True)
        self.wait_for_element(self.BTN_EDIT_DISPOSISI)
        return self
    
    def click_kembali_dari_detail(self):
        self.click(self.BTN_KEMBALI_DETAIL, scroll=True)
        return self
    
    def click_kembali_dari_form(self):
        self.click(self.BTN_KEMBALI_FORM, scroll=True)
        return self
    
    def create_disposisi(self, tujuan: str, sifat: str, isi: str, catatan: str, batas_waktu: str):
        self.input_tujuan(tujuan)
        self.select_sifat(sifat)
        self.input_isi(isi)
        self.input_catatan(catatan)
        self.select_batas_waktu(batas_waktu)
        self.click_simpan()
        return self
    
    def update_disposisi(
        self,
        tujuan: Optional[str] = None,
        sifat: Optional[str] = None,
        isi: Optional[str] = None,
        catatan: Optional[str] = None,
        batas_waktu: Optional[str] = None
    ):
        self.wait_for_element(self.INPUT_TUJUAN)
        
        if tujuan:
            self.input_tujuan(tujuan)
        if sifat:
            self.select_sifat(sifat)
        if isi:
            self.input_isi(isi)
        if catatan:
            self.input_catatan(catatan)
        if batas_waktu:
            self.select_batas_waktu(batas_waktu)
        
        self.click_simpan()
        return self
    
    def verify_on_create_page(self) -> bool:
        return self.is_element_visible(self.INPUT_TUJUAN, timeout=self.MEDIUM_TIMEOUT)