"""
Example visual regression tests
These tests demonstrate Percy visual testing with Selenium
"""
import pytest
from percy import percy_snapshot


@pytest.mark.visual
@pytest.mark.smoke
def test_homepage_desktop(driver, base_url, percy):
    """Test homepage visual appearance on desktop viewport"""
    driver.get(base_url)
    driver.implicitly_wait(5)
    
    # Take Percy snapshot
    percy('Homepage - Desktop - 1920x1080')


@pytest.mark.visual
@pytest.mark.mobile
def test_homepage_mobile(driver, base_url, percy):
    """Test homepage visual appearance on mobile viewport"""
    driver.set_window_size(375, 667)  # iPhone SE size
    driver.get(base_url)
    driver.implicitly_wait(5)
    
    percy('Homepage - Mobile - 375x667')


@pytest.mark.visual
@pytest.mark.parametrize("width,height,device", [
    (1920, 1080, "Desktop"),
    (1024, 768, "Tablet"),
    (375, 667, "Mobile"),
])
def test_responsive_homepage(driver, base_url, percy, width, height, device):
    """Test homepage across multiple viewports"""
    driver.set_window_size(width, height)
    driver.get(base_url)
    driver.implicitly_wait(5)
    
    percy(f'Homepage - {device} - {width}x{height}')


@pytest.mark.visual
@pytest.mark.critical
def test_checkout_page_visual(driver, base_url, percy):
    """Test checkout page critical business flow"""
    # Navigate to checkout (example)
    driver.get(f"{base_url}/checkout")
    driver.implicitly_wait(5)
    
    percy('Checkout Page - Critical Flow')
