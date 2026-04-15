"""
projekt_3.py: testovací skript pro třetí projekt  
do Engeto Online Testing Akademie
author: Pavlína Čepcová
email: cepcovap@gmail.com
"""
import pytest
import random
from playwright.sync_api import expect, Page

@pytest.fixture
def accept_cookies(page: Page) -> Page:
    """
    Opens homepage and accepts cookies 
    if the cookie bar is visible.
    Returns: 
        Page: Playwright page object with cookies accepted.
    """
    homepage = "https://automationexercise.com/"
    cookie_bar_selector = "div.fc-dialog-container"
    cookie_button_selector = "button.fc-cta-consent.fc-primary-button"
    page.goto(homepage)
    page.wait_for_load_state("load")
    accept_button = page.locator(cookie_button_selector)
   #Click accept button only if it is present on the page
    if accept_button.count() > 0:
        accept_button.click()
    cookie_bar = page.locator(cookie_bar_selector)
    expect(cookie_bar).not_to_be_visible()
    return page

def handle_ads(page):
    page.mouse.click(10, 10)

def user_login(page, email, password):
    #Clicks on link with login and fills out form with Email Address 
    #and password
    page.locator('a[href="/login"]').click()
    expect(page.get_by_text("Login to your account")).to_be_visible()
    page.locator('input[data-qa="login-email"]').fill(email)
    page.locator('input[data-qa="login-password"]').fill(password)
    page.locator('button[data-qa="login-button"]').click()
    page.wait_for_load_state("load") 
    handle_ads(page)
    
def add_product_to_cart(page):
    page.locator('a[href="#Women"]').click()
    page.wait_for_load_state("load")
    handle_ads(page)
    page.locator('a[href="/category_products/1"]').click()
    page.locator('a[data-product-id="3"]').first.click()
    page.locator('button:has-text("Continue Shopping")').click()


def test_homepage_is_visible(accept_cookies):
    """
    Verifies that the homepage is loaded by checking
    that the main image is visible.
    """
    page = accept_cookies
    locator_img = "div.logo.pull-left"
    expect(page.locator(locator_img)).to_be_visible()

def test_user_registration_positive(accept_cookies):
    page = accept_cookies
    name = f"test{random.randint(10000,99999)}"
    email = f"{name}@example.com"

    #Clicks on link with signup and fills out form with Name and Email Address
    page.locator('a[href="/login"]').click()
    expect(page.get_by_text("Login to your account")).to_be_visible()
    page.locator('input[data-qa="signup-name"]').fill(name)
    page.locator('input[data-qa="signup-email"]').fill(email)
    page.locator('button[data-qa="signup-button"]').click()
    expect(page.get_by_text("Enter Account Information")).to_be_visible()

    #Filling out the main registration form on the next page
    page.locator("input#id_gender1").click()
    page.locator('input[data-qa="password"]').fill("1234")
    page.locator("#days").select_option("1")
    page.locator("#months").select_option("January")
    page.locator("#years").select_option("2000")
    page.locator('input[data-qa="first_name"]').fill("Jon")
    page.locator('input[data-qa="last_name"]').fill("Doe")
    page.locator('input[data-qa="address"]').fill("123 Test Street")
    page.locator("#country").select_option("Canada")
    page.locator('input[data-qa="state"]').fill("Ontario")
    page.locator('input[data-qa="city"]').fill("Toronto")
    page.locator('input[data-qa="zipcode"]').fill("M5V 3L9")
    page.locator('input[data-qa="mobile_number"]').fill("123456789")
    page.locator('button[data-qa="create-account"]').click()
    page.wait_for_load_state("load")
    handle_ads(page)
    expect(page.get_by_text("Account Created")).to_be_visible()
    page.locator('a[data-qa="continue-button"]').click()
    page.wait_for_load_state("load")
    handle_ads(page)
    expect(page.get_by_text(f"Logged in as {name}")).to_be_visible()
    page.locator('a[href="/delete_account"]').click()
    page.wait_for_load_state("load") 
    handle_ads(page)
    expect(page.get_by_text("Account Deleted")).to_be_visible()
    page.locator('a[data-qa="continue-button"]').click()
    
def test_user_login_positive(accept_cookies):
    page = accept_cookies
    #Using pre-created acccount for login test
    TEST_NAME = "mytestname"
    TEST_EMAIL = "mytestemail@exercise.com"
    TEST_PASSWORD = "1234"
    user_login(page, TEST_EMAIL, TEST_PASSWORD)
    expect(page.get_by_text(f"Logged in as {TEST_NAME}")).to_be_visible()
    page.locator('a[href="/logout"]').click()

def test_add_to_cart_and_delete(accept_cookies):
    page = accept_cookies
    add_product_to_cart(page)
    page.locator('ul.nav.navbar-nav >> a[href="/view_cart"]').click()
    page.wait_for_load_state("load")
    expect(page.get_by_text("Sleeveless Dress")).to_be_visible()
    expect(page.locator('button.disabled')).to_have_text("1")
    page.locator('.cart_quantity_delete').click()
    page.locator('ul.nav.navbar-nav >> a[href="/view_cart"]').click()
    page.wait_for_load_state("load")  
    expect(page.get_by_text("Cart is empty!")).to_be_visible()

def test_login_add_product_and_payment_positive(accept_cookies):
    page = accept_cookies
    TEST_NAME = "Jane Doe"
    TEST_EMAIL = "mytestemail@exercise.com"
    TEST_PASSWORD = "1234"
    TEST_CARD_NUMBER = "4242424242424242"
    
    user_login(page, TEST_EMAIL, TEST_PASSWORD)
    add_product_to_cart(page)
    page.locator('ul.nav.navbar-nav >> a[href="/view_cart"]').click()
    page.get_by_text("Proceed To Checkout").click()
    page.wait_for_load_state("load") 
    expect(page.get_by_text("Your delivery address")).to_be_visible()
    page.get_by_text("Place Order").click()
    page.locator('input[name="name_on_card"]').fill(TEST_NAME)
    page.locator('input[name="card_number"]').fill(TEST_CARD_NUMBER)
    page.locator('input[name="cvc"]').fill("111")
    page.locator('input[name="expiry_month"]').fill("01")
    page.locator('input[name="expiry_year"]').fill("29")
    page.locator('button[data-qa="pay-button"]').click()
    page.wait_for_load_state("load") 
    expect(page.get_by_text("Order Placed!")).to_be_visible()
    page.locator('a[data-qa="continue-button"]').click()    






    


    

    






    
