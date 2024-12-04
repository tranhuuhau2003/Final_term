import time

from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from utils.helper import click_element, fill_input, check_toast_message, check_error_message
from selenium.webdriver.common.by import By


@pytest.fixture
def driver():
    """Khởi tạo WebDriver cho mỗi bài kiểm thử."""
    driver = webdriver.Chrome()  # Đảm bảo ChromeDriver đã được cài đặt và trong PATH
    driver.maximize_window()
    yield driver
    driver.quit()


class TestAuthentication:

    def test_valid_login(self, driver):
        driver.get("http://localhost/Webbanhang-main/index.html")

        # Nhấn vào "Đăng nhập / Đăng ký"
        click_element(driver, By.CLASS_NAME, "text-dndk")

        # Nhấn vào "Đăng nhập"
        click_element(driver, By.ID, "login")

        # Điền số điện thoại và mật khẩu đúng
        fill_input(driver, By.ID, "phone-login", "0123456789")
        fill_input(driver, By.ID, "password-login", "123456")

        # Nhấn nút "Đăng nhập"
        click_element(driver, By.ID, "login-button")

        # Kiểm tra thông báo thành công
        try:
            toast_success = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "toast--success"))
            )
            assert toast_success.is_displayed(), "Thông báo thành công không hiển thị."
            print("Thông báo thành công hiển thị.")

            WebDriverWait(driver, 5).until(
                EC.invisibility_of_element_located((By.CLASS_NAME, "toast--success"))
            )
        except TimeoutException:
            assert False, "Thông báo thành công không biến mất sau thời gian chờ."

        # Kiểm tra hiển thị nút tài khoản cá nhân
        click_element(driver, By.CLASS_NAME, "text-dndk")

        my_account_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='javascript:;'][onclick='myAccount()']"))
        )
        assert my_account_button.is_displayed(), "Nút 'Tài khoản của tôi' không hiển thị sau khi đăng nhập."

        # Nhấn vào nút "Tài khoản của tôi"
        my_account_button.click()
        time.sleep(3)

        print("Đăng nhập thành công.")

    def test_invalid_login(self, driver):
        driver.get("http://localhost/Webbanhang-main/index.html")

        # Nhấn vào "Đăng nhập / Đăng ký"
        click_element(driver, By.CLASS_NAME, "text-dndk")

        # Nhấn vào "Đăng nhập"
        click_element(driver, By.ID, "login")

        # Điền số điện thoại và mật khẩu sai
        fill_input(driver, By.ID, "phone-login", "0123456789")
        fill_input(driver, By.ID, "password-login", "1234567")
        # Nhấn nút "Đăng nhập"
        click_element(driver, By.ID, "login-button")
        time.sleep(2)

        # Kiểm tra thông báo lỗi
        try:
            check_toast_message(driver, "toast__msg", "Sai mật khẩu")
            print("Thông báo lỗi hiển thị đúng: Sai mật khẩu.")
        except AssertionError as e:
            assert False, f"Thông báo lỗi không đúng hoặc không hiển thị: {str(e)}"

    def test_login_empty_password(self, driver):
        # Mở trang chính
        driver.get("http://localhost/Webbanhang-main/index.html")
        time.sleep(2)

        # Nhấn vào "Đăng nhập / Đăng ký"
        click_element(driver, By.CLASS_NAME, "text-dndk")

        # Nhấn vào "Đăng nhập"
        click_element(driver, By.ID, "login")

        # Điền số điện thoại nhưng không điền mật khẩu
        fill_input(driver, By.ID, "phone-login", "hgbaodev")
        fill_input(driver, By.ID, "password-login", "")  # Để trống mật khẩu
        time.sleep(2)

        # Nhấn nút "Đăng nhập"
        click_element(driver, By.ID, "login-button")
        time.sleep(2)

        # Kiểm tra thông báo lỗi
        check_toast_message(driver, "form-message-check-login", "Vui lòng nhập mật khẩu")

        # Kiểm tra thông báo lỗi
        try:
            check_toast_message(driver, "form-message-check-login", "Vui lòng nhập mật khẩu")
            print("Thông báo lỗi hiển thị đúng: Vui lòng nhập mật khẩu.")
        except AssertionError as e:
            assert False, f"Thông báo lỗi không đúng hoặc không hiển thị: {str(e)}"

    def test_register(self, driver):
        driver.get("http://localhost/Webbanhang-main/index.html")
        time.sleep(2)

        # Nhấn vào "Đăng nhập / Đăng ký"
        click_element(driver, By.CLASS_NAME, "text-dndk")

        # Nhấn vào "Đăng ký"
        click_element(driver, By.ID, "signup")

        # Điền thông tin vào các trường đăng ký
        fill_input(driver, By.ID, "fullname", "Nguyễn Văn AC")  # Họ và tên
        fill_input(driver, By.ID, "phone", "0123456769")  # Số điện thoại
        fill_input(driver, By.ID, "password", "password123")  # Mật khẩu
        fill_input(driver, By.ID, "password_confirmation", "password123")  # Nhập lại mật khẩu
        time.sleep(2)

        # Nhấn chọn ô checkbox
        checkbox = driver.find_element(By.ID, "checkbox-signup")
        driver.execute_script("arguments[0].click();", checkbox)
        time.sleep(1)

        # Nhấn vào nút "Đăng ký"
        click_element(driver, By.ID, "signup-button")
        time.sleep(2)

        # Kiểm tra thông báo lỗi
        try:
            check_toast_message(driver, "toast__msg", "Tạo thành công tài khoản !")
            print("Kiểm thử tạo tài khoản thành công.")
        except AssertionError as e:
            assert False, f"Thông báo xác nhận không đúng hoặc không hiển thị: {str(e)}"

    def test_register_missing_phone(self, driver):
        driver.get("http://localhost/Webbanhang-main/index.html")
        time.sleep(2)

        # Nhấn vào "Đăng nhập / Đăng ký"
        click_element(driver, By.CLASS_NAME, "text-dndk")

        # Nhấn vào "Đăng ký"
        click_element(driver, By.ID, "signup")

        # Điền thông tin vào các trường đăng ký (bỏ qua "Số điện thoại")
        fill_input(driver, By.ID, "fullname", "Nguyễn Văn AC")  # Họ và tên
        fill_input(driver, By.ID, "password", "password123")  # Mật khẩu
        fill_input(driver, By.ID, "password_confirmation", "password123")  # Nhập lại mật khẩu

        # Nhấn vào checkbox
        checkbox = driver.find_element(By.ID, "checkbox-signup")
        driver.execute_script("arguments[0].click();", checkbox)
        time.sleep(2)

        # Nhấn vào nút "Đăng ký"
        click_element(driver, By.ID, "signup-button")
        time.sleep(2)

        # Kiểm tra thông báo lỗi khi thiếu số điện thoại
        check_error_message(driver, "form-message-phone", "Vui lòng nhập vào số điện thoại")

        print("Kiểm thử đăng ký thiếu số điện thoại thành công.")

    def test_register_duplicate_phone(self, driver):
        driver.get("http://localhost/Webbanhang-main/index.html")
        time.sleep(2)  # Thêm thời gian chờ sau khi tải trang chính

        # Nhấn vào "Đăng nhập / Đăng ký"
        click_element(driver, By.CLASS_NAME, "text-dndk")

        # Nhấn vào "Đăng ký"
        click_element(driver, By.ID, "signup")
        time.sleep(2)  # Thêm thời gian chờ sau khi nhấn "Đăng ký"

        # Điền thông tin vào các trường đăng ký (sử dụng số điện thoại đã tồn tại)
        fill_input(driver, By.ID, "fullname", "Nguyễn Văn AC")  # Họ và tên
        fill_input(driver, By.ID, "phone", "hgbaodev")  # Số điện thoại đã đăng ký
        fill_input(driver, By.ID, "password", "123456")  # Mật khẩu
        fill_input(driver, By.ID, "password_confirmation", "123456")  # Nhập lại mật khẩu
        time.sleep(2)  # Thêm thời gian chờ sau khi điền các trường

        # Nhấn vào checkbox
        checkbox = driver.find_element(By.ID, "checkbox-signup")
        driver.execute_script("arguments[0].click();", checkbox)
        time.sleep(2)  # Thêm thời gian chờ sau khi nhấn vào checkbox

        # Nhấn nút "Đăng ký"
        click_element(driver, By.ID, "signup-button")
        time.sleep(2)  # Thêm thời gian chờ sau khi nhấn "Đăng ký"

        # Kiểm tra thông báo lỗi khi đăng ký trùng tài khoản
        check_toast_message(driver, "toast__msg", "Tài khoản đã tồn tại !")

        print("Kiểm thử đăng ký với tài khoản đã tồn tại thành công.")

    def test_logout(self, driver):
        driver.get("http://localhost/Webbanhang-main/index.html")
        time.sleep(2)

        # Nhấn vào "Đăng nhập / Đăng ký"
        click_element(driver, By.CLASS_NAME, "text-dndk")

        # Nhấn vào "Đăng nhập"
        click_element(driver, By.ID, "login")

        # Điền số điện thoại và mật khẩu
        fill_input(driver, By.ID, "phone-login", "hgbaodev")  # Số điện thoại
        fill_input(driver, By.ID, "password-login", "123456")  # Mật khẩu
        time.sleep(2)

        # Nhấn vào nút "Đăng nhập"
        click_element(driver, By.ID, "login-button")
        time.sleep(2)

        # Kiểm tra thông báo hoặc trạng thái đăng nhập
        # (Có thể thêm kiểm tra toast thông báo thành công tại đây nếu cần)

        # Đăng xuất
        # Nhấn vào "Đăng nhập / Đăng ký"
        click_element(driver, By.CLASS_NAME, "text-dndk")
        time.sleep(1)

        # Nhấn vào "Thoát tài khoản"
        click_element(driver, By.ID, "logout")
        time.sleep(1)

        # Kiểm tra nút "Đăng nhập" xuất hiện sau khi đăng xuất
        login_button_after_logout = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "login"))
        )
        assert login_button_after_logout.is_displayed(), "Nút 'Đăng nhập' không xuất hiện sau khi đăng xuất."