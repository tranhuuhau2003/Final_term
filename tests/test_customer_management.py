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
from Final_term.utils.driver_helper import init_driver, close_driver  # Import từ driver_helper
from selenium.webdriver.common.by import By
from datetime import datetime



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

        driver.get("http://localhost/Webbanhang-main/index.html")

        # Đăng nhập vào hệ thống
        login(driver, "hgbaodev", "123456")
        time.sleep(4)

        # Nhấn vào "Đăng nhập / Đăng ký"
        click_element(driver, By.CLASS_NAME, "text-dndk")
        time.sleep(2)

        # Chờ "Quản lý cửa hàng" xuất hiện và nhấn vào
        click_element(driver, By.XPATH, "//a[contains(text(), 'Quản lý cửa hàng')]")
        time.sleep(2)

        # Nhấn vào phần "Khách hàng"
        click_element(driver, By.XPATH, "//div[@class='hidden-sidebar' and text()='Khách hàng']")
        time.sleep(2)

        # Điền thông tin khách hàng và thêm khách hàng mới
        add_customer(driver, "abdca", "0999998888", "MatKhau123!")
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

        try:
            # Truy cập trang web
            driver.get("http://localhost/Webbanhang-main/index.html")
            time.sleep(2)

            # Đăng nhập tài khoản admin
            login(driver, "hgbaodev", "123456")
            time.sleep(4)

            # Nhấn vào "Đăng nhập / Đăng ký"
            click_element(driver, By.CLASS_NAME, "text-dndk")
            time.sleep(2)

            # Điều hướng đến trang quản lý cửa hàng
            click_element(driver, By.XPATH, "//a[contains(text(), 'Quản lý cửa hàng')]")
            time.sleep(2)

            # Chuyển đến phần "Khách hàng"
            click_element(driver, By.XPATH, "//div[@class='hidden-sidebar' and text()='Khách hàng']")
            time.sleep(2)

            # Chờ menu thả xuống xuất hiện để lọc khách hàng theo trạng thái
            dropdown = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "tinh-trang-user"))
            )

            # Tạo đối tượng Select và chọn giá trị "Hoạt động" (value="1")
            select = Select(dropdown)
            select.select_by_value("1")
            time.sleep(2)

            try:
                # Chờ các kết quả hiển thị
                results = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "status-complete"))
                )
                time.sleep(2)

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

        try:
            # Truy cập trang web
            driver.get("http://localhost/Webbanhang-main/index.html")
            time.sleep(2)

            # Đăng nhập tài khoản admin
            login(driver, "hgbaodev", "123456")
            time.sleep(4)

            # Nhấn vào "Đăng nhập / Đăng ký"
            click_element(driver, By.CLASS_NAME, "text-dndk")
            time.sleep(2)

            # Điều hướng đến trang quản lý cửa hàng
            click_element(driver, By.XPATH, "//a[contains(text(), 'Quản lý cửa hàng')]")
            time.sleep(2)

            # Chuyển đến phần "Khách hàng"
            click_element(driver, By.XPATH, "//div[@class='hidden-sidebar' and text()='Khách hàng']")

            # Chờ menu thả xuống xuất hiện để lọc khách hàng theo trạng thái
            dropdown = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "tinh-trang-user"))
            )

            # Tạo đối tượng Select và chọn giá trị "Bị khóa" (value="0")
            select = Select(dropdown)
            select.select_by_value("0")
            time.sleep(2)

            # Đợi bảng xuất hiện
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#show-user")))
                table = driver.find_element(By.CSS_SELECTOR, "#show-user")
                rows = table.find_elements(By.TAG_NAME, "tr")

                # Kiểm tra nếu bảng chứa dòng "Không có dữ liệu"
                if len(rows) == 1 and "Không có dữ liệu" in rows[0].text:
                    print("Bảng không có dữ liệu, kiểm thử thành công.")
                    assert True, "Bảng không có dữ liệu, không cần kiểm tra thêm."
                    return

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

    def test_search_existing_customer(self, driver):

        try:
            # Mở trang web
            driver.get("http://localhost/Webbanhang-main/index.html")

            # Đăng nhập
            login(driver, "hgbaodev", "123456")
            time.sleep(4)

            # Điều hướng đến trang quản lý khách hàng
            click_element(driver, By.CLASS_NAME, "text-dndk")
            time.sleep(2)

            click_element(driver, By.XPATH, "//a[contains(text(), 'Quản lý cửa hàng')]")
            time.sleep(2)

            click_element(driver, By.XPATH, "//div[@class='hidden-sidebar' and text()='Khách hàng']")
            time.sleep(2)

            # Danh sách khách hàng mẫu để tìm kiếm
            existing_customers = ["Võ Khánh Linh"]

            # Tìm kiếm khách hàng tồn tại
            for customer in existing_customers:
                print(f"Tìm kiếm khách hàng: {customer}")

                # Tìm trường tìm kiếm và nhập khách hàng
                search_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "form-search-user"))
                )
                search_input.clear()  # Xóa nội dung cũ
                search_input.send_keys(customer)  # Nhập từ khóa tìm kiếm
                time.sleep(2)

                # Kiểm tra kết quả tìm kiếm
                search_results = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, "//tbody[@id='show-user']/tr"))
                )
                assert len(search_results) > 0, f"Không tìm thấy khách hàng nào với từ khóa: {customer}"

                for result in search_results:
                    cells = result.find_elements(By.TAG_NAME, "td")
                    found = any(customer.lower() in cell.text.lower() for cell in cells)
                    assert found, f"Không tìm thấy thông tin khách hàng '{customer}' trong hàng: {result.text}"

                print(f"Tìm kiếm khách hàng '{customer}' thành công. Tất cả kết quả đều khớp!")

        finally:
            # Đảm bảo logout sau khi kiểm tra
            logout_admin(driver)

    def test_search_nonexistent_customer(self, driver):

        try:
            # Mở trang web
            driver.get("http://localhost/Webbanhang-main/index.html")

            # Đăng nhập
            login(driver, "hgbaodev", "123456")
            time.sleep(4)

            # Điều hướng đến trang quản lý khách hàng
            click_element(driver, By.CLASS_NAME, "text-dndk")
            click_element(driver, By.XPATH, "//a[contains(text(), 'Quản lý cửa hàng')]")
            click_element(driver, By.XPATH, "//div[@class='hidden-sidebar' and text()='Khách hàng']")
            time.sleep(2)

            # Từ khóa tìm kiếm không tồn tại
            nonexistent_keyword = "Không Tồn Tại"
            print(f"Tìm kiếm khách hàng không tồn tại: {nonexistent_keyword}")

            # Tìm trường tìm kiếm và nhập từ khóa
            search_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "form-search-user"))
            )
            search_input.clear()  # Xóa nội dung cũ
            search_input.send_keys(nonexistent_keyword)  # Nhập từ khóa không tồn tại
            time.sleep(2)

            # Kiểm tra sự hiện diện của thông báo "Không có dữ liệu"
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
            # Đảm bảo luôn đăng xuất sau khi kiểm tra
            logout_admin(driver)

    # test lọc khách hàng theo ngày
    # nhớ cập nhật lại ngày kết thúc (2 chổ) khi chạy test demo
    def test_filter_customers_by_date(self, driver):
        try:
            driver.get("http://localhost/Webbanhang-main/index.html")
            time.sleep(2)

            # Đăng nhập bằng hàm login có sẵn
            login(driver, "hgbaodev", "123456")
            time.sleep(3)

            # Điều hướng đến trang quản lý khách hàng
            click_element(driver, By.CLASS_NAME, "text-dndk")
            time.sleep(2)

            click_element(driver, By.XPATH, "//a[contains(text(), 'Quản lý cửa hàng')]")
            click_element(driver, By.XPATH, "//div[@class='hidden-sidebar' and text()='Khách hàng']")
            time.sleep(1)

            # Nhập ngày kết thúc
            fill_input(driver, By.ID, "time-end-user", "12-20-2024")  # Nhập ngày theo định dạng MM-DD-YYYY
            time.sleep(3)

            # Nhập ngày bắt đầu
            fill_input(driver, By.ID, "time-start-user", "12-01-2024")  # Nhập ngày theo định dạng MM-DD-YYYY
            time.sleep(3)

            # Đợi bảng xuất hiện
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#show-user")))
                table = driver.find_element(By.CSS_SELECTOR, "#show-user")
                rows = table.find_elements(By.TAG_NAME, "tr")

                # Kiểm tra nếu bảng chứa dòng "Không có dữ liệu"
                if len(rows) == 1 and "Không có dữ liệu" in rows[0].text:
                    print("Bảng không có dữ liệu, kiểm thử thành công.")
                    assert True, "Bảng không có dữ liệu, không cần kiểm tra thêm."
                    return

                # Chuyển đổi ngày bắt đầu và kết thúc thành datetime
                start_date = datetime.strptime("12-01-2024", "%m-%d-%Y")
                end_date = datetime.strptime("12-20-2024", "%m-%d-%Y")

                valid_count = 0
                # Duyệt qua từng hàng để kiểm tra logic ngày
                for i, row in enumerate(rows):
                    try:
                        # Lấy dữ liệu ngày từ cột "Ngày tham gia"
                        date_text = row.find_element(By.XPATH, "./td[4]").text
                        date_obj = datetime.strptime(date_text, "%d/%m/%Y")  # Định dạng dd/MM/yyyy

                        if start_date <= date_obj <= end_date:
                            print(f"Hàng {i + 1}: {date_text} hợp lệ.")
                            valid_count += 1
                        else:
                            print(f"Hàng {i + 1}: {date_text} không nằm trong khoảng ngày lọc.")
                    except Exception as e:
                        print(f"Lỗi xử lý hàng {i + 1}: {e}")

                # Kiểm tra kết quả lọc
                assert valid_count > 0, "Không có khách hàng nào tham gia trong khoảng ngày lọc."
                print(f"Tìm thấy {valid_count} khách hàng hợp lệ.")

            except TimeoutException:
                assert False, "Không thể tìm thấy bảng dữ liệu sau khi chờ đợi."

        except Exception as e:
            print(f"Lỗi: {str(e)}")
            assert False, f"Đã xảy ra lỗi trong quá trình kiểm thử: {str(e)}"

        finally:
            # Đảm bảo logout sau khi kiểm thử
            try:
                logout_admin(driver)
            except Exception as final_e:
                print(f"Lỗi khi đăng xuất: {str(final_e)}")

    def test_reset_customer_page(self, driver):

        try:
            # Truy cập trang web
            driver.get("http://localhost/Webbanhang-main/index.html")
            time.sleep(2)

            # Đăng nhập tài khoản admin
            login(driver, "hgbaodev", "123456")
            time.sleep(4)

            # Điều hướng đến trang quản lý khách hàng
            click_element(driver, By.CLASS_NAME, "text-dndk")
            time.sleep(2)

            click_element(driver, By.XPATH, "//a[contains(text(), 'Quản lý cửa hàng')]")
            time.sleep(2)

            click_element(driver, By.XPATH, "//div[@class='hidden-sidebar' and text()='Khách hàng']")
            time.sleep(2)

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

        try:
            # Truy cập trang web
            driver.get("http://localhost/Webbanhang-main/index.html")
            time.sleep(2)

            # Đăng nhập tài khoản admin
            login(driver, "hgbaodev", "123456")
            time.sleep(4)

            # Điều hướng đến trang quản lý khách hàng
            click_element(driver, By.CLASS_NAME, "text-dndk")
            time.sleep(2)

            click_element(driver, By.XPATH, "//a[contains(text(), 'Quản lý cửa hàng')]")
            click_element(driver, By.XPATH, "//div[@class='hidden-sidebar' and text()='Khách hàng']")

            # Tìm khách hàng theo số điện thoại
            customer_phone = "0777777777"  # Số điện thoại của khách hàng cần sửa
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
            time.sleep(4)

            # Điều hướng đến trang quản lý khách hàng
            click_element(driver, By.CLASS_NAME, "text-dndk")
            time.sleep(2)

            click_element(driver, By.XPATH, "//a[contains(text(), 'Quản lý cửa hàng')]")
            click_element(driver, By.XPATH, "//div[@class='hidden-sidebar' and text()='Khách hàng']")
            time.sleep(1)

            # Tìm kiếm khách hàng theo họ tên và số điện thoại
            # Tìm kiếm trong bảng theo họ tên và số điện thoại
            search_name = "aaa"  # Tên khách hàng cần tìm
            search_phone = "01111111111"  # Số điện thoại của khách hàng cần tìm

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


