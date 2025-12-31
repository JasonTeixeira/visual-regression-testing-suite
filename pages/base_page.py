"""
Base page class with common Selenium interactions and Percy integration.
All page objects should inherit from this class.
"""
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging

logger = logging.getLogger(__name__)


class BasePage:
    """Base page with common web automation functionality"""
    
    def __init__(self, driver, timeout=15):
        """
        Initialize base page with WebDriver instance
        
        Args:
            driver: Selenium WebDriver instance
            timeout: Maximum wait time for elements (default 15s)
        """
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)
        
    def find_element(self, locator):
        """
        Find element with explicit wait
        
        Args:
            locator: Tuple of (By.STRATEGY, "locator")
            
        Returns:
            WebElement if found
            
        Raises:
            TimeoutException: If element not found within timeout
        """
        try:
            element = self.wait.until(
                EC.presence_of_element_located(locator)
            )
            logger.debug(f"Found element: {locator}")
            return element
        except TimeoutException:
            logger.error(f"Element not found: {locator}")
            raise
    
    def find_elements(self, locator):
        """
        Find multiple elements with explicit wait
        
        Args:
            locator: Tuple of (By.STRATEGY, "locator")
            
        Returns:
            List of WebElements
        """
        try:
            elements = self.wait.until(
                EC.presence_of_all_elements_located(locator)
            )
            logger.debug(f"Found {len(elements)} elements: {locator}")
            return elements
        except TimeoutException:
            logger.warning(f"No elements found: {locator}")
            return []
    
    def click(self, locator):
        """
        Click element with wait for clickability
        
        Args:
            locator: Tuple of (By.STRATEGY, "locator")
        """
        try:
            element = self.wait.until(
                EC.element_to_be_clickable(locator)
            )
            element.click()
            logger.debug(f"Clicked element: {locator}")
        except TimeoutException:
            logger.error(f"Element not clickable: {locator}")
            raise
    
    def send_keys(self, locator, text, clear_first=True):
        """
        Type text into element
        
        Args:
            locator: Tuple of (By.STRATEGY, "locator")
            text: Text to enter
            clear_first: Whether to clear field first (default True)
        """
        element = self.find_element(locator)
        if clear_first:
            element.clear()
        element.send_keys(text)
        logger.debug(f"Entered text into: {locator}")
    
    def get_text(self, locator):
        """
        Get text content of element
        
        Args:
            locator: Tuple of (By.STRATEGY, "locator")
            
        Returns:
            str: Element text content
        """
        element = self.find_element(locator)
        text = element.text
        logger.debug(f"Got text '{text}' from: {locator}")
        return text
    
    def is_visible(self, locator, timeout=None):
        """
        Check if element is visible
        
        Args:
            locator: Tuple of (By.STRATEGY, "locator")
            timeout: Optional custom timeout
            
        Returns:
            bool: True if visible, False otherwise
        """
        wait_time = timeout if timeout else self.timeout
        try:
            WebDriverWait(self.driver, wait_time).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
    
    def is_present(self, locator, timeout=None):
        """
        Check if element is present in DOM (not necessarily visible)
        
        Args:
            locator: Tuple of (By.STRATEGY, "locator")
            timeout: Optional custom timeout
            
        Returns:
            bool: True if present, False otherwise
        """
        wait_time = timeout if timeout else self.timeout
        try:
            WebDriverWait(self.driver, wait_time).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
    
    def wait_for_element_to_disappear(self, locator, timeout=None):
        """
        Wait for element to disappear from page
        
        Args:
            locator: Tuple of (By.STRATEGY, "locator")
            timeout: Optional custom timeout
        """
        wait_time = timeout if timeout else self.timeout
        try:
            WebDriverWait(self.driver, wait_time).until(
                EC.invisibility_of_element_located(locator)
            )
            logger.debug(f"Element disappeared: {locator}")
        except TimeoutException:
            logger.warning(f"Element still visible after {wait_time}s: {locator}")
            raise
    
    def scroll_to_element(self, locator):
        """
        Scroll element into view
        
        Args:
            locator: Tuple of (By.STRATEGY, "locator")
        """
        element = self.find_element(locator)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});",
            element
        )
        logger.debug(f"Scrolled to element: {locator}")
    
    def wait_for_page_load(self):
        """Wait for page to be fully loaded"""
        # Wait for document ready state
        self.wait.until(
            lambda driver: driver.execute_script("return document.readyState") == "complete"
        )
        logger.debug("Page fully loaded")
    
    def wait_for_ajax(self, timeout=10):
        """
        Wait for AJAX calls to complete (jQuery)
        
        Args:
            timeout: Maximum wait time
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: driver.execute_script("return jQuery.active == 0")
            )
            logger.debug("AJAX calls completed")
        except Exception:
            # jQuery might not be present
            logger.debug("jQuery not available or no AJAX calls")
            pass
    
    def take_screenshot(self, name):
        """
        Take screenshot and save to file
        
        Args:
            name: Filename for screenshot (without extension)
            
        Returns:
            str: Path to saved screenshot
        """
        filepath = f"screenshots/{name}.png"
        self.driver.save_screenshot(filepath)
        logger.info(f"Screenshot saved: {filepath}")
        return filepath
    
    def get_current_url(self):
        """
        Get current page URL
        
        Returns:
            str: Current URL
        """
        return self.driver.current_url
    
    def refresh_page(self):
        """Refresh current page"""
        self.driver.refresh()
        self.wait_for_page_load()
        logger.debug("Page refreshed")
