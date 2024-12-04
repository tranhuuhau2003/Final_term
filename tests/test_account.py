import time

from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from utils.helper import click_element, fill_input, check_toast_message, check_error_message, login
from selenium.webdriver.common.by import By


@pytest.fixture
def driver():
    """Khởi tạo WebDriver cho mỗi bài kiểm thử."""
    driver = webdriver.Chrome()  # Đảm bảo ChromeDriver đã được cài đặt và trong PATH
    driver.maximize_window()
    yield driver
    driver.quit()

class TestAccount:

    def test_change_account_information(self, driver):
        driver.get("http://localhost/Webbanhang-main/index.html")

        # Gọi hàm login để đăng nhập
        login(driver, "hgbaodev", "123456")
        time.sleep(3)

        # Nhấn vào "Đăng nhập / Đăng ký"
        click_element(driver, By.CLASS_NAME, "text-dndk")
        time.sleep(2)

        # Nhấn vào "Tài khoản của tôi"
        click_element(driver, By.CSS_SELECTOR, "a[href='javascript:;'][onclick='myAccount()']")
        time.sleep(2)

        # Cập nhật địa chỉ giao hàng
        address_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "infoaddress"))
        )
        address_input.clear()  # Xóa địa chỉ cũ
        address_input.click()
        address_input.send_keys("123 Đường ABC, Quận 1, TP.HCM")
        time.sleep(2)  # Thêm thời gian chờ sau khi nhập địa chỉ

        # Nhấn "Lưu thay đổi"
        click_element(driver, By.ID, "save-info-user")
        time.sleep(3)  # Chờ thông tin được lưu

        # Nhấn vào "Đăng nhập / Đăng ký"
        click_element(driver, By.CLASS_NAME, "text-dndk")
        time.sleep(2)

        # Kiểm tra địa chỉ đã được cập nhật
        click_element(driver, By.CSS_SELECTOR, "a[href='javascript:;'][onclick='myAccount()']")
        updated_address = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "infoaddress"))
        )
        time.sleep(3)
        assert updated_address.get_attribute("value") == "123 Đường ABC, Quận 1, TP.HCM", "Địa chỉ chưa được cập nhật!"
        print("Địa chỉ đã được cập nhật thành công!")
