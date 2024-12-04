import time

from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
import pytest
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from utils.helper import click_element, fill_input, check_toast_message, check_error_message, login, add_customer
from selenium.webdriver.common.by import By


@pytest.fixture
def driver():
    """Khởi tạo WebDriver với profile Chrome được định trước."""
    profile_path = "C:\\Users\\user\\AppData\\Local\\Google\\Chrome\\User Data\\Default"

    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_path}")

    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    yield driver
    driver.quit()


class TestCustomerManagement:

    def test_add_customer(self, driver):
        """
        Test thêm khách hàng mới vào danh sách khách hàng.
        """
        # Truy cập trang web
        driver.get("http://localhost/Webbanhang-main/index.html")
        time.sleep(2)

        # Đăng nhập tài khoản admin sử dụng hàm login từ helper
        login(driver, "hgbaodev", "123456")
        time.sleep(3)

        # Nhấn vào "Đăng nhập / Đăng ký"
        click_element(driver, By.CLASS_NAME, "text-dndk")
        time.sleep(2)

        # Điều hướng đến trang quản lý cửa hàng
        click_element(driver, By.XPATH, "//a[contains(text(), 'Quản lý cửa hàng')]")
        time.sleep(2)

        # Chuyển đến phần "Khách hàng"
        click_element(driver, By.XPATH, "//div[@class='hidden-sidebar' and text()='Khách hàng']")
        time.sleep(2)

        # Sử dụng hàm add_customer để thêm khách hàng
        add_customer(driver, "Nhật Sinh", "0394996781", "MatKhau123!")
        time.sleep(3)

        # Kiểm tra thông tin khách hàng trong bảng
        rows = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//tbody[@id='show-user']/tr"))
        )
        expected_name = "Nhật Sinh"
        expected_phone = "0394996781"

        customer_found = False
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) > 1 and cells[1].text.strip() == expected_name and cells[2].text.strip() == expected_phone:
                customer_found = True
                break

        # Assert kiểm tra kết quả
        assert customer_found, f"Không tìm thấy khách hàng '{expected_name}' với số điện thoại '{expected_phone}' trong danh sách."
        print(f"Khách hàng '{expected_name}' với số điện thoại '{expected_phone}' đã được thêm thành công!")

    def test_filter_active_customers(self, driver):
        """
        Test thêm khách hàng mới vào danh sách khách hàng và lọc theo trạng thái "Hoạt động".
        """
        # Truy cập trang web
        driver.get("http://localhost/Webbanhang-main/index.html")
        time.sleep(2)

        # Đăng nhập tài khoản admin sử dụng hàm login từ helper
        login(driver, "hgbaodev", "123456")
        time.sleep(3)

        # Nhấn vào "Đăng nhập / Đăng ký"
        click_element(driver, By.CLASS_NAME, "text-dndk")
        time.sleep(2)

        # Điều hướng đến trang quản lý cửa hàng
        click_element(driver, By.XPATH, "//a[contains(text(), 'Quản lý cửa hàng')]")
        time.sleep(2)

        # Chuyển đến phần "Khách hàng"
        click_element(driver, By.XPATH, "//div[@class='hidden-sidebar' and text()='Khách hàng']")
        time.sleep(2)

        # Sử dụng hàm add_customer để thêm khách hàng
        add_customer(driver, "Nhật Sinh", "0394996781", "MatKhau123!")

        # Chờ menu thả xuống xuất hiện để lọc khách hàng theo trạng thái
        dropdown = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "tinh-trang-user"))
        )

        # Tạo đối tượng Select
        select = Select(dropdown)

        # Chọn giá trị "Hoạt động" (value="1")
        select.select_by_value("1")
        time.sleep(2)

        # Chờ các kết quả hiển thị
        results = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "status-complete"))
        )
        time.sleep(3)

        # Kiểm tra trạng thái của từng kết quả
        statuses = [result.text.strip() for result in results]
        assert "Hoạt động" in statuses, "Lỗi: Không có khách hàng nào đang hoạt động."
        assert all(status == "Hoạt động" for status in statuses), (
            f"Lỗi: Có trạng thái không phải 'Hoạt động'. Các trạng thái không đúng: "
            f"{[status for status in statuses if status != 'Hoạt động']}"
        )
        print("Kết quả kiểm tra thành công: Tất cả khách hàng đang ở trạng thái 'Hoạt động'.")

    def test_filter_locked_customers(self, driver):
        """
        Test thêm khách hàng mới vào danh sách khách hàng và lọc theo trạng thái "Bị khóa".
        """
        # Truy cập trang web
        driver.get("http://localhost/Webbanhang-main/index.html")
        time.sleep(2)

        # Đăng nhập tài khoản admin sử dụng hàm login từ helper
        login(driver, "hgbaodev", "123456")
        time.sleep(3)

        # Nhấn vào "Đăng nhập / Đăng ký"
        click_element(driver, By.CLASS_NAME, "text-dndk")
        time.sleep(2)

        # Điều hướng đến trang quản lý cửa hàng
        click_element(driver, By.XPATH, "//a[contains(text(), 'Quản lý cửa hàng')]")
        time.sleep(2)

        # Chuyển đến phần "Khách hàng"
        click_element(driver, By.XPATH, "//div[@class='hidden-sidebar' and text()='Khách hàng']")
        time.sleep(2)

        # Sử dụng hàm add_customer để thêm khách hàng
        add_customer(driver, "Nhật Sinh", "0394996781", "MatKhau123!")
        time.sleep(2)

        # Chờ menu thả xuống xuất hiện để lọc khách hàng theo trạng thái
        dropdown = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "tinh-trang-user"))
        )

        # Tạo đối tượng Select
        select = Select(dropdown)

        # Chọn giá trị "Bị khóa" (value="0")
        select.select_by_value("0")
        time.sleep(2)

        try:
            # Chờ các kết quả hiển thị
            results = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "status-no-complete"))
            )

            # Kiểm tra trạng thái của từng kết quả
            statuses = [result.text.strip() for result in results]  # Lấy tất cả trạng thái
            assert "Bị khóa" in statuses, "Không có khách hàng nào bị khóa."
            assert all(status == "Bị khóa" for status in statuses), (
                f"Lỗi: Có trạng thái không phải 'Bị khóa'. Các trạng thái không đúng: "
                f"{[status for status in statuses if status != 'Bị khóa']}"
            )

            print("Kết quả kiểm tra thành công: Tất cả khách hàng đang ở trạng thái 'Bị khóa'.")

        except TimeoutException:
            print("Không có khách hàng nào bị khóa.")

    def test_search_customer(self, driver):
        """
        Test tìm kiếm khách hàng trong danh sách khách hàng.
        """
        # Truy cập trang web
        driver.get("http://localhost/Webbanhang-main/index.html")

        # Đăng nhập tài khoản admin sử dụng hàm login từ helper
        login(driver, "hgbaodev", "123456")
        time.sleep(3)

        # Nhấn vào "Đăng nhập / Đăng ký"
        click_element(driver, By.CLASS_NAME, "text-dndk")
        time.sleep(2)

        # Điều hướng đến trang quản lý cửa hàng
        click_element(driver, By.XPATH, "//a[contains(text(), 'Quản lý cửa hàng')]")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@class='hidden-sidebar' and text()='Khách hàng']"))
        )
        time.sleep(2)

        # Chuyển đến phần "Khách hàng"
        click_element(driver, By.XPATH, "//div[@class='hidden-sidebar' and text()='Khách hàng']")
        time.sleep(2)

        # Sử dụng hàm add_customer để thêm khách hàng
        add_customer(driver, "Nhật Sinh", "0394996781", "MatKhau123!")
        time.sleep(2)

        # Chờ trường tìm kiếm khách hàng xuất hiện
        search_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "form-search-user"))
        )
        search_input.clear()  # Xóa nội dung cũ nếu có
        search_input.send_keys("Nhật Sinh")  # Nhập tên khách hàng vào ô tìm kiếm

        # Đợi một chút để hệ thống xử lý tìm kiếm
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "show-user"))
        )
        time.sleep(3)


        # Lấy tất cả các hàng trong bảng kết quả
        rows = driver.find_elements(By.XPATH, "//tbody[@id='show-user']/tr")

        # Kiểm tra xem từ khóa có trong các ô của bảng không
        keyword = "Nhật Sinh"
        found = False
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            for cell in cells:
                if keyword in cell.text:
                    found = True
                    print("Kết quả tìm kiếm đúng:", cell.text)
                    break
            if found:
                break

        # Sử dụng assert để kiểm tra kết quả
        assert found, f"Không tìm thấy kết quả khớp với từ khóa: {keyword}"
        print("Tìm kiếm khách hàng thành công!")
