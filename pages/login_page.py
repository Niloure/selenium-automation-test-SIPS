from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class LoginPage(BasePage):
    LOGIN_PATH = "/login"

    USERNAME = (By.ID, "input-login-username")
    PASSWORD = (By.ID, "input-login-password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    ERROR_MESSAGE = (By.CLASS_NAME, "p-inline-message-text")

    def open(self) -> None:
        self.driver.get(self.base_url + self.LOGIN_PATH)

    def login(self, username: str = "", password: str = "") -> None:
        if username:
            self.input_text(self.USERNAME, username)
        if password:
            self.input_text(self.PASSWORD, password)
        
        self.click(self.LOGIN_BUTTON)

    def is_login_failed(self) -> bool:
        return "/login" in self.driver.current_url
    
    def is_login_successful(self) -> bool:
        return "/login" not in self.driver.current_url
    
    def wait_for_login_complete(self) -> None:
        self.wait.until(lambda driver: "/login" not in driver.current_url)