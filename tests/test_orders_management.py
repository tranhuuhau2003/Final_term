import datetime
import time

from selenium.common import TimeoutException, StaleElementReferenceException
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


class TestOrdersManagement:
    def test_search_order_by_id(self, driver):
        """
        Kiểm tra tìm kiếm đơn hàng theo mã đơn hàng.
        """
        try:
            # Mở trang web
            driver.get("http://localhost/Webbanhang-main/index.html")

            # Đăng nhập
            login(driver, "hgbaodev", "123456")
            time.sleep(4)

            # Nhấn vào "Đăng nhập / Đăng ký"
            click_element(driver, By.CLASS_NAME, "text-dndk")

            # Điều hướng đến trang quản lý đơn hàng
            click_element(driver, By.XPATH, "//a[contains(text(), 'Quản lý cửa hàng')]")
            click_element(driver, By.XPATH, "//div[@class='hidden-sidebar' and text()='Đơn hàng']")

            # Danh sách mã đơn hàng mẫu để tìm kiếm
            order_ids = ["DH1", "DH2"]

            # Tìm kiếm đơn hàng theo mã
            for order_id in order_ids:
                print(f"Tìm kiếm đơn hàng với mã: {order_id}")

                # Nhập mã đơn hàng vào trường tìm kiếm
                search_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "form-search-order"))
                )
                search_input.clear()
                search_input.send_keys(order_id)
                time.sleep(2)  # Chờ kết quả hiển thị

                # Kiểm tra kết quả hiển thị
                orders = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located(
                        (By.XPATH, f"//tbody[@id='showOrder']/tr[td[text()='{order_id}']]"))
                )
                assert len(orders) > 0, f"Không tìm thấy đơn hàng với mã: {order_id}"

                print(f"Tìm kiếm đơn hàng '{order_id}' thành công. Kết quả hiển thị đúng!")

        finally:
            # Đảm bảo logout sau khi kiểm tra
            logout_admin(driver)

    def test_search_order_by_customer(self, driver):
        """
        Kiểm tra tìm kiếm đơn hàng theo tên khách hàng.
        """
        try:
            # Mở trang web
            driver.get("http://localhost/Webbanhang-main/index.html")

            # Đăng nhập
            login(driver, "hgbaodev", "123456")
            time.sleep(4)

            # Nhấn vào "Đăng nhập / Đăng ký"
            click_element(driver, By.CLASS_NAME, "text-dndk")

            # Điều hướng đến trang quản lý đơn hàng
            click_element(driver, By.XPATH, "//a[contains(text(), 'Quản lý cửa hàng')]")
            click_element(driver, By.XPATH, "//div[@class='hidden-sidebar' and text()='Đơn hàng']")

            # Danh sách tên khách hàng mẫu để tìm kiếm
            customers = ["0123456789"]

            # Tìm kiếm đơn hàng theo tên khách hàng
            for customer in customers:
                print(f"Tìm kiếm đơn hàng với khách hàng: {customer}")

                # Nhập tên khách hàng vào trường tìm kiếm
                search_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "form-search-order"))
                )
                search_input.clear()
                search_input.send_keys(customer)
                time.sleep(2)  # Chờ kết quả hiển thị

                # Kiểm tra kết quả hiển thị
                orders = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located(
                        (By.XPATH, f"//tbody[@id='showOrder']/tr[td[text()='{customer}']]"))
                )
                assert len(orders) > 0, f"Không tìm thấy đơn hàng với khách hàng: {customer}"

                print(f"Tìm kiếm đơn hàng với khách hàng '{customer}' thành công. Kết quả hiển thị đúng!")

        finally:
            # Đảm bảo logout sau khi kiểm tra
            logout_admin(driver)

    def test_search_nonexistent_order(self, driver):
        """
        Kiểm tra tìm kiếm đơn hàng với từ khóa không tồn tại.
        """
        try:
            # Mở trang web
            driver.get("http://localhost/Webbanhang-main/index.html")

            # Đăng nhập
            login(driver, "hgbaodev", "123456")
            time.sleep(4)

            # Nhấn vào "Đăng nhập / Đăng ký"
            click_element(driver, By.CLASS_NAME, "text-dndk")

            # Điều hướng đến trang quản lý đơn hàng
            click_element(driver, By.XPATH, "//a[contains(text(), 'Quản lý cửa hàng')]")
            click_element(driver, By.XPATH, "//div[@class='hidden-sidebar' and text()='Đơn hàng']")

            # Từ khóa không tồn tại
            nonexistent_keywords = ["INVALID_ID", "UNKNOWN_CUSTOMER"]

            for keyword in nonexistent_keywords:
                print(f"Tìm kiếm với từ khóa không tồn tại: {keyword}")

                # Nhập từ khóa không tồn tại vào trường tìm kiếm
                search_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "form-search-order"))
                )
                search_input.clear()
                search_input.send_keys(keyword)
                time.sleep(2)  # Chờ kết quả hiển thị

                # Kiểm tra thông báo "Không có dữ liệu"
                no_data_message = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//tbody[@id='showOrder']/tr/td[@colspan='6' and text()='Không có dữ liệu']")
                    )
                )
                assert no_data_message.is_displayed(), f"Thông báo không hiển thị khi tìm kiếm với từ khóa: {keyword}"

                print(f"Tìm kiếm với từ khóa '{keyword}' hiển thị chính xác thông báo 'Không có dữ liệu'.")

        finally:
            # Đảm bảo logout sau khi kiểm tra
            logout_admin(driver)

    def test_filter_orders_by_status(self, driver):
        """
        Kiểm tra lọc đơn hàng theo trạng thái (Tất cả, Đã xử lý, Chưa xử lý) và trường hợp không có đơn hàng.
        """
        try:
            # Mở trang web
            driver.get("http://localhost/Webbanhang-main/index.html")

            # Đăng nhập
            login(driver, "hgbaodev", "123456")
            time.sleep(4)

            # Nhấn vào "Đăng nhập / Đăng ký"
            click_element(driver, By.CLASS_NAME, "text-dndk")

            # Điều hướng đến trang quản lý đơn hàng
            click_element(driver, By.XPATH, "//a[contains(text(), 'Quản lý cửa hàng')]")
            click_element(driver, By.XPATH, "//div[@class='hidden-sidebar' and text()='Đơn hàng']")

            # Lấy dropdown trạng thái đơn hàng
            status_dropdown = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "tinh-trang"))
            )
            status_options = status_dropdown.find_elements(By.TAG_NAME, "option")

            # Map trạng thái từ dropdown tới trạng thái hiển thị
            status_map = {
                "Tất cả": None,  # Không kiểm tra cụ thể với "Tất cả"
                "Đã xử lý": "Đã xử lý",
                "Chưa xử lý": "Chưa xử lý"
            }

            # Kiểm tra từng trạng thái
            for option in status_options:
                status_text = option.text
                print(f"Kiểm tra trạng thái: {status_text}")

                # Chọn trạng thái trong dropdown
                status_dropdown.click()
                option.click()
                time.sleep(1)  # Chờ danh sách đơn hàng thay đổi

                try:
                    # Kiểm tra nếu không có đơn hàng nào
                    no_data_message = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located(
                            (By.XPATH, "//tbody[@id='showOrder']/tr/td[text()='Không có dữ liệu']"))
                    )
                    if no_data_message.is_displayed():
                        print(f"Không có đơn hàng nào với trạng thái '{status_text}'.")
                        continue  # Tiến hành kiểm tra trạng thái cho các trường hợp còn lại
                except TimeoutException:
                    # Nếu không tìm thấy thông báo "Không có dữ liệu", tiến hành kiểm tra đơn hàng
                    pass

                # Lấy danh sách đơn hàng hiển thị
                orders = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, "//tbody[@id='showOrder']/tr"))
                )

                # Kiểm tra trạng thái của từng đơn hàng
                for order in orders:
                    status_element = order.find_element(By.XPATH, ".//td/span")
                    order_status = status_element.text

                    # Nếu trạng thái là "Tất cả", bỏ qua kiểm tra chi tiết
                    if status_map[status_text] is None:
                        continue

                    # Kiểm tra trạng thái hiển thị có khớp với trạng thái được chọn
                    assert order_status == status_map[status_text], \
                        f"Đơn hàng có trạng thái '{order_status}' không khớp với trạng thái '{status_map[status_text]}' đã chọn."

                print(f"Tất cả đơn hàng đều hiển thị đúng trạng thái: {status_text}")

            print("Kiểm thử lọc đơn hàng theo trạng thái thành công.")

        finally:
            # Đảm bảo logout sau khi kiểm tra
            logout_admin(driver)

    def test_filter_orders_by_date(self, driver):
        try:
            driver.get("http://localhost/Webbanhang-main/index.html")
            time.sleep(2)

            # Đăng nhập
            login(driver, "hgbaodev", "123456")
            time.sleep(3)

            # Điều hướng đến trang quản lý đơn hàng
            click_element(driver, By.CLASS_NAME, "text-dndk")
            time.sleep(2)

            click_element(driver, By.XPATH, "//a[contains(text(), 'Quản lý cửa hàng')]")
            click_element(driver, By.XPATH, "//div[@class='hidden-sidebar' and text()='Đơn hàng']")
            time.sleep(1)

            # Nhập ngày kết thúc
            fill_input(driver, By.ID, "time-end", "12-11-2024")
            time.sleep(3)

            # Nhập ngày bắt đầu
            fill_input(driver, By.ID, "time-start", "12-01-2024")
            time.sleep(3)

            # Đợi bảng xuất hiện
            try:
                WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#showOrder")))
                table = driver.find_element(By.CSS_SELECTOR, "#showOrder")
                rows = table.find_elements(By.TAG_NAME, "tr")

                # Kiểm tra nếu bảng chứa dòng "Không có dữ liệu"
                if len(rows) == 1 and "Không có dữ liệu" in rows[0].text:
                    print("Bảng không có dữ liệu, kiểm thử thành công.")
                    assert True, "Bảng không có dữ liệu, không cần kiểm tra thêm."
                    return

                # Chuyển đổi ngày bắt đầu và kết thúc thành datetime
                start_date = datetime.strptime("12-01-2024", "%m-%d-%Y")
                end_date = datetime.strptime("12-11-2024", "%m-%d-%Y")

                valid_count = 0
                # Duyệt qua từng hàng để kiểm tra logic ngày
                for i, row in enumerate(rows):
                    try:
                        # Lấy dữ liệu ngày từ cột "Ngày tạo đơn hàng"
                        date_text = row.find_element(By.XPATH, "./td[3]").text  # Giả sử cột ngày ở vị trí thứ 3
                        date_obj = datetime.strptime(date_text, "%d/%m/%Y")

                        if start_date <= date_obj <= end_date:
                            print(f"Hàng {i + 1}: {date_text} hợp lệ.")
                            valid_count += 1
                        else:
                            print(f"Hàng {i + 1}: {date_text} không nằm trong khoảng ngày lọc.")
                    except Exception as e:
                        print(f"Lỗi xử lý hàng {i + 1}: {e}")

                # Kiểm tra kết quả lọc
                assert valid_count > 0, "Không có đơn hàng nào trong khoảng ngày lọc."
                print(f"Tìm thấy {valid_count} đơn hàng hợp lệ.")

            except TimeoutException:
                assert False, "Không thể tìm thấy bảng dữ liệu sau khi chờ đợi."

        except Exception as e:
            print(f"Lỗi: {str(e)}")
            assert False, f"Đã xảy ra lỗi trong quá trình kiểm thử: {str(e)}"

    def test_update_order_status(self, driver):
        try:
            driver.get("http://localhost/Webbanhang-main/index.html")

            # Đăng nhập
            login(driver, "hgbaodev", "123456")
            time.sleep(4)

            # Điều hướng đến trang quản lý đơn hàng
            click_element(driver, By.CLASS_NAME, "text-dndk")
            time.sleep(2)
            click_element(driver, By.XPATH, "//a[contains(text(), 'Quản lý cửa hàng')]")
            time.sleep(2)
            click_element(driver, By.XPATH, "//div[@class='hidden-sidebar' and text()='Đơn hàng']")
            time.sleep(2)

            # Kiểm tra nếu bảng có dữ liệu
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//tbody[@id='showOrder']")))
                orders_rows = driver.find_elements(By.XPATH, "//tbody[@id='showOrder']/tr")
                if len(orders_rows) == 0:
                    print("Bảng đơn hàng không có dữ liệu.")
                    assert False, "Không có dữ liệu trong bảng đơn hàng"
                else:
                    print(f"Bảng đơn hàng có {len(orders_rows)} đơn hàng.")
            except Exception as e:
                print(f"Lỗi khi kiểm tra bảng đơn hàng: {str(e)}")
                assert False, "Lỗi khi kiểm tra bảng đơn hàng"

            # Lặp qua từng đơn hàng trong bảng
            for index in range(len(orders_rows)):
                try:
                    # Cập nhật lại danh sách đơn hàng sau mỗi vòng lặp, tránh stale element
                    orders_rows = driver.find_elements(By.XPATH, "//tbody[@id='showOrder']/tr")
                    order = orders_rows[index]
                    print(f"Đang kiểm tra đơn hàng thứ {index + 1}")

                    # Trích xuất thông tin trạng thái đơn hàng
                    order_status_element = order.find_element(By.XPATH, ".//td[5]/span")
                    order_status = order_status_element.text.strip()

                    # In ra thông tin trạng thái
                    print(f"Trạng thái đơn hàng {index + 1}: {order_status}")

                    # Kiểm tra trạng thái đơn hàng
                    if order_status == "Chưa xử lý":
                        print(f"Trạng thái đơn hàng {index + 1} là: Chưa xử lý. Cập nhật trạng thái.")

                        # Nhấn vào nút Chi tiết của đơn hàng
                        detail_button = order.find_element(By.CLASS_NAME, "btn-detail")
                        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(detail_button)).click()

                        # Thêm sleep để quan sát modal mở ra
                        time.sleep(2)

                        # Chờ modal chi tiết mở ra và tìm nút "Chưa xử lý"
                        WebDriverWait(driver, 10).until(
                            EC.visibility_of_element_located((By.CLASS_NAME, "modal-detail-btn")))

                        # Nhấn vào nút Chưa xử lý để thay đổi trạng thái
                        status_button = driver.find_element(By.CLASS_NAME, "modal-detail-btn")
                        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(status_button)).click()

                        # Thêm sleep để quan sát việc thay đổi trạng thái
                        time.sleep(2)

                        # Kiểm tra trạng thái đã thay đổi trong modal
                        updated_status_button = WebDriverWait(driver, 10).until(
                            EC.visibility_of_element_located((By.CLASS_NAME, "modal-detail-btn"))
                        )
                        updated_status = updated_status_button.text
                        if updated_status == "Chưa xử lý":
                            print(f"Trạng thái đơn hàng {index + 1} đã được cập nhật thành: Chưa xử lý.")
                        else:
                            print(f"Trạng thái đơn hàng {index + 1} không thay đổi đúng.")

                        # Đóng modal sau khi cập nhật
                        close_button = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, "//button[@class='modal-close']"))
                        )
                        close_button.click()

                        # Thêm sleep để quan sát việc đóng modal
                        time.sleep(1)

                        # Dừng kiểm tra các đơn hàng còn lại sau khi đã cập nhật thành công
                        print("Đã cập nhật trạng thái cho đơn hàng. Dừng kiểm tra các đơn hàng khác.")
                        break  # Dừng vòng lặp sau khi cập nhật trạng thái thành công

                    else:
                        print(f"Trạng thái đơn hàng {index + 1} không phải là 'Chưa xử lý'.")

                except Exception as e:
                    print(f"Lỗi khi xử lý đơn hàng {index + 1}: {str(e)}")

                # Thêm sleep để quan sát giữa các bước kiểm thử
                time.sleep(1)

            print("Kiểm thử cập nhật trạng thái đơn hàng thành công.")

        except Exception as e:
            print(f"Lỗi khi kiểm thử cập nhật trạng thái đơn hàng: {str(e)}")
            assert False, f"Đã xảy ra lỗi trong quá trình kiểm thử: {str(e)}"
