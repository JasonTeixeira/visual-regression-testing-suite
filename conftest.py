"""
Pytest configuration and fixtures for visual regression testing
"""
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from percy import percy_snapshot
import os


@pytest.fixture(scope="session")
def percy_enabled():
    """Check if Percy is enabled via environment variable"""
    return os.getenv('PERCY_TOKEN') is not None


@pytest.fixture(scope="function")
def driver(request):
    """Initialize WebDriver for each test"""
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(10)
    
    yield driver
    
    driver.quit()


@pytest.fixture
def base_url():
    """Base URL for the application under test"""
    return os.getenv('BASE_URL', 'https://www.example.com')


@pytest.fixture
def percy(driver, percy_enabled):
    """Percy snapshot helper"""
    def take_snapshot(name, **kwargs):
        if percy_enabled:
            percy_snapshot(driver, name, **kwargs)
        else:
            print(f"Percy disabled - skipping snapshot: {name}")
    
    return take_snapshot
