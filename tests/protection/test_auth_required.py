import pytest
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


@pytest.mark.protection
@pytest.mark.auth
class TestAuthRequired:
    def test_dashboard_requires_login(self, driver, base_url):
        driver.get(base_url + "/")
        
        menus = driver.find_elements(By.CSS_SELECTOR, ".p-menuitem-text")
        menu_texts = [menu.text for menu in menus]
        
        assert "Manage User" not in menu_texts
    
    def test_surat_masuk_requires_login(self, driver, base_url):
        base = BasePage(driver, base_url)
        driver.get(base_url + "/surat/masuk")
        
        base.wait_for_url_contains("/login")
        
        assert "/login" in driver.current_url
    
    def test_surat_keluar_requires_login(self, driver, base_url):
        base = BasePage(driver, base_url)
        driver.get(base_url + "/surat/keluar")
        
        base.wait_for_url_contains("/login")
        
        assert "/login" in driver.current_url
    
    def test_user_page_requires_login(self, driver, base_url):
        base = BasePage(driver, base_url)
        driver.get(base_url + "/user")
        
        base.wait_for_url_contains("/login")
        
        assert "/login" in driver.current_url