import time

from selenium.common import TimeoutException
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



class TestLoginRegister:

    def test_register(self, driver):
        driver.get("http://localhost/Webbanhang-main/index.html")
        time.sleep(2)

        try:
            # Nhấn vào "Đăng nhập / Đăng ký"
            click_element(driver, By.CLASS_NAME, "text-dndk")

            # Nhấn vào "Đăng ký"
            click_element(driver, By.ID, "signup")

            # Điền thông tin vào các trường đăng ký
            fill_input(driver, By.ID, "fullname", "Nguyễn dVăn sadaC")  # Họ và tên
            fill_input(driver, By.ID, "phone", "0123324235676229")  # Số điện thoại
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

            # Kiểm tra thông báo đăng ký thành công
            check_toast_message(driver, "toast__msg", "Tạo thành công tài khoản !")
            print("Kiểm thử tạo tài khoản thành công.")
            time.sleep(2)

        except AssertionError as e:
            assert False, f"Thông báo xác nhận không đúng hoặc không hiển thị: {str(e)}"

        finally:
            # Đăng xuất nếu thông báo tạo tài khoản thành công đã xuất hiện
            try:
                # Nếu tài khoản được đăng nhập, thực hiện đăng xuất
                logout(driver)
            except Exception as e:
                print(f"Không thể thực hiện đăng xuất: {str(e)}")

    def test_register_missing_phone(self, driver):
        try:
            driver.get("http://localhost/Webbanhang-main/index.html")
            time.sleep(2)

            # Nhấn vào "Đăng nhập / Đăng ký"
            click_element(driver, By.CLASS_NAME, "text-dndk")

            # Nhấn vào "Đăng ký"
            click_element(driver, By.ID, "signup")

            # Điền thông tin vào các trường đăng ký (bỏ qua "Số điện thoại")
            fill_input(driver, By.ID, "fullname", "Nguyễn Văn AC")  # Họ và tên
            time.sleep(1)

            fill_input(driver, By.ID, "password", "password123")  # Mật khẩu
            time.sleep(1)

            fill_input(driver, By.ID, "password_confirmation", "password123")  # Nhập lại mật khẩu
            time.sleep(1)

            # Nhấn vào checkbox
            checkbox = driver.find_element(By.ID, "checkbox-signup")
            driver.execute_script("arguments[0].click();", checkbox)
            time.sleep(1)

            # Nhấn vào nút "Đăng ký"
            click_element(driver, By.ID, "signup-button")
            time.sleep(2)

            # Kiểm tra thông báo lỗi khi thiếu số điện thoại
            check_error_message(driver, "form-message-phone", "Vui lòng nhập vào số điện thoại")

            print("Kiểm thử đăng ký thiếu số điện thoại thành công.")
        except Exception as e:
            assert False, f"Đã xảy ra lỗi trong quá trình kiểm thử: {str(e)}"
        finally:
            # Gọi hàm logout để đảm bảo đăng xuất sau mỗi kiểm thử
            logout(driver)

    def test_register_duplicate_phone(self, driver):
        try:
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
        except Exception as e:
            assert False, f"Đã xảy ra lỗi trong quá trình kiểm thử: {str(e)}"
        finally:
            # Gọi hàm logout để đảm bảo trạng thái sạch cho kiểm thử tiếp theo
            logout(driver)

    def test_valid_login(self, driver):
        try:
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
        except Exception as e:
            assert False, f"Đã xảy ra lỗi trong quá trình kiểm thử: {str(e)}"
        finally:
            # Gọi hàm logout để đảm bảo trạng thái sạch
            logout(driver)

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

        # Đăng xuất
        assert logout(driver), "Đăng xuất không thành công."
        print("Kiểm thử đăng xuất thành công.")

