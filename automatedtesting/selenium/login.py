from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def print_with_timestamp(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")


def login(user, password):
    print_with_timestamp('Starting the browser...')
    # --uncomment when running in Azure DevOps.
    options = ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    driver.get('https://www.saucedemo.com/')

    print_with_timestamp('Logging in...')
    driver.find_element(By.CSS_SELECTOR, "input[id='user-name']").send_keys(user)
    driver.find_element(By.CSS_SELECTOR, "input[id='password']").send_keys(password)
    driver.find_element(By.ID, "login-button").click()
    print_with_timestamp('Login successful! Proceeding with tests.')
    return driver


def add_items(driver):
    print_with_timestamp("Adding items to cart...")

    items = driver.find_elements(By.CSS_SELECTOR, '.inventory_item')

    added_items = []

    for item in items[:min(6, len(items))]:
        item_name = item.find_element(
            By.CLASS_NAME, 'inventory_item_name').text
        button = item.find_element(By.CSS_SELECTOR, '.pricebar > button')
        button.click()
        added_items.append(item_name)

    print_with_timestamp("Items '{}' added.".format("', '".join(added_items)))

    cart_badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")

    cart_items_count = cart_badge.text

    expected_count = len(added_items)
    actual_count = int(cart_items_count)
    assert expected_count == actual_count, f"Items count mismatch. Expected: {expected_count}, Actual: {actual_count}"
    print_with_timestamp(f"Added {actual_count} items to cart")


def remove_items(driver):
    print_with_timestamp("Removing items from cart")

    cart_link = driver.find_element(By.CLASS_NAME, "shopping_cart_link")
    cart_link.click()

    items = driver.find_elements(By.CLASS_NAME, 'cart_item')

    removed_items = []

    for item in items:
        item_name = item.find_element(
            By.CLASS_NAME, 'inventory_item_name').text
        button = item.find_element(By.CSS_SELECTOR, '.item_pricebar > button')
        button.click()
        removed_items.append(item_name)

    print_with_timestamp(f"Removed {len(items)} items")

    try:
        cart_badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")
    except NoSuchElementException:
        cart_badge = None

    assert cart_badge is None, "Still existing items in the cart."


if __name__ == "__main__":
    driver = login('standard_user', 'secret_sauce')
    add_items(driver)
    remove_items(driver)
    print_with_timestamp("All Selenium test run successfully")