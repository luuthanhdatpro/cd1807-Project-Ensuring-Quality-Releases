#!/usr/bin/env python

from login import login
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


def add_items(driver):
    print_with_timestamp("Adding items to cart...")

    # Get all the items in the inventory list
    items = driver.find_elements(By.CSS_SELECTOR, '.inventory_item')

    # List to store added items
    added_items = []

    # Iterate through the items (maximum 6 or the actual number of items if less than 6)
    for item in items[:min(6, len(items))]:
        # Get the name of the item and add to cart
        item_name = item.find_element(
            By.CLASS_NAME, 'inventory_item_name').text
        button = item.find_element(By.CSS_SELECTOR, '.pricebar > button')
        button.click()
        added_items.append(item_name)

    # Print the list of added items
    print_with_timestamp("Items '{}' added.".format("', '".join(added_items)))

    # Show the number of items in the cart
    # Find the shopping cart badge element
    cart_badge = driver.find_element(By.CLASS_NAME, "shopping_cart_badge")

    # Get the text from the badge
    cart_items_count = cart_badge.text

    # Perform the assertion
    expected_count = len(added_items)
    actual_count = int(cart_items_count)
    assert expected_count == actual_count, f"Items count mismatch. Expected: {expected_count}, Actual: {actual_count}"
    print_with_timestamp(f"Added {actual_count} items to cart")


def remove_items(driver):
    print_with_timestamp("Removing items from cart")

    # Click on the shopping cart link
    cart_link = driver.find_element(By.CLASS_NAME, "shopping_cart_link")
    cart_link.click()

    # Find all items in the cart and remove them
    items = driver.find_elements(By.CLASS_NAME, 'cart_item')

    # List to store added items
    removed_items = []

    for item in items:
        # Get the name of the item and click the 'Remove' button
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