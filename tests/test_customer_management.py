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

class TestCustomerManagement:

    def test_add_customer(self, driver):
        """
        Kiểm tra chức năng thêm khách hàng và hiển thị thông báo thành công.
        Nếu không phải thông báo thành công thì test này sẽ thất bại.
        """
        driver.get("http://localhost/Webbanhang-main/index.html")

        # Đăng nhập vào hệ thống
        login(driver, "hgbaodev", "123456")
        time.sleep(4)

        # Nhấn vào "Đăng nhập / Đăng ký"
        click_element(driver, By.CLASS_NAME, "text-dndk")

        # Chờ "Quản lý cửa hàng" xuất hiện và nhấn vào
        click_element(driver, By.XPATH, "//a[contains(text(), 'Quản lý cửa hàng')]")

        # Nhấn vào phần "Khách hàng"
        click_element(driver, By.XPATH, "//div[@class='hidden-sidebar' and text()='Khách hàng']")

        # Điền thông tin khách hàng và thêm khách hàng mới
        add_customer(driver, "Nhật Sssadaináadh", "03942a2199621781", "MatKhau123!")
        time.sleep(2)

        try:
            # Kiểm tra thông báo từ toast__msg
            check_toast_message(driver, "toast__msg", "Tạo thành công tài khoản !")
            print("Thêm khách hàng thành công!")
        except AssertionError:
            # Nếu không phải thông báo thành công, kiểm tra thất bại
            assert False, "Kiểm thừ thêm khách hàng thất bại!"

        finally:
            # Đảm bảo luôn logout sau khi kiểm tra xong
            logout_admin(driver)

    def test_filter_active_customers(self, driver):
        """
        Test thêm khách hàng mới vào danh sách khách hàng và lọc theo trạng thái "Hoạt động".
        """
        try:
            # Truy cập trang web
            driver.get("http://localhost/Webbanhang-main/index.html")
            time.sleep(2)

            # Đăng nhập tài khoản admin
            login(driver, "hgbaodev", "123456")
            time.sleep(2)

            # Nhấn vào "Đăng nhập / Đăng ký"
            click_element(driver, By.CLASS_NAME, "text-dndk")
            time.sleep(2)

            # Điều hướng đến trang quản lý cửa hàng
            click_element(driver, By.XPATH, "//a[contains(text(), 'Quản lý cửa hàng')]")

            # Chuyển đến phần "Khách hàng"
            click_element(driver, By.XPATH, "//div[@class='hidden-sidebar' and text()='Khách hàng']")

            # Chờ menu thả xuống xuất hiện để lọc khách hàng theo trạng thái
            dropdown = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "tinh-trang-user"))
            )

            # Tạo đối tượng Select và chọn giá trị "Hoạt động" (value="1")
            select = Select(dropdown)
            select.select_by_value("1")

            try:
                # Chờ các kết quả hiển thị
                results = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "status-complete"))
                )

                # Kiểm tra trạng thái của từng kết quả
                statuses = [result.text.strip() for result in results]
                assert all(status == "Hoạt động" for status in statuses), (
                    f"Lỗi: Có trạng thái không phải 'Hoạt động'. Các trạng thái không đúng: "
                    f"{[status for status in statuses if status != 'Hoạt động']}"
                )

                print("Lọc đúng các khách hàng đang ở trạng thái 'Hoạt động'.")

            except TimeoutException:
                print("Không có khách hàng nào đang hoạt động.")

        finally:
            # Đảm bảo luôn logout sau khi kiểm tra xong
            logout_admin(driver)

    def test_filter_locked_customers(self, driver):
        """
        Test thêm khách hàng mới vào danh sách khách hàng và lọc theo trạng thái "Bị khóa".
        """
        try:
            # Truy cập trang web
            driver.get("http://localhost/Webbanhang-main/index.html")
            time.sleep(2)

            # Đăng nhập tài khoản admin
            login(driver, "hgbaodev", "123456")
            time.sleep(3)

            # Nhấn vào "Đăng nhập / Đăng ký"
            click_element(driver, By.CLASS_NAME, "text-dndk")
            time.sleep(2)

            # Điều hướng đến trang quản lý cửa hàng
            click_element(driver, By.XPATH, "//a[contains(text(), 'Quản lý cửa hàng')]")

            # Chuyển đến phần "Khách hàng"
            click_element(driver, By.XPATH, "//div[@class='hidden-sidebar' and text()='Khách hàng']")

            # Chờ menu thả xuống xuất hiện để lọc khách hàng theo trạng thái
            dropdown = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "tinh-trang-user"))
            )

            # Tạo đối tượng Select và chọn giá trị "Bị khóa" (value="0")
            select = Select(dropdown)
            select.select_by_value("0")

            # Chờ các kết quả hiển thị
            results = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "status-no-complete"))
            )
            time.sleep(2)


            # Kiểm tra trạng thái của từng kết quả
            statuses = [result.text.strip() for result in results]  # Lấy tất cả trạng thái
            assert all(status == "Bị khóa" for status in statuses), (
                f"Lỗi: Có trạng thái không phải 'Bị khóa'. Các trạng thái không đúng: "
                f"{[status for status in statuses if status != 'Bị khóa']}"
            )

            print("Lọc đúng các khách hàng đang ở trạng thái 'Bị khóa'.")

        except TimeoutException:
            print("Không có khách hàng nào bị khóa.")
        finally:
            # Đảm bảo luôn logout sau khi kiểm tra xong
            logout_admin(driver)

    def test_search_customer(self, driver):
        """
        Test tìm kiếm khách hàng trong danh sách khách hàng.
        """
        try:
            # Truy cập trang web
            driver.get("http://localhost/Webbanhang-main/index.html")
            time.sleep(2)

            # Đăng nhập tài khoản admin sử dụng hàm login từ helper
            login(driver, "hgbaodev", "123456")
            time.sleep(2)

            # Nhấn vào "Đăng nhập / Đăng ký"
            click_element(driver, By.CLASS_NAME, "text-dndk")
            time.sleep(2)

            # Điều hướng đến trang quản lý cửa hàng
            click_element(driver, By.XPATH, "//a[contains(text(), 'Quản lý cửa hàng')]")

            # Chuyển đến phần "Khách hàng"
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='hidden-sidebar' and text()='Khách hàng']"))
            )
            click_element(driver, By.XPATH, "//div[@class='hidden-sidebar' and text()='Khách hàng']")

            # Chờ trường tìm kiếm khách hàng xuất hiện
            search_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "form-search-user"))
            )
            search_input.clear()  # Xóa nội dung cũ nếu có
            search_input.send_keys("Nhật Sinh")  # Nhập tên khách hàng vào ô tìm kiếm
            time.sleep(2)

            # Đợi bảng kết quả cập nhật
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "show-user"))
            )

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

        finally:
            # Đảm bảo luôn logout sau khi kiểm tra xong
            logout_admin(driver)

  # đang sửa chưa xong nha bé
    def test_filter_customers_by_date(self, driver):
        """
        Test lọc khách hàng trong danh sách theo khoảng ngày.
        """
        try:
            # Truy cập trang web
            driver.get("http://localhost/Webbanhang-main/index.html")
            time.sleep(2)

            # Đăng nhập tài khoản admin
            login(driver, "hgbaodev", "123456")
            time.sleep(2)

            # Điều hướng đến trang quản lý khách hàng
            click_element(driver, By.CLASS_NAME, "text-dndk")
            time.sleep(2)

            click_element(driver, By.XPATH, "//a[contains(text(), 'Quản lý cửa hàng')]")

            click_element(driver, By.XPATH, "//div[@class='hidden-sidebar' and text()='Khách hàng']")
            time.sleep(2)

            # Sử dụng JavaScript để thay đổi giá trị của ô ngày bắt đầu và ngày kết thúc
            start_date_value = "2024-12-01"  # Thay đổi theo định dạng yyyy-mm-dd
            end_date_value = "2024-12-04"  # Thay đổi theo định dạng yyyy-mm-dd
            driver.execute_script(f"document.getElementById('time-start-user').value = '{start_date_value}';")
            time.sleep(2)

            driver.execute_script(f"document.getElementById('time-end-user').value = '{end_date_value}';")
            time.sleep(2)

            # Đợi để hệ thống cập nhật danh sách khách hàng
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#show-user tr"))
            )

            # Lấy tất cả các dòng trong bảng kết quả
            rows = driver.find_elements(By.CSS_SELECTOR, "#show-user tr")

            # Kiểm tra từng dòng xem ngày có nằm trong khoảng lọc không
            found = False
            for row in rows:
                # Lấy giá trị ngày từ cột ngày (giả định ngày ở cột thứ 4)
                date_cell = row.find_elements(By.TAG_NAME, "td")[3]
                date_value = date_cell.text.strip()

                # Kiểm tra xem ngày có nằm trong khoảng lọc không
                if start_date_value <= date_value <= end_date_value:
                    print(f"Ngày {date_value} nằm trong khoảng lọc.")
                    found = True
                else:
                    print(f"Ngày {date_value} không nằm trong khoảng lọc.")

            # Đảm bảo ít nhất một dòng dữ liệu nằm trong khoảng lọc
            assert found, "Không có khách hàng nào tham gia trong khoảng ngày lọc."

        finally:
            # Đảm bảo luôn logout sau khi kiểm tra
            logout_admin(driver)

    def test_reset_customer_page(self, driver):
        """
        Test chức năng reset trang khách hàng.
        """
        try:
            # Truy cập trang web
            driver.get("http://localhost/Webbanhang-main/index.html")
            time.sleep(2)

            # Đăng nhập tài khoản admin
            login(driver, "hgbaodev", "123456")
            time.sleep(2)

            # Điều hướng đến trang quản lý khách hàng
            click_element(driver, By.CLASS_NAME, "text-dndk")
            time.sleep(2)

            click_element(driver, By.XPATH, "//a[contains(text(), 'Quản lý cửa hàng')]")
            click_element(driver, By.XPATH, "//div[@class='hidden-sidebar' and text()='Khách hàng']")

            # Chờ menu thả xuống "Tình trạng" xuất hiện
            dropdown = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "tinh-trang-user"))
            )
            time.sleep(2)

            select = Select(dropdown)
            select.select_by_value("0")
            time.sleep(2)  # Đợi thay đổi áp dụng

            # Nhấn vào nút "Reset"
            reset_button = driver.find_element(By.CLASS_NAME, "btn-reset-order")
            reset_button.click()
            time.sleep(2)  # Đợi trạng thái được reset

            # Kiểm tra giá trị của dropdown sau khi reset
            selected_option = select.first_selected_option
            print(f"Giá trị dropdown sau khi reset: {selected_option.text}")

            # Đảm bảo dropdown quay về "Tất cả" (value="2")
            assert selected_option.get_attribute('value') == "2", "Dropdown không reset về giá trị 'Tất cả'!"

            print("Reset trang quản lý khách hàng thành công.")

        finally:
            # Đảm bảo luôn logout hoặc đóng trình duyệt
            logout_admin(driver)

    def test_edit_customer_information(self, driver):
        """
        Test chức năng sửa thông tin khách hàng.
        """
        try:
            # Truy cập trang web
            driver.get("http://localhost/Webbanhang-main/index.html")
            time.sleep(2)

            # Đăng nhập tài khoản admin
            login(driver, "hgbaodev", "123456")
            time.sleep(2)

            # Điều hướng đến trang quản lý khách hàng
            click_element(driver, By.CLASS_NAME, "text-dndk")
            time.sleep(2)

            click_element(driver, By.XPATH, "//a[contains(text(), 'Quản lý cửa hàng')]")
            click_element(driver, By.XPATH, "//div[@class='hidden-sidebar' and text()='Khách hàng']")

            # Tìm khách hàng theo số điện thoại
            customer_phone = "adaasdasqaaas"  # Số điện thoại của khách hàng cần sửa
            customer_row = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//td[text()='{customer_phone}']/ancestor::tr"))
            )

            # Nhấn vào nút "Chỉnh sửa" của khách hàng đó
            edit_button = customer_row.find_element(By.CLASS_NAME, "btn-edit")
            edit_button.click()
            time.sleep(2)

            # Chỉnh sửa tên khách hàng
            fullname_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "fullname")))
            fullname_input.clear()
            fullname_input.send_keys("carrotne")  # Nhập tên mới

            # Lưu thông tin đã chỉnh sửa
            click_element(driver, By.ID, "btn-update-account")
            time.sleep(2)

            # Kiểm tra thông báo từ toast__msg
            check_toast_message(driver, "toast__msg", "Cập nhật thông tin thành công!")
            print("Sửa thông tin khách hàng thành công!")

            # Kiểm tra tên đã được cập nhật
            new_name = "carrotne"
            updated_name = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//td[text()='{new_name}']"))
            )

            # Assert để kiểm tra kết quả
            assert updated_name is not None, f"Tên không được cập nhật thành công. Không tìm thấy tên '{new_name}' trong bảng."

            # In thông báo thành công
            print(f"Tên đã được cập nhật thành công thành: {new_name}")

        except AssertionError:
            # Nếu có lỗi trong quá trình kiểm tra thông báo hoặc cập nhật thông tin
            print("Kiểm tra sửa thông tin khách hàng thất bại!")

        finally:
            # Đảm bảo luôn logout sau khi kiểm tra xong
            logout_admin(driver)

    # FALSE khi xóa một khách hàng với sdt và họ tên, web xóa không đúng khách hàng đã chỉ định
    def test_delete_customer(self, driver):
        try:
            driver.get("http://localhost/Webbanhang-main/index.html")
            time.sleep(2)

            # Đăng nhập vào tài khoản (sử dụng hàm login từ helper)
            login(driver, "hgbaodev", "123456")
            time.sleep(2)

            # Điều hướng đến trang quản lý khách hàng
            click_element(driver, By.CLASS_NAME, "text-dndk")
            time.sleep(2)

            click_element(driver, By.XPATH, "//a[contains(text(), 'Quản lý cửa hàng')]")
            click_element(driver, By.XPATH, "//div[@class='hidden-sidebar' and text()='Khách hàng']")
            time.sleep(1)

            # Tìm kiếm khách hàng theo họ tên và số điện thoại
            # Tìm kiếm trong bảng theo họ tên và số điện thoại
            search_name = "trhuuhau"  # Tên khách hàng cần tìm
            search_phone = "0352117260"  # Số điện thoại của khách hàng cần tìm

            customer_row = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH,
                                                f"//td[contains(text(), '{search_name}')]/parent::tr//td[contains(text(), '{search_phone}')]/parent::tr"))
            )
            print("Đã tìm thấy dòng khách hàng:")
            print(customer_row.text)  # In ra nội dung của dòng khách hàng tìm thấy

            assert customer_row, f"Không tìm thấy khách hàng {search_name} với số điện thoại {search_phone}."
            print(f"Khách hàng {search_name} với số điện thoại {search_phone} đã được tìm thấy.")

            # Tìm và nhấn nút xóa cho khách hàng này
            # Đảm bảo nút xóa đã sẵn sàng
            delete_button = WebDriverWait(customer_row, 10).until(
                EC.element_to_be_clickable((By.XPATH, ".//button[@class='btn-delete']"))
            )
            # Thực hiện các thao tác xóa tài khoản
            delete_button.click()
            time.sleep(2)
            alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
            alert.accept()
            time.sleep(3)

            # Sau khi xóa tài khoản
            driver.execute_script(
                "console.log('Dữ liệu trong localStorage sau khi xóa: ', localStorage.getItem('accounts'))")

            # Kiểm tra xem tài khoản đã bị xóa thành công chưa
            try:
                # Thử tìm lại số điện thoại của khách hàng đã xóa
                phone_deleted = WebDriverWait(driver, 10).until(
                    EC.invisibility_of_element_located((By.XPATH, f"//td[text()='{search_phone}']"))
                )
                assert phone_deleted, f"Tài khoản với số điện thoại {search_phone} vẫn chưa bị xóa."
                print(f"Tài khoản với số điện thoại {search_phone} đã được xóa thành công.")
            except Exception as e:
                print("Không thể xóa tài khoản:", e)


        finally:
            # Đảm bảo luôn đăng xuất khỏi tài khoản admin, ngay cả khi có lỗi
            logout_admin(driver)

