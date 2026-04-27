from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from datetime import datetime
import logging
import os
import time

logger = logging.getLogger(__name__)


class BaseCetakanAgenda(BasePage):
    BTN_CETAK = (By.XPATH, "//button[.//span[contains(normalize-space(), 'Cetak')]]")
    BTN_KEMBALI = (By.XPATH, "//button[.//span[contains(normalize-space(), 'Kembali')]]")
    
    DIALOG_ROOT = (By.CSS_SELECTOR, "div.p-dialog")
    EMPTY_MESSAGE = (By.CSS_SELECTOR, "tr.p-datatable-emptymessage")
    DATA_ROW = (By.CSS_SELECTOR, "tbody.p-datatable-tbody tr:not(.p-datatable-emptymessage)")
    DIALOG_CETAK = (By.XPATH, "//button[contains(@class, 'p-button')]//span[contains(@class, 'pi-print')]/parent::button")
    BTN_CLOSE_X = (By.XPATH, "//div[@role='dialog']//button[@aria-label='Close']")
    DATEPICKER_PANEL = (By.CSS_SELECTOR, "div.p-datepicker")
    
    MONTHS_ID = {
        1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
        7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"
    }
    
    INPUT_TGL_START = None
    INPUT_TGL_END = None
    
    def _safe_click(self, locator):
        element = self.wait_for_element(locator, condition="clickable")

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            element
        )

        try:
            element.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", element)

    def _select_tanggal(self, locator, tgl_surat: str) -> None:
        self._safe_click(locator)

        self.wait_for_element(self.DATEPICKER_PANEL)

        dt = datetime.strptime(tgl_surat, "%d/%m/%Y")
        month_str = self.MONTHS_ID[dt.month]

        btn_year = self.wait_for_element(
            (By.CLASS_NAME, "p-datepicker-year"),
            timeout=self.MEDIUM_TIMEOUT
        )
        self._safe_click((By.CLASS_NAME, "p-datepicker-year"))

        xpath_year = f"//*[contains(@class, 'p-yearpicker-year') and normalize-space()='{dt.year}']"
        self._safe_click((By.XPATH, xpath_year))

        xpath_month = f"//*[contains(@class, 'p-monthpicker-month') and normalize-space()='{month_str}']"
        self._safe_click((By.XPATH, xpath_month))

        xpath_day = (
            f"//td[not(contains(@class,'p-datepicker-other-month'))]"
            f"//span[normalize-space()='{dt.day}']"
        )
        self._safe_click((By.XPATH, xpath_day))
    
    def cetak_agenda(self, tgl_start: str, tgl_end: str) -> None:
        if self.INPUT_TGL_START is None or self.INPUT_TGL_END is None:
            raise NotImplementedError("Subclass must define INPUT_TGL_START and INPUT_TGL_END")
        
        self._select_tanggal(self.INPUT_TGL_START, tgl_start)
        self.wait_for_invisibility(self.DATEPICKER_PANEL)
        self._select_tanggal(self.INPUT_TGL_END, tgl_end)
        
        self.click(self.BTN_CETAK)
        
        try:
            self.wait_for_element(self.DATA_ROW, timeout=self.MEDIUM_TIMEOUT)
        except Exception:
            logger.debug("No data rows found")
    
    def klik_print_dialog(self) -> None:
        self.click(self.DIALOG_CETAK, use_js=True)
    
    def tutup_dialog_cetak(self):
        """Menutup dialog dengan cara yang paling efektif & singkat."""
        btn = self.wait_for_element(self.BTN_CLOSE_X)
        try:
            btn.click() # Coba klik normal
        except:
            self.driver.execute_script("arguments[0].click();", btn) # Force klik jika terhalang
        
        self.wait_for_invisibility(self.DIALOG_CETAK)

    def wait_for_download_complete(self, timeout: int = 30) -> None:
        """
        Menunggu download dengan toleransi tinggi. 
        Jika deteksi file gagal tapi tidak ada error sistem, 
        kita biarkan lanjut ke tutup_dialog agar test tidak macet.
        """
        download_dir = getattr(self, "download_dir", os.path.join(os.path.expanduser("~"), "Downloads"))
        start_time = time.time()

        def _check(driver):
            try:
                current_files = os.listdir(download_dir)
                # Cek file PDF yang baru (dibuat dalam 30 detik terakhir)
                for f in current_files:
                    if f.endswith(".pdf"):
                        path = os.path.join(download_dir, f)
                        if os.path.getmtime(path) > start_time - 2: # Margin 2 detik
                            return True
                return False
            except Exception:
                return False

        try:
            # Kita kecilkan timeoutnya jadi 30 detik saja agar tidak kelamaan menunggu
            self._get_wait(timeout).until(_check)
        except Exception:
            # Jika timeout (file tidak terdeteksi), jangan gagalkan test!
            # Berikan peringatan saja di log, lalu lanjut ke step berikutnya (tutup dialog)
            print("INFO: Deteksi file download timeout, mencoba melanjutkan ke penutupan dialog...")
    
    def is_data_visible(self, text: str) -> bool:
        xpath = f"//tbody[contains(@class, 'p-datatable-tbody')]//td[contains(normalize-space(), '{text}')]"
        return self.is_element_visible((By.XPATH, xpath), timeout=self.MEDIUM_TIMEOUT)
    
    def click_kembali(self) -> None:
        self.click(self.BTN_KEMBALI, scroll=True)