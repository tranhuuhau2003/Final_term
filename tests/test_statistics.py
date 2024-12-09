import datetime
import time

from selenium.common import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import pytest
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from Final_term.utils.helper import click_element, fill_input, check_toast_message, check_error_message, login, add_customer, logout, logout_admin, add_to_cart, add_multiple_to_cart, update_product_quantity_in_cart, check_cart_quantity, scroll_to_element
from selenium.webdriver.common.by import By
from datetime import datetime



@pytest.fixture
def driver():
    """
    Khởi tạo WebDriver với profile Chrome được định trước.
    """
    profile_path = "C:\\Users\\user\\AppData\\Local\\Google\\Chrome\\User Data"
    profile_directory = "Default"  # Đây là profile mà bạn muốn sử dụng (ví dụ: "Default", "Profile 1",...)

    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_path}")  # Chỉ định thư mục chứa profile
    options.add_argument(f"profile-directory={profile_directory}")  # Chỉ định tên thư mục profile

    driver = webdriver.Chrome(options=options)
    driver.maximize_window()

    try:
        yield driver  # Cung cấp driver cho test
    finally:
        driver.quit()  # Đóng trình duyệt

@pytest.fixture
def setup_and_teardown(driver):
    """
    Fixture đảm bảo logout sau mỗi test.
    """
    try:
        yield driver  # Sử dụng driver từ fixture `driver`
    finally:
        # Đăng xuất trước khi teardown
        try:
            logout_admin(driver)
        except Exception as e:
            print(f"Không thể đăng xuất: {e}")

class TestStatitics:
