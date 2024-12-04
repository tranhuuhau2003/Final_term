# Tui làm đăng nhập,đăng kí ,đăng xuất,giỏ hàng( bao gồm thanh toán),tài khoản của tôi,tìm kiếm món ăn ở trang chủ,chức năng khách hàng của admin  oke ko mn

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


def click_element(driver, by, value):
    """Click vào một phần tử."""
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((by, value))
    )
    ActionChains(driver).move_to_element(element).click().perform()


def fill_input(driver, by, value, input_value):
    """Điền giá trị vào input."""
    field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((by, value))
    )
    field.clear()  # Đảm bảo input trống trước khi nhập
    field.send_keys(input_value)
    time.sleep(1)


def check_toast_message(driver, message_class, expected_text):
    """Kiểm tra thông báo (toast message)."""
    toast_message = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, message_class))
    )
    assert toast_message.is_displayed(), f"Không hiển thị thông báo. {expected_text} thất bại."
    assert expected_text in toast_message.text, f"Thông báo không khớp: {toast_message.text}"


def check_error_message(driver, message_class, expected_text):
    """Kiểm tra thông báo lỗi."""
    try:
        # Đợi và lấy thông báo lỗi
        error_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, message_class))
        )

        # Kiểm tra thông báo lỗi có hiển thị không
        assert error_message.is_displayed(), f"Không hiển thị thông báo lỗi với class '{message_class}'."

        # Kiểm tra nội dung thông báo lỗi
        assert expected_text in error_message.text, \
            f"Thông báo lỗi không đúng. Mong đợi '{expected_text}', nhưng nhận được: {error_message.text}"

        print(f"Thông báo lỗi hiển thị đúng: {expected_text}")

    except AssertionError as e:
        print(f"Lỗi khi kiểm tra thông báo lỗi: {str(e)}")
        raise  # Ném lỗi lên để thông báo cho người kiểm thử


def login(driver, phone_number, password):
    """
    Hàm đăng nhập vào tài khoản.

    :param driver: Đối tượng WebDriver
    :param phone_number: Số điện thoại đăng nhập
    :param password: Mật khẩu đăng nhập
    """
    # Nhấn vào "Đăng nhập / Đăng ký"
    click_element(driver, By.CLASS_NAME, "text-dndk")

    # Nhấn vào "Đăng nhập"
    click_element(driver, By.ID, "login")

    # Điền số điện thoại và mật khẩu
    fill_input(driver, By.ID, "phone-login", phone_number)
    fill_input(driver, By.ID, "password-login", password)

    # Nhấn nút "Đăng nhập"
    click_element(driver, By.ID, "login-button")


def add_customer(driver, fullname, phone, password):
    """
    Hàm thêm một khách hàng mới vào danh sách khách hàng.

    :param driver: Đối tượng WebDriver
    :param fullname: Tên khách hàng
    :param phone: Số điện thoại khách hàng
    :param password: Mật khẩu của khách hàng
    """
    # Nhấn vào nút "Thêm khách hàng"
    click_element(driver, By.XPATH, "//button[@id='btn-add-user']")

    # Điền thông tin khách hàng mới
    fill_input(driver, By.ID, "fullname", fullname)
    fill_input(driver, By.ID, "phone", phone)
    fill_input(driver, By.ID, "password", password)

    # Nhấn nút "Đăng ký"
    click_element(driver, By.ID, "signup-button")
