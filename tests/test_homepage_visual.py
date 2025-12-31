"""
Visual regression tests for homepage.
These tests use Percy to capture and compare screenshots across different viewports.
"""
import pytest
from percy import percy_snapshot
from pages.home_page import HomePage
import logging

logger = logging.getLogger(__name__)


@pytest.mark.visual
class TestHomepageVisual:
    """Visual regression test suite for homepage"""
    
    def test_homepage_desktop_1920(self, driver, base_url):
        """
        Test homepage visual appearance on large desktop (1920x1080)
        This is the most common desktop resolution
        """
        logger.info("Testing homepage on desktop 1920x1080")
        driver.set_window_size(1920, 1080)
        
        home = HomePage(driver, base_url)
        home.navigate()
        home.prepare_for_visual_snapshot()
        
        # Take Percy snapshot
        percy_snapshot(driver, 'Homepage - Desktop 1920x1080')
        
        # Verify page loaded correctly
        assert home.is_loaded(), "Homepage did not load properly"
    
    def test_homepage_desktop_1366(self, driver, base_url):
        """
        Test homepage on medium desktop (1366x768)
        Second most common desktop resolution
        """
        logger.info("Testing homepage on desktop 1366x768")
        driver.set_window_size(1366, 768)
        
        home = HomePage(driver, base_url)
        home.navigate()
        home.prepare_for_visual_snapshot()
        
        percy_snapshot(driver, 'Homepage - Desktop 1366x768')
        assert home.is_loaded()
    
    def test_homepage_tablet_portrait(self, driver, base_url):
        """
        Test homepage on tablet portrait (768x1024)
        iPad portrait orientation
        """
        logger.info("Testing homepage on tablet portrait 768x1024")
        driver.set_window_size(768, 1024)
        
        home = HomePage(driver, base_url)
        home.navigate()
        home.prepare_for_visual_snapshot()
        
        percy_snapshot(driver, 'Homepage - Tablet Portrait 768x1024')
        assert home.is_loaded()
    
    def test_homepage_tablet_landscape(self, driver, base_url):
        """
        Test homepage on tablet landscape (1024x768)
        iPad landscape orientation
        """
        logger.info("Testing homepage on tablet landscape 1024x768")
        driver.set_window_size(1024, 768)
        
        home = HomePage(driver, base_url)
        home.navigate()
        home.prepare_for_visual_snapshot()
        
        percy_snapshot(driver, 'Homepage - Tablet Landscape 1024x768')
        assert home.is_loaded()
    
    def test_homepage_mobile_iphone_se(self, driver, base_url):
        """
        Test homepage on iPhone SE (375x667)
        Small mobile viewport - important for responsive design
        """
        logger.info("Testing homepage on iPhone SE 375x667")
        driver.set_window_size(375, 667)
        
        home = HomePage(driver, base_url)
        home.navigate()
        home.prepare_for_visual_snapshot()
        
        percy_snapshot(driver, 'Homepage - Mobile iPhone SE 375x667')
        assert home.is_loaded()
    
    def test_homepage_mobile_iphone_12(self, driver, base_url):
        """
        Test homepage on iPhone 12/13 (390x844)
        Modern iPhone size
        """
        logger.info("Testing homepage on iPhone 12 390x844")
        driver.set_window_size(390, 844)
        
        home = HomePage(driver, base_url)
        home.navigate()
        home.prepare_for_visual_snapshot()
        
        percy_snapshot(driver, 'Homepage - Mobile iPhone 12 390x844')
        assert home.is_loaded()
    
    def test_homepage_mobile_iphone_pro_max(self, driver, base_url):
        """
        Test homepage on iPhone Pro Max (428x926)
        Large mobile viewport
        """
        logger.info("Testing homepage on iPhone Pro Max 428x926")
        driver.set_window_size(428, 926)
        
        home = HomePage(driver, base_url)
        home.navigate()
        home.prepare_for_visual_snapshot()
        
        percy_snapshot(driver, 'Homepage - Mobile iPhone Pro Max 428x926')
        assert home.is_loaded()
    
    def test_homepage_mobile_android_pixel(self, driver, base_url):
        """
        Test homepage on Android Pixel (393x851)
        Common Android resolution
        """
        logger.info("Testing homepage on Android Pixel 393x851")
        driver.set_window_size(393, 851)
        
        home = HomePage(driver, base_url)
        home.navigate()
        home.prepare_for_visual_snapshot()
        
        percy_snapshot(driver, 'Homepage - Mobile Android Pixel 393x851')
        assert home.is_loaded()


