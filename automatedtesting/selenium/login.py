# #!/usr/bin/env python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions


# Start the browser and login with standard_user
def login (user, password):
    print ('Starting the browser...')
    # --uncomment when running in Azure DevOps.
    # options = ChromeOptions()
    # options.add_argument("--headless") 
    # driver = webdriver.Chrome(options=options)
    driver = webdriver.Chrome()
    print ('Browser started successfully. Navigating to the demo page to login.')
    driver.get('https://www.saucedemo.com/')
    input_username = driver.find_element(By.ID, 'user-name')
    input_password = driver.find_element(By.ID, 'password')
    btn_login = driver.find_element(By.ID, 'login-button')
    
    input_password.send_keys(user)
    input_password.send_keys(password)
    btn_login.click()
    product_label = driver.find_element(By.CSS_SELECTOR, "div[class='inventory_item_name']").text
    assert "Sauce Labs Bike Light" in product_label
    return driver
def add_to_cart(driver, items):
    print ('Adding 6 items to cart ...')
    add_to_cart_btns = driver.find_elements(By.CLASS_NAME, "btn_inventory")
    for btns in add_to_cart_btns[:6]:
        btns.click()
    print('Added to cart')
def remove_from_cart(driver, items):
    print ('Removing 6 items from cart ...')
    remove_btns = driver.find_elements(By.CLASS_NAME, "btn_inventory")
    for btns in remove_btns[:2]:
        btns.click()
    print ('Removed 6 items from cart ...')
if __name__ = "__main__":
    items = 6
    driver = login('standard_user', 'secret_sauce')
    add_to_cart(driver, items)
    remove_from_cart(driver, items)
