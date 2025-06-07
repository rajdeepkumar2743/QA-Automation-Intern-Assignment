import pytest
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Enable logging
logging.basicConfig(level=logging.INFO)

# Pytest fixture to initialize and quit WebDriver
@pytest.fixture(scope="module")
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")  # Start browser maximized
    # options.add_argument("--headless")  # Uncomment for headless execution
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

# Test: Homepage Title Verification
def test_homepage_title(driver):
    driver.get("https://www.iamdave.ai")
    WebDriverWait(driver, 10).until(EC.title_contains("Dave"))
    assert "Dave" in driver.title, "Page title does not contain 'Dave'"

# Test: Logo Visibility on Homepage
def test_logo_present(driver):
    driver.get("https://www.iamdave.ai")

    # Wait until a logo image is visible based on src, alt, or class
    logo = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH,
                                          "//img[contains(@src, 'logo') or contains(@alt, 'Dave') or contains(@class, 'logo')]"))
    )

    # Scroll logo into view (in case it's initially offscreen)
    driver.execute_script("arguments[0].scrollIntoView(true);", logo)
    assert logo.is_displayed(), "Logo is not visible on the homepage"

# Test: 'Get Started' Button or Link Visibility
def test_get_started_button(driver):
    driver.get("https://www.iamdave.ai")

    # Ensure the page has loaded
    WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    # Try to locate 'Get Started' element (link or button)
    elements = driver.find_elements(By.XPATH,
                                    "//*[self::a or self::button or self::div]"
                                    "[contains(text(), 'Get Started') or contains(text(), 'get started') or contains(@href, 'contact')]")

    assert elements, "No 'Get Started' element found on the page"

    # Filter visible elements
    visible_elements = [el for el in elements if el.is_displayed()]

    # If none visible, try scrolling into view
    if not visible_elements:
        for el in elements:
            driver.execute_script("arguments[0].scrollIntoView(true);", el)
        visible_elements = [el for el in elements if el.is_displayed()]

    assert visible_elements, "'Get Started' element found but not visible"

    # Optional debug logging (can be removed or logged to file)
    for idx, el in enumerate(visible_elements):
        logging.info(f"Visible 'Get Started' element {idx}: text='{el.text}', href='{el.get_attribute('href')}'")

    # Final check on the first visible element
    assert visible_elements[0].is_displayed(), "'Get Started' element is not displayed"

# Test: Footer Presence and Visibility
def test_footer_presence(driver):
    driver.get("https://www.iamdave.ai")

    # Wait until the footer is visible
    footer = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.TAG_NAME, "footer"))
    )

    assert footer.is_displayed(), "Footer is not visible on the page"
