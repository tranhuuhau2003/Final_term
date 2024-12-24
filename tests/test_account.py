import time

from selenium.common import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from Final_term.utils.helper import click_element, fill_input, check_toast_message, check_error_message, login, add_customer, logout, logout_admin, add_to_cart, add_multiple_to_cart, update_product_quantity_in_cart, check_cart_quantity, scroll_to_element
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

class TestAccount:

    def test_change_account_information(self, driver):
        try:
            driver.get("http://localhost/Webbanhang-main/index.html")

            login(driver, "0123456789", "123456")
            time.sleep(3)

            click_element(driver, By.CLASS_NAME, "text-dndk")
            time.sleep(2)

            click_element(driver, By.CSS_SELECTOR, "a[href='javascript:;'][onclick='myAccount()']")
            time.sleep(2)

            address_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "infoaddress"))
            )
            address_input.clear()
            address_input.click()
            address_input.send_keys("123 Đường ABC, Quận 1, TP.HCM")
            time.sleep(2)

            click_element(driver, By.ID, "save-info-user")
            time.sleep(1)

            result = check_toast_message(driver, "toast__msg", "Cập nhật thông tin thành công !")
            assert result, "Không nhận được thông báo 'Cập nhật thông tin thành công!' hoặc thông báo không đúng."
            print("Kiểm thử thay đổi thông tin tài khoản thành công!")

        except Exception as e:
            assert False, f"Đã xảy ra lỗi trong quá trình kiểm thử: {str(e)}"

        finally:
            logout(driver)

    def test_change_password(self, driver):
        driver.get("http://localhost/Webbanhang-main/index.html")

        try:
            login(driver, "0123456789", "123456")
            time.sleep(4)

            click_element(driver, By.CLASS_NAME, "text-dndk")
            time.sleep(2)

            click_element(driver, By.CSS_SELECTOR, "a[href='javascript:;'][onclick='myAccount()']")
            time.sleep(2)

            current_password_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "password-cur-info"))
            )
            current_password_input.send_keys("123456")

            fill_input(driver, By.ID, "password-after-info", "Anhpham2@.")
            fill_input(driver, By.ID, "password-comfirm-info", "Anhpham2@.")

            click_element(driver, By.ID, "save-password")
            time.sleep(2)

            result = check_toast_message(driver, "toast__msg", "Đổi mật khẩu thành công !")
            assert result, "Không nhận được thông báo 'Đổi mật khẩu thành công!' hoặc thông báo không đúng."
            print("Đổi mật khẩu thành công.")

            logout_success = logout(driver)
            assert logout_success, "Đăng xuất không thành công."
            time.sleep(1)

            login(driver, "0123456789", "Anhpham2@.")
            time.sleep(2)

            click_element(driver, By.CLASS_NAME, "text-dndk")
            time.sleep(1)

            my_account_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='javascript:;'][onclick='myAccount()']"))
            )
            assert my_account_button.is_displayed(), "Đăng nhập thất bại, không thấy 'Tài khoản của tôi'."
            print("Đăng nhập lại thành công, mật khẩu đã được thay đổi.")

        except Exception as e:
            assert False, f"Đã xảy ra lỗi trong quá trình kiểm thử: {str(e)}"

        finally:
            logout(driver)
