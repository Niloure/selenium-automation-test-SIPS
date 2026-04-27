from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from datetime import datetime
import os
from typing import Optional
import logging
import time
from pathlib import Path

logger = logging.getLogger(__name__)


class SuratMasukPage(BasePage):
    BTN_TAMBAH = (By.XPATH, "//button[.//span[contains(normalize-space(), 'Tambah')]]")
    BTN_SIMPAN = (By.XPATH, "//button[.//span[contains(normalize-space(), 'Simpan')]]")
    BTN_KEMBALI = (By.XPATH, "//button[.//span[contains(normalize-space(), 'Kembali')]]")
    
    INPUT_NO_AGENDA = (By.ID, "input-detail-surat_masuk-no_agenda")
    SELECT_KODE_KLASIFIKASI = (By.ID, "input-detail-surat_masuk-kode_klasifikasi")
    DROPDOWN_PANEL = (By.XPATH, "//ul[@id='input-detail-surat_masuk-kode_klasifikasi_list']")
    INPUT_ASAL_SURAT = (By.ID, "input-detail-surat_masuk-asal_surat")
    INPUT_TGL_SURAT = (By.ID, "input-detail-surat_masuk-tgl_surat")
    DATEPICKER_PANEL = (By.XPATH, "//div[contains(@class,'p-datepicker') and contains(@class,'p-component')]")
    INPUT_NO_SURAT = (By.ID, "input-detail-surat_masuk-no_surat")
    INPUT_RINGKAS = (By.ID, "input-detail-surat_masuk-isi_ringkas")
    INPUT_KETERANGAN = (By.ID, "input-detail-surat_masuk-keterangan")
    
    SELECT_FILE = (By.XPATH, "//div[@id='input-detail-surat_masuk-file_surat']//input[@type='file']")
    BTN_CHOOSE_FILE = (By.XPATH, "//div[@id='input-detail-surat_masuk-file_surat']//span[contains(@class, 'p-fileupload-choose')]")
    
    SEARCH_INPUT = (By.XPATH, "//input[@placeholder='Search']")
    
    BTN_DETAIL = (By.XPATH, ".//button[contains(@class, 'p-button-help')]//span[contains(@class, 'pi-search')]")
    BTN_EDIT = (By.XPATH, ".//button[contains(@class, 'p-button-success')]//span[contains(@class, 'pi-pencil')]")
    BTN_DELETE = (By.XPATH, ".//button[contains(@class, 'p-button-warning')]//span[contains(@class, 'pi-trash')]")
    BTN_PRINT = (By.XPATH, ".//button[contains(@class, 'p-button-info')]//span[contains(@class, 'pi-print')]")
    BTN_DISPOSISI = (By.XPATH, "//button[contains(@class, 'p-button-secondary')]//span[contains(@class, 'pi-file-o')]/ancestor::button")
    
    DIALOG_PRINT = (By.XPATH, "//div[@role='dialog' and .//span[contains(text(), 'Print')]]")
    DIALOG_DELETE = (By.XPATH, "//div[@role='dialog' and .//span[contains(text(), 'Delete')]]")
    BTN_CETAK_FINAL = (By.XPATH, "//div[@role='dialog']//button[@aria-label='Cetak']")
    BTN_HAPUS_FINAL = (By.XPATH, "//div[@role='dialog']//button[@aria-label='Hapus']")
    BTN_KEMBALI_DIALOG = (By.XPATH, "//div[@role='dialog']//button[@aria-label='Kembali']")
    
    LEMBARAN_SURAT_PRINT = (By.XPATH, "//p[contains(text(), 'Lembar Disposisi')]")
    
    MONTHS_ID = {
        1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
        7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"
    }
    
    def click_tambah(self) -> None:
        self.click(self.BTN_TAMBAH, scroll=True)
        self.wait_for_element(self.INPUT_NO_AGENDA)
    
    def search_user(self, keyword: str) -> None:
        self.input_text(self.SEARCH_INPUT, keyword, clear_first=True)
    
    def select_kode_klasifikasi(self, kode_klasifikasi: str) -> None:
        dropdown = self.wait_for_element(self.SELECT_KODE_KLASIFIKASI, condition="clickable")
        self.driver.execute_script("arguments[0].scrollIntoView(true);", dropdown)
        dropdown.click()
        
        self.wait_for_element(self.DROPDOWN_PANEL)
        
        option_xpath = (By.XPATH, f"//li[contains(@class, 'p-dropdown-item')]//span[contains(text(), '{kode_klasifikasi}')] | //li[contains(@class, 'p-dropdown-item') and normalize-space()='{kode_klasifikasi}']")
        self.click(option_xpath, use_js=True)
    
    def select_tanggal_surat(self, tgl_surat: str) -> None:
        self.click(self.INPUT_TGL_SURAT, scroll=True)
        self.wait_for_element(self.DATEPICKER_PANEL)
        
        dt = datetime.strptime(tgl_surat, "%d/%m/%Y")
        month_str = self.MONTHS_ID[dt.month]
        
        btn_year = self.wait_for_element((By.CLASS_NAME, "p-datepicker-year"), timeout=self.MEDIUM_TIMEOUT)
        self.driver.execute_script("arguments[0].click();", btn_year)
        
        xpath_year = f"//*[contains(@class, 'p-yearpicker-year') and normalize-space()='{dt.year}']"
        self.click((By.XPATH, xpath_year), use_js=True)
        
        xpath_month = f"//*[contains(@class, 'p-monthpicker-month') and normalize-space()='{month_str}']"
        self.click((By.XPATH, xpath_month), use_js=True)
        
        xpath_day = f"//td[not(contains(@class,'p-datepicker-other-month'))]//span[normalize-space()='{dt.day}']"
        self.click((By.XPATH, xpath_day), use_js=True)
        
    
    def upload_file_surat(self, file_path: str) -> None:
        input_file = self.wait_for_element(self.SELECT_FILE, condition="present")
        input_file.send_keys(file_path)
        logger.info(f"Uploaded file {os.path.basename(file_path)}")
    
    def open_detail(self, no_surat: str) -> None:
        row = self.get_row_by_text(no_surat)
        row.find_element(*self.BTN_DETAIL).click()
        self.wait_for_element(self.INPUT_ASAL_SURAT)
    
    def open_edit(self, no_surat: str) -> None:
        row = self.get_row_by_text(no_surat)
        row.find_element(*self.BTN_EDIT).click()
        self.wait_for_element(self.INPUT_ASAL_SURAT)
    
    def open_print(self, no_agenda: str) -> None:
        row = self.get_row_by_text(no_agenda)
        row.find_element(*self.BTN_PRINT).click()
        self.wait_for_element(self.DIALOG_PRINT)
    
    def open_disposisi(self) -> None:
        btn_disposisi = self.wait_for_element(self.BTN_DISPOSISI, condition="clickable")
        self.driver.execute_script("arguments[0].click();", btn_disposisi)
    
    def get_row_by_text(self, text: str):
        xpath = f"//tbody/tr[.//descendant::*[normalize-space()='{text}']]"
        return self.wait_for_element((By.XPATH, xpath))
    
    def is_user_exists(self, text: str) -> bool:
        try:
            xpath = f"//tbody/tr[.//descendant::*[normalize-space()='{text}']]"
            self.wait_for_element((By.XPATH, xpath), timeout=self.MEDIUM_TIMEOUT)
            return True
        except:
            return False
    
    def create_surat_masuk(
        self,
        no_agenda: str,
        kode_klasifikasi: str,
        asal_surat: str,
        tgl_surat: str,
        no_surat: str,
        file_path: str,
        ringkas: str,
        ket: str,
        double_click_choose: bool = True
    ) -> None:
        self.wait_for_element(self.INPUT_NO_AGENDA)
        
        self.input_text(self.INPUT_NO_AGENDA, no_agenda)
        self.input_text(self.INPUT_ASAL_SURAT, asal_surat)
        self.input_text(self.INPUT_NO_SURAT, no_surat)
        self.input_text(self.INPUT_RINGKAS, ringkas)
        self.input_text(self.INPUT_KETERANGAN, ket)
        
        self.select_kode_klasifikasi(kode_klasifikasi)
        self.select_tanggal_surat(tgl_surat)
        self.upload_file_surat(file_path)
        
        if double_click_choose:
            toggle_file = self.wait_for_element(self.BTN_CHOOSE_FILE, condition="clickable")
            toggle_file.click()
        
        btn_simpan = self.wait_for_element(self.BTN_SIMPAN, condition="clickable")
        self.driver.execute_script("arguments[0].click();", btn_simpan)
        
        self.wait_for_element(self.BTN_TAMBAH)
    
    def edit_surat_masuk(
        self,
        no_surat_search: str,
        kode_klasifikasi: Optional[str] = None,
        asal_surat: Optional[str] = None,
        tgl_surat: Optional[str] = None,
        no_surat: Optional[str] = None,
        file_path: Optional[str] = None,
        ringkas: Optional[str] = None,
        ket: Optional[str] = None
    ) -> None:
        self.open_edit(no_surat_search)
        
        if asal_surat:
            self.input_text(self.INPUT_ASAL_SURAT, asal_surat, clear_first=True)
        
        if no_surat:
            self.input_text(self.INPUT_NO_SURAT, no_surat, clear_first=True)
        
        if ringkas:
            self.input_text(self.INPUT_RINGKAS, ringkas, clear_first=True)
        
        if ket:
            self.input_text(self.INPUT_KETERANGAN, ket, clear_first=True)
        
        if kode_klasifikasi:
            self.select_kode_klasifikasi(kode_klasifikasi)
        
        if tgl_surat:
            self.select_tanggal_surat(tgl_surat)
        
        if file_path:
            self.upload_file_surat(file_path)
            toggle = self.wait_for_element(self.BTN_CHOOSE_FILE, condition="clickable")
            toggle.click()
        
        self.click(self.BTN_SIMPAN)
        self.click(self.BTN_KEMBALI)
        
        self.wait_for_element(self.BTN_TAMBAH)
    
    def hapus_surat(self, no_agenda: str) -> None:
        row = self.get_row_by_text(no_agenda)
        row.find_element(*self.BTN_DELETE).click()
        
        self.wait_for_element(self.DIALOG_DELETE)
        self.click(self.BTN_HAPUS_FINAL)
        self.wait_for_invisibility(self.DIALOG_DELETE)

    def print_surat(self, no_agenda: str, download_dir: str = None) -> None:
        if download_dir is None:
            download_dir = str(Path.home() / "Downloads")
        
        row = self.get_row_by_text(no_agenda)
        row.find_element(*self.BTN_PRINT).click()
        
        self.wait_for_element(self.LEMBARAN_SURAT_PRINT)
        self.wait_for_element(self.DIALOG_PRINT)
        
        btn_cetak = self.wait_for_element(self.BTN_CETAK_FINAL, condition="clickable")
        
        files_before = set(os.listdir(download_dir))
        btn_cetak.click()
        
        self.wait.until(lambda driver: len(set(os.listdir(download_dir)) - files_before) > 0)
        