import pytest
from pages.login_page import LoginPage

@pytest.mark.negative
@pytest.mark.auth
class TestLoginNegative:
    def test_login_wrong_password(self, driver, base_url, admin_creds):
        """Menggunakan username valid dari env, password salah."""
        login = LoginPage(driver, base_url)
        login.open()
        valid_username, _ = admin_creds
        login.login(valid_username, "wrong_password_123")
        assert login.is_login_failed()
    
    def test_login_wrong_username(self, driver, base_url, admin_creds):
        """Menggunakan password valid dari env, username salah."""
        login = LoginPage(driver, base_url)
        login.open()
        _, valid_password = admin_creds
        login.login("wrong_username", valid_password)
        assert login.is_login_failed()
    
    def test_login_empty_fields(self, driver, base_url):
        login = LoginPage(driver, base_url)
        login.open()
        login.login("", "")
        assert login.is_login_failed()