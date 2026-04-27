from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class DashboardPage(BasePage):
    DASHBOARD_TITLE = (By.XPATH, "//h1[normalize-space()='Dashboard']")
    USER_BUTTON = (By.XPATH, "//button[contains(@class, 'p-button-secondary')]//span[contains(@class, 'p-button-label')]")
    LOGOUT_MENU = (By.XPATH, "//li[.//span[normalize-space()='Logout']]")
    LOGIN_URL_PART = "/login"
    
    MENU_LOCATORS = {
        "Manage User": (By.XPATH, "//span[normalize-space()='Manage User']"),
        "Catatan Surat": (By.XPATH, "//li[@aria-label='Catat Surat']"),
        "Klasifikasi Surat": (By.XPATH, "//span[normalize-space()='Klasifikasi Surat']"),
        "Buku Agenda": (By.XPATH, "//li[@aria-label='Buku Agenda']"),
    }
    
    def wait_until_loaded(self):
        self.wait_for_element(self.DASHBOARD_TITLE)
    
    def wait_loaded(self):
        self.wait_until_loaded()
    
    def get_user_role(self) -> str:
        element = self.wait_for_element(self.USER_BUTTON)
        return element.text.strip()
    
    def open_user_menu(self):
        self.click(self.USER_BUTTON, scroll=True)
        self.wait_for_element(self.LOGOUT_MENU)
    
    def logout(self):
        self.open_user_menu()
        self.click(self.LOGOUT_MENU)
        self.wait_for_url_contains(self.LOGIN_URL_PART)
    
    def is_redirected_to_login(self) -> bool:
        self.wait_for_url_contains(self.LOGIN_URL_PART)
        return self.LOGIN_URL_PART in self.driver.current_url
    
    def is_menu_visible(self, menu_text: str) -> bool:
        if menu_text not in self.MENU_LOCATORS:
            return False
        
        locator = self.MENU_LOCATORS[menu_text]
        return self.is_element_visible(locator, timeout=self.MEDIUM_TIMEOUT)
    
    def is_manage_user_visible(self) -> bool:
        return self.is_menu_visible("Manage User")