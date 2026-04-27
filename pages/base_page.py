from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from typing import List, Tuple, Optional, Union, Callable
from selenium.webdriver.common.by import By
import logging

logger = logging.getLogger(__name__)


class BasePage:
    DEFAULT_TIMEOUT = 10
    MEDIUM_TIMEOUT = 5
    FAST_TIMEOUT = 3
    RETRY_COUNT = 3
    
    def __init__(self, driver, base_url: str):
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(driver, self.DEFAULT_TIMEOUT)
        self.medium_wait = WebDriverWait(driver, self.MEDIUM_TIMEOUT)
        self.fast_wait = WebDriverWait(driver, self.FAST_TIMEOUT)
        
    def _get_wait(self, timeout: Optional[int] = None) -> WebDriverWait:
        if timeout is not None:
            return WebDriverWait(self.driver, timeout)
        return self.wait
    
    def wait_for_element(
        self,
        locator: Tuple[By, str],
        timeout: Optional[int] = None,
        condition: str = "visible"
    ) -> WebElement:
        wait = self._get_wait(timeout)
        
        if condition == "clickable":
            return wait.until(EC.element_to_be_clickable(locator))
        elif condition == "present":
            return wait.until(EC.presence_of_element_located(locator))
        else:
            return wait.until(EC.visibility_of_element_located(locator))
    
    def wait_for_elements(
        self,
        locator: Tuple[By, str],
        timeout: Optional[int] = None
    ) -> List[WebElement]:
        wait = self._get_wait(timeout)
        return wait.until(EC.presence_of_all_elements_located(locator))
    
    def wait_for_invisibility(
        self,
        locator: Tuple[By, str],
        timeout: Optional[int] = None
    ) -> bool:
        wait = self._get_wait(timeout)
        return wait.until(EC.invisibility_of_element_located(locator))
    
    def wait_for_url_contains(self, text: str, timeout: Optional[int] = None) -> None:
        wait = self._get_wait(timeout)
        wait.until(lambda driver: text in driver.current_url)
    
    def wait_for_url_not_contains(self, text: str, timeout: Optional[int] = None) -> None:
        wait = self._get_wait(timeout)
        wait.until(lambda driver: text not in driver.current_url)
    
    def click(
        self,
        locator: Tuple[By, str],
        scroll: bool = True,
        use_js: bool = False,
        timeout: Optional[int] = None
    ) -> None:
        for attempt in range(self.RETRY_COUNT):
            try:
                element = self.wait_for_element(locator, timeout, "clickable")
                
                if scroll:
                    self.driver.execute_script(
                        "arguments[0].scrollIntoView({block: 'center', behavior: 'instant'});",
                        element
                    )
                    self.wait_for_element(locator, timeout, "clickable")
                
                if use_js:
                    self.driver.execute_script("arguments[0].click();", element)
                else:
                    element.click()
                
                logger.debug(f"Clicked element: {locator}")
                return
                
            except (TimeoutException, StaleElementReferenceException) as e:
                if attempt == self.RETRY_COUNT - 1:
                    logger.error(f"Failed to click element {locator}: {e}")
                    raise
                logger.warning(f"Retry clicking {locator}, attempt {attempt + 1}")
    
    def input_text(
        self,
        locator: Tuple[By, str],
        text: str,
        clear_first: bool = True,
        timeout: Optional[int] = None
    ) -> None:
        for attempt in range(self.RETRY_COUNT):
            try:
                element = self.wait_for_element(locator, timeout, "visible")
                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center'});",
                    element
                )
                
                if clear_first:
                    element.clear()
                
                element.send_keys(text)
                logger.debug(f"Input text into {locator}: {text[:50]}...")
                return
                
            except (TimeoutException, StaleElementReferenceException) as e:
                if attempt == self.RETRY_COUNT - 1:
                    logger.error(f"Failed to input text to {locator}: {e}")
                    raise
                logger.warning(f"Retry input to {locator}, attempt {attempt + 1}")
    
    def get_text(
        self,
        locator: Tuple[By, str],
        timeout: Optional[int] = None
    ) -> str:
        element = self.wait_for_element(locator, timeout, "visible")
        return element.text.strip()
    
    def get_attribute(
        self,
        locator: Tuple[By, str],
        attribute: str,
        timeout: Optional[int] = None
    ) -> str:
        element = self.wait_for_element(locator, timeout, "present")
        return element.get_attribute(attribute)
    
    def scroll_to(self, locator: Tuple[By, str], timeout: Optional[int] = None) -> WebElement:
        element = self.wait_for_element(locator, timeout, "present")
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});",
            element
        )
        return element
    
    def find_element(
        self,
        locator: Tuple[By, str],
        timeout: Optional[int] = None
    ) -> WebElement:
        return self.wait_for_element(locator, timeout, "present")
    
    def is_element_present(
        self,
        locator: Tuple[By, str],
        timeout: Optional[int] = None
    ) -> bool:
        try:
            self.wait_for_element(locator, timeout, "present")
            return True
        except TimeoutException:
            return False
    
    def is_element_visible(
        self,
        locator: Tuple[By, str],
        timeout: Optional[int] = None
    ) -> bool:
        try:
            self.wait_for_element(locator, timeout, "visible")
            return True
        except TimeoutException:
            return False
    
    def select_dropdown_option(
        self,
        dropdown_locator: Tuple[By, str],
        option_text: str,
        wait_for_panel: Optional[Tuple[By, str]] = None
    ) -> None:
        self.click(dropdown_locator, scroll=True)
        
        if wait_for_panel:
            self.wait_for_element(wait_for_panel, timeout=self.MEDIUM_TIMEOUT)
        
        option_xpath = (
            By.XPATH,
            f"//li[contains(@class, 'p-dropdown-item')]//span[contains(text(), '{option_text}')] | "
            f"//li[contains(@class, 'p-dropdown-item') and normalize-space()='{option_text}']"
        )
        self.click(option_xpath, scroll=False, use_js=True)
    
    def get_row_by_text(
        self,
        text: str,
        timeout: Optional[int] = None
    ) -> WebElement:
        xpath = f"//tbody/tr[.//descendant::*[contains(normalize-space(), '{text}')]]"
        return self.wait_for_element((By.XPATH, xpath), timeout, "present")
    
    def is_text_exists(
        self,
        text: str,
        timeout: Optional[int] = None
    ) -> bool:
        try:
            wait = self._get_wait(timeout or self.FAST_TIMEOUT)
            xpath = f"//*[contains(normalize-space(), '{text}')]"
            wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            return True
        except TimeoutException:
            return False
    
    def safe_execute(
        self,
        action: Callable,
        error_message: str = "Action failed",
        retries: int = RETRY_COUNT
    ) -> Optional[any]:
        for attempt in range(retries):
            try:
                return action()
            except Exception as e:
                if attempt == retries - 1:
                    logger.error(f"{error_message}: {e}")
                    raise
                logger.warning(f"Retry {error_message}, attempt {attempt + 1}")
        return None