@pytest.mark.visual
@pytest.mark.parametrize("width,height,device_name", [
    (1920, 1080, "Desktop Full HD"),
    (1366, 768, "Desktop HD"),
    (1024, 768, "Tablet Landscape"),
    (768, 1024, "Tablet Portrait"),
    (414, 896, "iPhone 11"),
    (375, 667, "iPhone SE"),
])
def test_homepage_responsive_matrix(driver, base_url, width, height, device_name):
    """
    Parametrized test for multiple viewports
    This demonstrates pytest's parametrization for efficient multi-device testing
    """
    logger.info(f"Testing homepage on {device_name} ({width}x{height})")
    driver.set_window_size(width, height)
    
    home = HomePage(driver, base_url)
    home.navigate()
    home.prepare_for_visual_snapshot()
    
    percy_snapshot(driver, f'Homepage - {device_name} {width}x{height}')
    assert home.is_loaded(), f"Homepage failed to load on {device_name}"


@pytest.mark.visual
@pytest.mark.interactive
class TestHomepageInteractive:
    """Visual tests for interactive states and user interactions"""
    
    def test_homepage_with_search_open(self, driver, base_url):
        """
        Test homepage with search dropdown/overlay open
        Important to test interactive states for visual regression
        """
        logger.info("Testing homepage with search open")
        driver.set_window_size(1920, 1080)
        
        home = HomePage(driver, base_url)
        home.navigate()
        home.wait_for_homepage_load()
        
        # Open search (assuming it has a dropdown/overlay)
        try:
            home.click(home.SEARCH_BAR)
            home.wait_for_page_load()
            home.hide_dynamic_elements()
            
            percy_snapshot(driver, 'Homepage - Search Dropdown Open')
        except Exception as e:
            logger.warning(f"Could not open search: {e}")
            pytest.skip("Search interaction not available")
    
    def test_homepage_scrolled_to_footer(self, driver, base_url):
        """
        Test homepage scrolled to footer
        Ensures footer visual consistency
        """
        logger.info("Testing homepage scrolled to footer")
        driver.set_window_size(1920, 1080)
        
        home = HomePage(driver, base_url)
        home.navigate()
        home.prepare_for_visual_snapshot()
        
        # Scroll to footer
        home.scroll_to_footer()
        
        percy_snapshot(driver, 'Homepage - Footer View')
        assert home.is_visible(home.FOOTER)


@pytest.mark.visual
@pytest.mark.smoke
def test_homepage_critical_path(driver, base_url):
    """
    Smoke test for critical homepage visual elements
    This test should run on every commit as a quick sanity check
    """
    logger.info("Running critical path visual smoke test")
    driver.set_window_size(1920, 1080)
    
    home = HomePage(driver, base_url)
    home.navigate()
    home.prepare_for_visual_snapshot()
    
    # Verify critical elements are visible
    assert home.is_visible(home.HERO_BANNER), "Hero banner not visible"
    assert home.is_visible(home.NAVIGATION_MENU), "Navigation not visible"
    assert home.is_visible(home.FOOTER), "Footer not visible"
    
    # Take snapshot
    percy_snapshot(driver, 'Homepage - Smoke Test')
    
    logger.info("Critical path visual test passed")
