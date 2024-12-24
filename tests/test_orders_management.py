import datetime
import time

from selenium.common import TimeoutException, StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import pytest
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from Final_term.utils.helper import click_element, fill_input, check_toast_message, check_error_message, login, \
    add_customer, logout, logout_admin, add_to_cart, add_multiple_to_cart, update_product_quantity_in_cart, \
    check_cart_quantity, scroll_to_element, navigate_to_product_orders, clear_and_send_keys, select_dropdown_option
from Final_term.utils.driver_helper import init_driver, close_driver  # Import từ driver_helper
from selenium.webdriver.common.by import By
from datetime import datetime



@pytest.fixture
def driver():
    driver = init_driver()
    yield driver
    close_driver(driver)


class TestOrdersManagement:
    def test_search_order_by_id(self, driver):
        try:
            navigate_to_product_orders(driver, "hgbaodev", "123456")

            clear_and_send_keys(driver, By.ID, "form-search-order", "DH1")
            orders = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, f"//tbody[@id='showOrder']/tr[td[text()='DH1']]"))
            )
            assert len(orders) > 0, f"Không tìm thấy đơn hàng với mã: DH1"
            print(f"Tìm kiếm đơn hàng 'DH1' thành công. Kết quả hiển thị đúng!")

        finally:
            logout_admin(driver)

    def test_search_order_by_customer(self, driver):
        try:
            navigate_to_product_orders(driver, "hgbaodev", "123456")
            clear_and_send_keys(driver, By.ID, "form-search-order", "0123456789")
            orders = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, f"//tbody[@id='showOrder']/tr[td[text()='0123456789']]"))
            )
            assert len(orders) > 0, f"Không tìm thấy đơn hàng với khách hàng: 0123456789"
            print(f"Tìm kiếm đơn hàng với khách hàng '0123456789' thành công. Kết quả hiển thị đúng!")

        finally:
            logout_admin(driver)

    def test_search_nonexistent_order(self, driver):
        try:
            navigate_to_product_orders(driver, "hgbaodev", "123456")
            nonexistent_keywords = ["INVALID_ID", "UNKNOWN_CUSTOMER"]

            for keyword in nonexistent_keywords:
                print(f"Tìm kiếm với từ khóa không tồn tại: {keyword}")

                clear_and_send_keys(driver, By.ID, "form-search-order", keyword)
                no_data_message = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//tbody[@id='showOrder']/tr/td[@colspan='6' and text()='Không có dữ liệu']")
                    )
                )
                assert no_data_message.is_displayed(), f"Thông báo không hiển thị khi tìm kiếm với từ khóa: {keyword}"
                print(f"Tìm kiếm với từ khóa '{keyword}' hiển thị chính xác thông báo 'Không có dữ liệu'.")

        finally:
            logout_admin(driver)

    def test_filter_orders_by_status(self, driver):
        try:
            navigate_to_product_orders(driver, "hgbaodev", "123456")
            status_map = {
                "Tất cả": None,
                "Đã xử lý": "Đã xử lý",
                "Chưa xử lý": "Chưa xử lý"
            }

            for status_text, expected_status in status_map.items():
                print(f"Kiểm tra trạng thái: {status_text}")

                select_dropdown_option(driver, By.ID, "tinh-trang", status_text)
                time.sleep(2)

                no_data = driver.find_elements(By.XPATH, "//tbody[@id='showOrder']/tr/td[text()='Không có dữ liệu']")
                if no_data:
                    print(f"Không có đơn hàng nào với trạng thái '{status_text}'.")
                    continue

                orders = driver.find_elements(By.XPATH, "//tbody[@id='showOrder']/tr")
                for order in orders:
                    order_status = order.find_element(By.XPATH, ".//td/span").text

                    if expected_status is not None:
                        assert order_status == expected_status, \
                            f"Đơn hàng có trạng thái '{order_status}' không khớp với trạng thái '{expected_status}' đã chọn."

                print(f"Tất cả đơn hàng đều hiển thị đúng trạng thái: {status_text}")

            print("Kiểm thử lọc đơn hàng theo trạng thái thành công.")
        finally:
            logout_admin(driver)

    def test_filter_orders_by_date(self, driver):
        try:
            navigate_to_product_orders(driver, "hgbaodev", "123456")

            fill_input(driver, By.ID, "time-end", "12-11-2024")
            time.sleep(2)

            fill_input(driver, By.ID, "time-start", "12-01-2024")
            time.sleep(2)

            WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#showOrder")))
            table = driver.find_element(By.CSS_SELECTOR, "#showOrder")
            rows = table.find_elements(By.TAG_NAME, "tr")

            if len(rows) == 1 and "Không có dữ liệu" in rows[0].text:
                print("Bảng không có dữ liệu, kiểm thử thành công.")
                return

            start_date = datetime.strptime("12-01-2024", "%m-%d-%Y")
            end_date = datetime.strptime("12-11-2024", "%m-%d-%Y")

            valid_count = 0
            for i, row in enumerate(rows):
                try:
                    date_text = row.find_element(By.XPATH, "./td[3]").text
                    date_obj = datetime.strptime(date_text, "%d/%m/%Y")

                    if start_date <= date_obj <= end_date:
                        print(f"Hàng {i + 1}: {date_text} hợp lệ.")
                        valid_count += 1
                    else:
                        print(f"Hàng {i + 1}: {date_text} không nằm trong khoảng ngày lọc.")
                        assert False, f"Hàng {i + 1} có ngày '{date_text}' không nằm trong khoảng ngày lọc."
                except Exception as e:
                    print(f"Lỗi xử lý hàng {i + 1}: {e}")

            assert valid_count > 0, "Không có đơn hàng nào trong khoảng ngày lọc."
            print(f"Tìm thấy {valid_count} đơn hàng hợp lệ.")
        finally:
            logout_admin(driver)

    def test_update_order_status(self, driver):
        try:
            navigate_to_product_orders(driver, "hgbaodev", "123456")

            orders_rows = driver.find_elements(By.XPATH, "//tbody[@id='showOrder']/tr")
            assert len(orders_rows) > 0, "Bảng đơn hàng không có dữ liệu."
            print(f"Bảng đơn hàng có {len(orders_rows)} đơn hàng.")

            for index, order in enumerate(orders_rows):
                order_status_element = order.find_element(By.XPATH, ".//td[5]/span")
                order_status = order_status_element.text.strip()

                print(f"Trạng thái đơn hàng {index + 1}: {order_status}")

                if order_status == "Chưa xử lý":
                    detail_button = order.find_element(By.CLASS_NAME, "btn-detail")
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(detail_button)).click()
                    time.sleep(2)

                    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "modal-detail-btn")))

                    status_button = driver.find_element(By.CLASS_NAME, "modal-detail-btn")
                    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(status_button)).click()
                    time.sleep(2)

                    updated_status_button = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "modal-detail-btn")))
                    updated_status = updated_status_button.text

                    assert updated_status != "Chưa xử lý", f"Trạng thái đơn hàng {index + 1} không thay đổi đúng."
                    print(f"Trạng thái đơn hàng {index + 1} đã được cập nhật thành: {updated_status}.")

                    close_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@class='modal-close']")))
                    close_button.click()
                    time.sleep(1)

                    print("Đã cập nhật trạng thái cho đơn hàng.")
                    break

            print("Kiểm thử cập nhật trạng thái đơn hàng thành công.")
        finally:
            logout_admin(driver)

