import time

from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from Final_term.utils.helper import click_element, fill_input, check_toast_message, check_error_message, login, add_customer, logout, logout_admin, add_to_cart, add_multiple_to_cart, update_product_quantity_in_cart, check_cart_quantity, scroll_to_element, \
register_account
from Final_term.utils.driver_helper import init_driver, close_driver  # Import từ driver_helper
from selenium.webdriver.common.by import By



@pytest.fixture
def driver():
    """
    Khởi tạo WebDriver và đóng WebDriver sau khi test xong.
    """
    driver = init_driver()  # Gọi hàm khởi tạo driver từ file driver_helper
    yield driver  # Cung cấp driver cho test
    close_driver(driver)  # Đóng driver sau khi test xong



class TestLoginRegister:

    def test_register(self, driver):
        try:
            register_account(driver, "Nguyễn Văn ABC", "0101010101", "password123")
            result = check_toast_message(driver, "toast__msg", "Tạo thành công tài khoản !")
            assert result, "Thông báo xác nhận không đúng hoặc không hiển thị."
            print("Kiểm thử tạo tài khoản thành công.")
        finally:
            logout(driver)

    def test_register_missing_phone(self, driver):
        try:
            register_account(driver, "Nguyễn Văn AC", "", "password123")
            result = check_toast_message(driver, "form-message-phone", "Vui lòng nhập vào số điện thoại")
            assert result, "Thông báo lỗi không đúng hoặc không hiển thị."
            print("Kiểm thử đăng ký thiếu số điện thoại thành công.")
        finally:
            logout(driver)

    def test_register_duplicate_phone(self, driver):
        try:
            register_account(driver, "Nguyễn Văn ABC", "0123456789", "123456")
            result = check_toast_message(driver, "toast__msg", "Tài khoản đã tồn tại !")
            assert result, "Thông báo lỗi không đúng hoặc không hiển thị."
            print("Kiểm thử đăng ký với tài khoản đã tồn tại thành công.")
        finally:
            logout(driver)

    def test_valid_login(self, driver):
        try:
            login(driver, "0123456789", "123456")  # Using the existing login function
            result = check_toast_message(driver, "toast--success", "Đăng nhập thành công")
            assert result, "Thông báo đăng nhập thành công không đúng hoặc không hiển thị."
            print("Đăng nhập thành công.")

            # Verify 'My Account' button appears after login
            my_account_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='javascript:;'][onclick='myAccount()']"))
            )
            assert my_account_button.is_displayed(), "Nút 'Tài khoản của tôi' không hiển thị."
        finally:
            logout(driver)

    def test_invalid_login(self, driver):
        try:
            login(driver, "0123456789", "wrongpassword")  # Using the existing login function
            result = check_toast_message(driver, "toast__msg", "Sai mật khẩu")
            assert result, "Thông báo lỗi không đúng hoặc không hiển thị."
            print("Thông báo lỗi hiển thị đúng: Sai mật khẩu.")
        except Exception as e:
            assert False, f"Đã xảy ra lỗi trong quá trình kiểm thử: {str(e)}"

    def test_login_empty_password(self, driver):
        try:
            driver.get("http://localhost/Webbanhang-main/index.html")
            click_element(driver, By.CLASS_NAME, "text-dndk")
            click_element(driver, By.ID, "login")
            fill_input(driver, By.ID, "phone-login", "hgbaodev")
            fill_input(driver, By.ID, "password-login", "")
            click_element(driver, By.ID, "login-button")
            result = check_toast_message(driver, "form-message-check-login", "Vui lòng nhập mật khẩu")
            assert result, "Thông báo lỗi không đúng hoặc không hiển thị."
            print("Thông báo lỗi hiển thị đúng: Vui lòng nhập mật khẩu.")
        except Exception as e:
            assert False, f"Đã xảy ra lỗi trong quá trình kiểm thử: {str(e)}"

    def test_logout(self, driver):
        try:
            login(driver, "hgbaodev", "123456")  # Using the existing login function
            logout_success = logout(driver)
            assert logout_success, "Đăng xuất không thành công."
            print("Kiểm thử đăng xuất thành công.")
        except Exception as e:
            assert False, f"Đã xảy ra lỗi trong quá trình kiểm thử: {str(e)}"
