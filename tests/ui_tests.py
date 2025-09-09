import pytest
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


# Configure logging to show timestamped logs during test execution
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

URL = "https://www.iamdave.ai/"

# Fixture to initialize and tear down the WebDriver once per module
@pytest.fixture(scope="module")
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")  # Launch browser in maximized mode
    # options.add_argument("--headless")  # Uncomment to run tests without opening the browser
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()  # Clean up after tests complete

# Reusable function to wait until an element is visible
def wait_for_visibility(driver, locator, timeout=10):
    return WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(locator))

# Test 1: Verify the homepage title contains the word "Dave"
def test_homepage_title(driver):
    driver.get(URL)
    WebDriverWait(driver, 10).until(EC.title_contains("Dave"))
    assert "Dave" in driver.title, "Page title does not contain 'Dave'"

# Test 2: Check if the company logo is visible on the homepage

def test_logo_present(driver):
    driver.get("https://www.iamdave.ai/")

    # Try common logo selectors
    logo_selectors = [
        (By.XPATH, "//img[contains(@alt, 'logo') or contains(@class, 'logo')]"),
        (By.XPATH, "//svg[contains(@class, 'logo')]"),
        (By.XPATH, "//*[contains(@id, 'logo')]"),
    ]

    logo = None
    for by, value in logo_selectors:
        try:
            logo = wait_for_visibility(driver, (by, value), timeout=5)
            if logo.is_displayed():
                break
        except TimeoutException:
            continue

    if not logo or not logo.is_displayed():
        # Log all images for debugging
        images = driver.find_elements(By.TAG_NAME, "img")
        for idx, img in enumerate(images):
            logging.info(f"Image[{idx}]: alt='{img.get_attribute('alt')}', class='{img.get_attribute('class')}', id='{img.get_attribute('id')}'")
        pytest.fail("Logo not found or not visible within the expected time")

    assert logo.is_displayed(), "Logo is not visible on the homepage"

# Test 3: Ensure the 'Get Started' button or link is present and visible
def test_get_started_button(driver):
    driver.get(URL)
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    # Look for 'Get Started' related elements (button, link, div with matching text)
    candidates = driver.find_elements(
        By.XPATH,
        "//*[self::a or self::button or self::div]"
        "[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'get started') or contains(@href, 'contact')]"
    )

    assert candidates, "No 'Get Started' element found"

    # Filter out visible elements from candidates
    visible = [el for el in candidates if el.is_displayed()]
    if not visible:
        # Try scrolling into view in case they are off-screen
        for el in candidates:
            driver.execute_script("arguments[0].scrollIntoView(true);", el)
        visible = [el for el in candidates if el.is_displayed()]

    assert visible, "'Get Started' element found but not visible"

    # Log details of all visible matches
    for idx, el in enumerate(visible):
        logging.info(f"[{idx}] Text: '{el.text.strip()}', Href: '{el.get_attribute('href')}'")

    assert visible[0].is_displayed(), "First 'Get Started' element is not displayed"

# Test 4: Validate that the page footer is visible
def test_footer_presence(driver):
    driver.get(URL)
    footer = wait_for_visibility(driver, (By.TAG_NAME, "footer"))
    assert footer.is_displayed(), "Footer is not visible on the page"
