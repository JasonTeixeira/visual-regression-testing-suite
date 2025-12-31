"""
Homepage page object for visual regression testing.
Handles navigation, interaction, and visual snapshot preparation for the homepage.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
import logging
import time

logger = logging.getLogger(__name__)


class HomePage(BasePage):
    """Page object for the application homepage"""
    
    # Locators
    HERO_BANNER = (By.CSS_SELECTOR, ".hero-banner")
    NAVIGATION_MENU = (By.CSS_SELECTOR, "nav.main-navigation")
    SEARCH_BAR = (By.ID, "site-search")
    SEARCH_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    LOGO = (By.CSS_SELECTOR, ".site-logo")
    FOOTER = (By.CSS_SELECTOR, "footer")
    
    # Dynamic elements to hide for visual testing
    TIMESTAMP = (By.CSS_SELECTOR, ".timestamp")
    LIVE_COUNTER = (By.CSS_SELECTOR, ".live-count")
    ROTATING_BANNER = (By.CSS_SELECTOR, ".rotating-banner")
    ANIMATED_ELEMENTS = (By.CSS_SELECTOR, "[data-animate='true']")
    
    def __init__(self, driver, base_url="https://www.example.com"):
        """
        Initialize homepage with driver and base URL
        
        Args:
            driver: Selenium WebDriver instance
            base_url: Base URL of the application
        """
        super().__init__(driver)
        self.base_url = base_url
        self.url = base_url
    
    def navigate(self):
        """Navigate to homepage"""
        logger.info(f"Navigating to homepage: {self.url}")
        self.driver.get(self.url)
        self.wait_for_page_load()
    
    def wait_for_homepage_load(self):
        """
        Wait for homepage-specific elements to load completely
        This ensures visual tests capture the fully rendered page
        """
        logger.debug("Waiting for homepage to load completely")
        
        # Wait for hero banner
        self.wait.until(
            EC.visibility_of_element_located(self.HERO_BANNER)
        )
        
        # Wait for navigation
        self.wait.until(
            EC.visibility_of_element_located(self.NAVIGATION_MENU)
        )
        
        # Wait for all images to load
        self.wait_for_images_to_load()
        
        # Wait for custom fonts to load
        self.wait_for_fonts_to_load()
        
        # Small buffer to ensure animations settle
        time.sleep(0.5)
        
        logger.debug("Homepage fully loaded")
    
    def wait_for_images_to_load(self):
        """Wait for all images on page to finish loading"""
        logger.debug("Waiting for images to load")
        
        # Use JavaScript to check if all images are loaded
        images_loaded = self.driver.execute_script("""
            return Array.from(document.images).every(img => img.complete && img.naturalHeight !== 0);
        """)
        
        if not images_loaded:
            # Wait up to 10 seconds for images
            for _ in range(20):
                images_loaded = self.driver.execute_script("""
                    return Array.from(document.images).every(img => img.complete);
                """)
                if images_loaded:
                    break
                time.sleep(0.5)
        
        logger.debug("All images loaded")
    
    def wait_for_fonts_to_load(self):
        """Wait for web fonts to load to avoid FOUT (Flash of Unstyled Text)"""
        logger.debug("Waiting for fonts to load")
        
        try:
            # Check if document.fonts API is available
            fonts_loaded = self.driver.execute_script("""
                if (document.fonts && document.fonts.ready) {
                    return document.fonts.ready.then(() => true);
                }
                return true;
            """)
            
            # Wait for fonts with timeout
            self.wait.until(
                lambda driver: driver.execute_script(
                    "return document.fonts ? document.fonts.status === 'loaded' : true"
                )
            )
            logger.debug("Fonts loaded")
        except Exception as e:
            logger.warning(f"Could not verify font loading: {e}")
            # Continue anyway - not all browsers support document.fonts
    
    def hide_dynamic_elements(self):
        """
        Hide elements that change frequently to prevent false positives in visual tests
        This is crucial for stable visual regression testing
        """
        logger.debug("Hiding dynamic elements for visual testing")
        
        # Use JavaScript to hide dynamic elements
        hide_script = """
        // Hide timestamps
        document.querySelectorAll('.timestamp, [data-timestamp]').forEach(el => {
            el.style.display = 'none';
        });
        
        // Hide live counters
        document.querySelectorAll('.live-count, .real-time-counter').forEach(el => {
            el.style.display = 'none';
        });
        
        // Stop and hide rotating banners
        document.querySelectorAll('.rotating-banner, .carousel-auto').forEach(el => {
            el.style.animation = 'none';
            el.style.transition = 'none';
        });
        
        // Stop all animations and transitions globally
        const style = document.createElement('style');
        style.innerHTML = `
            *, *::before, *::after {
                animation-duration: 0s !important;
                transition-duration: 0s !important;
            }
        `;
        document.head.appendChild(style);
        
        // Hide elements marked with data-dynamic attribute
        document.querySelectorAll('[data-dynamic="true"]').forEach(el => {
            el.style.display = 'none';
        });
        """
        
        self.driver.execute_script(hide_script)
        logger.debug("Dynamic elements hidden")
    
    def prepare_for_visual_snapshot(self):
        """
        Prepare page for visual snapshot by ensuring stability
        Call this before taking Percy snapshots
        """
        logger.info("Preparing homepage for visual snapshot")
        
        # Ensure page is fully loaded
        self.wait_for_homepage_load()
        
        # Hide dynamic elements
        self.hide_dynamic_elements()
        
        # Scroll to top to ensure consistent starting point
        self.scroll_to_top()
        
        # Small delay to ensure everything is stable
        time.sleep(0.3)
        
        logger.info("Homepage ready for visual snapshot")
    
    def scroll_to_top(self):
        """Scroll page to top"""
        self.driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(0.2)  # Small delay for smooth scroll to complete
    
    def scroll_to_footer(self):
        """Scroll to page footer"""
        footer = self.find_element(self.FOOTER)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({behavior: 'smooth', block: 'end'});",
            footer
        )
        time.sleep(0.5)  # Wait for scroll to complete
    
    def search(self, query):
        """
        Perform search from homepage
        
        Args:
            query: Search term to enter
        """
        logger.info(f"Searching for: {query}")
        self.send_keys(self.SEARCH_BAR, query)
        self.click(self.SEARCH_BUTTON)
        self.wait_for_page_load()
    
    def is_loaded(self):
        """
        Check if homepage is loaded
        
        Returns:
            bool: True if homepage is loaded, False otherwise
        """
        try:
            return (
                self.is_visible(self.HERO_BANNER, timeout=5) and
                self.is_visible(self.NAVIGATION_MENU, timeout=5)
            )
        except Exception:
            return False
    
    def get_hero_text(self):
        """
        Get text from hero banner
        
        Returns:
            str: Hero banner text
        """
        return self.get_text(self.HERO_BANNER)
    
    def click_logo(self):
        """Click site logo (usually returns to homepage)"""
        logger.info("Clicking site logo")
        self.click(self.LOGO)
        self.wait_for_page_load()
