import datetime
import time
from datetime import datetime

import pytest
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from Final_term.utils.driver_helper import init_driver, close_driver  # Import từ driver_helper
from Final_term.utils.helper import click_element, fill_input, check_toast_message, login, \
    add_customer, logout_admin, navigate_to_product_customer, clear_and_send_keys, select_dropdown_option


@pytest.fixture
def driver():
    """
    Khởi tạo WebDriver và đóng WebDriver sau khi test xong.
    """
    driver = init_driver()  # Gọi hàm khởi tạo driver từ file driver_helper
    yield driver  # Cung cấp driver cho test
    close_driver(driver)  # Đóng driver sau khi test xong

class TestCustomerManagement:

    def test_add_customer(self, driver):
        navigate_to_product_customer(driver, "hgbaodev", "123456")

        add_customer(driver, "abdcaa", "0999993778", "MatKhau123!")

        try:
            result = check_toast_message(driver, "toast__msg", "Tạo thành công tài khoản !")
            assert result, "Không nhận được thông báo Tạo thành công tài khoản ."
            print("Thêm khách hàng thành công!")

        finally:
            logout_admin(driver)

    def test_filter_active_customers(self, driver):
        try:
            navigate_to_product_customer(driver, "hgbaodev", "123456")
            dropdown = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "tinh-trang-user")))

            select = Select(dropdown)
            select.select_by_value("1")
            time.sleep(2)

            try:
                results = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "status-complete")))
                time.sleep(2)

                statuses = [result.text.strip() for result in results]
                assert all(status == "Hoạt động" for status in statuses), (
                    f"Lỗi: Có trạng thái không phải 'Hoạt động'. Các trạng thái không đúng: "
                    f"{[status for status in statuses if status != 'Hoạt động']}"
                )

                print("Lọc đúng các khách hàng đang ở trạng thái 'Hoạt động'.")

            except TimeoutException:
                print("Không có khách hàng nào đang hoạt động.")

        finally:
            logout_admin(driver)

    def test_filter_locked_customers(self, driver):
        try:
            navigate_to_product_customer(driver, "hgbaodev", "123456")
            dropdown = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "tinh-trang-user")))

            select = Select(dropdown)
            select.select_by_value("0")
            time.sleep(2)

            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#show-user")))
                table = driver.find_element(By.CSS_SELECTOR, "#show-user")
                rows = table.find_elements(By.TAG_NAME, "tr")

                if len(rows) == 1 and "Không có dữ liệu" in rows[0].text:
                    print("Bảng không có dữ liệu, kiểm thử thành công.")
                    assert True, "Bảng không có dữ liệu, không cần kiểm tra thêm."
                    return

                results = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "status-no-complete")))
                time.sleep(2)

                statuses = [result.text.strip() for result in results]
                assert all(status == "Bị khóa" for status in statuses), (
                    f"Lỗi: Có trạng thái không phải 'Bị khóa'. Các trạng thái không đúng: "
                    f"{[status for status in statuses if status != 'Bị khóa']}"
                )

                print("Lọc đúng các khách hàng đang ở trạng thái 'Bị khóa'.")

            except TimeoutException:
                print("Không có khách hàng nào bị khóa.")

        finally:
            logout_admin(driver)

    def test_search_existing_customer(self, driver):
        try:
            navigate_to_product_customer(driver, "hgbaodev", "123456")
            existing_customers = ["Võ Khánh Linh"]

            for customer in existing_customers:
                print(f"Tìm kiếm khách hàng: {customer}")
                clear_and_send_keys(driver, By.ID, "form-search-user", customer)

                search_results = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//tbody[@id='show-user']/tr")))
                assert len(search_results) > 0, f"Không tìm thấy khách hàng nào với từ khóa: {customer}"

                for result in search_results:
                    cells = result.find_elements(By.TAG_NAME, "td")
                    found = any(customer.lower() in cell.text.lower() for cell in cells)
                    assert found, f"Không tìm thấy thông tin khách hàng '{customer}' trong hàng: {result.text}"

                print(f"Tìm kiếm khách hàng '{customer}' thành công. Tất cả kết quả đều khớp!")

        finally:
            logout_admin(driver)

    def test_search_nonexistent_customer(self, driver):
        try:
            navigate_to_product_customer(driver, "hgbaodev", "123456")

            # Từ khóa tìm kiếm không tồn tại
            nonexistent_keyword = "Không Tồn Tại"
            print(f"Tìm kiếm khách hàng không tồn tại: {nonexistent_keyword}")
            clear_and_send_keys(driver, By.ID, "form-search-user", nonexistent_keyword)

            try:
                no_data_message = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//tbody[@id='show-user']/tr/td[@colspan='5' and text()='Không có dữ liệu']"))
                )
                assert no_data_message.is_displayed(), "Thông báo 'Không có dữ liệu' không được hiển thị khi không tìm thấy kết quả."
                print("Thông báo 'Không có dữ liệu' hiển thị chính xác.")
            except Exception as e:
                print(f"Lỗi khi kiểm tra thông báo 'Không có dữ liệu': {e}")
                raise

        finally:
            logout_admin(driver)

    # test lọc khách hàng theo ngày
    # nhớ cập nhật lại ngày kết thúc (2 chổ) khi chạy test demo
    def test_filter_customers_by_date(self, driver):
        try:
            navigate_to_product_customer(driver, "hgbaodev", "123456")

            fill_input(driver, By.ID, "time-end-user", "12-25-2024")  # Nhập ngày theo định dạng MM-DD-YYYY
            time.sleep(3)

            fill_input(driver, By.ID, "time-start-user", "12-01-2024")  # Nhập ngày theo định dạng MM-DD-YYYY
            time.sleep(3)

            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#show-user")))
                table = driver.find_element(By.CSS_SELECTOR, "#show-user")
                rows = table.find_elements(By.TAG_NAME, "tr")

                if len(rows) == 1 and "Không có dữ liệu" in rows[0].text:
                    print("Bảng không có dữ liệu, kiểm thử thành công.")
                    assert True, "Bảng không có dữ liệu, không cần kiểm tra thêm."
                    return

                start_date = datetime.strptime("12-01-2024", "%m-%d-%Y")
                end_date = datetime.strptime("12-25-2024", "%m-%d-%Y")

                valid_count = 0
                for i, row in enumerate(rows):
                    try:
                        date_text = row.find_element(By.XPATH, "./td[4]").text
                        date_obj = datetime.strptime(date_text, "%d/%m/%Y")  # Định dạng dd/MM/yyyy

                        if start_date <= date_obj <= end_date:
                            print(f"Hàng {i + 1}: {date_text} hợp lệ.")
                            valid_count += 1
                        else:
                            print(f"Hàng {i + 1}: {date_text} không nằm trong khoảng ngày lọc.")
                    except Exception as e:
                        print(f"Lỗi xử lý hàng {i + 1}: {e}")

                assert valid_count > 0, "Không có khách hàng nào tham gia trong khoảng ngày lọc."
                print(f"Tìm thấy {valid_count} khách hàng hợp lệ.")

            except TimeoutException:
                assert False, "Không thể tìm thấy bảng dữ liệu sau khi chờ đợi."

        finally:
            logout_admin(driver)

    def test_reset_customer_page(self, driver):

        try:
            navigate_to_product_customer(driver, "hgbaodev", "123456")

            # Chờ menu thả xuống "Tình trạng" xuất hiện
            dropdown = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "tinh-trang-user")))
            time.sleep(2)

            select = Select(dropdown)
            select.select_by_value("0")
            time.sleep(2)

            click_element(driver, By.CLASS_NAME, "btn-reset-order")
            time.sleep(2)

            selected_option = select.first_selected_option
            print(f"Giá trị dropdown sau khi reset: {selected_option.text}")

            assert selected_option.get_attribute('value') == "2", "Dropdown không reset về giá trị 'Tất cả'!"

            print("Reset trang quản lý khách hàng thành công.")

        finally:
            logout_admin(driver)

    def test_edit_customer_information(self, driver):
        try:
            navigate_to_product_customer(driver, "hgbaodev", "123456")

            customer_phone = "0777777777"  # Số điện thoại của khách hàng cần sửa
            customer_row = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, f"//td[text()='{customer_phone}']/ancestor::tr")))

            click_element(driver, By.CLASS_NAME, "btn-edit")

            fill_input(driver, By.ID, "fullname","carrotne" )
            click_element(driver, By.ID, "btn-update-account")
            time.sleep(2)

            result = check_toast_message(driver, "toast__msg", "Cập nhật thông tin thành công!")
            assert result, "Không nhận được thông báo Cập nhật thông tin thành công!"
            print("Sửa thông tin khách hàng thành công!")

            new_name = "carrotne"
            updated_name = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, f"//td[text()='{new_name}']")))

            assert updated_name is not None, f"Tên không được cập nhật thành công. Không tìm thấy tên '{new_name}' trong bảng."
            print(f"Tên đã được cập nhật thành công thành: {new_name}")

        finally:
            logout_admin(driver)

    # FALSE khi xóa một khách hàng với sdt và họ tên, web xóa không đúng khách hàng đã chỉ định
    def test_delete_customer(self, driver):
        try:
            navigate_to_product_customer(driver, "hgbaodev", "123456")

            search_name = "Nguyễn Văn ABC"
            search_phone = "0123456999"

            customer_row = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,
                                                f"//td[contains(text(), '{search_name}')]/parent::tr//td[contains(text(), '{search_phone}')]/parent::tr")))
            print("Đã tìm thấy dòng khách hàng:")
            print(customer_row.text)

            assert customer_row, f"Không tìm thấy khách hàng {search_name} với số điện thoại {search_phone}."
            print(f"Khách hàng {search_name} với số điện thoại {search_phone} đã được tìm thấy.")


            delete_button = WebDriverWait(customer_row, 10).until( EC.element_to_be_clickable((By.XPATH, ".//button[@class='btn-delete']")) )
            delete_button.click()
            time.sleep(2)
            alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
            alert.accept()
            time.sleep(3)


            try:
                WebDriverWait(driver, 10).until(
                    EC.invisibility_of_element_located((By.XPATH, f"//td[text()='{search_phone}']"))
                )

                print(f"Tài khoản với số điện thoại {search_phone} đã được xóa thành công.")
            except Exception:
                assert False, f"Tài khoản với số điện thoại {search_phone} vẫn chưa bị xóa."

        finally:
            logout_admin(driver)
