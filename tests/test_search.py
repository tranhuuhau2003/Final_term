import random
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


class TestSearch:


    def test_search_product(self, driver):
        # Mở trang web
        driver.get("http://localhost/Webbanhang-main/index.html")
        time.sleep(2)  # Thêm thời gian chờ sau khi tải trang

        # Danh sách sản phẩm mẫu để tìm kiếm
        products = ["nấm", "nấm chay", "đậu hũ xào nấm chay"]

        # Lặp qua từng từ khóa tìm kiếm
        for product in products:
            print(f"Tìm kiếm sản phẩm: {product}")

            # Tìm trường tìm kiếm và nhập sản phẩm
            search_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "form-search-input"))
            )
            search_input.clear()  # Xóa nội dung cũ
            search_input.send_keys(product)  # Nhập từ khóa tìm kiếm
            time.sleep(2)  # Chờ kích hoạt sự kiện tìm kiếm

            # Giả lập nhấn Enter để tìm kiếm
            search_input.send_keys("\n")
            time.sleep(2)  # Chờ kết quả tìm kiếm hiển thị

            # Kiểm tra kết quả tìm kiếm
            try:
                search_results = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "col-product"))
                )
                assert len(search_results) > 0, f"Không tìm thấy sản phẩm nào với từ khóa: {product}"

                # Kiểm tra từng sản phẩm trong danh sách kết quả
                for result in search_results:
                    product_name_element = result.find_element(By.CLASS_NAME, "card-title-link")
                    product_name = product_name_element.text.lower()
                    assert product.lower() in product_name, f"Sản phẩm '{product_name}' không khớp với từ khóa '{product}'"

                print(f"Tìm kiếm sản phẩm '{product}' thành công. Tất cả kết quả đều khớp!")
            except Exception as e:
                print(f"Không tìm thấy sản phẩm nào khớp với từ khóa '{product}'. Lỗi: {e}")

    def test_search_nonexistent_product(self, driver):
        # Mở trang web
        driver.get("http://localhost/Webbanhang-main/index.html")
        time.sleep(2)  # Thêm thời gian chờ sau khi tải trang

        # Từ khóa tìm kiếm không tồn tại
        nonexistent_keyword = "cơm cuộn"
        print(f"Tìm kiếm sản phẩm không tồn tại: {nonexistent_keyword}")

        # Tìm trường tìm kiếm và nhập từ khóa
        search_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "form-search-input"))
        )
        search_input.clear()  # Xóa nội dung cũ
        search_input.send_keys(nonexistent_keyword)  # Nhập từ khóa tìm kiếm
        time.sleep(2)  # Chờ kích hoạt sự kiện tìm kiếm

        # Giả lập nhấn Enter để tìm kiếm
        search_input.send_keys("\n")
        time.sleep(2)  # Chờ kết quả tìm kiếm hiển thị

        # Kiểm tra thông báo "không có kết quả"
        try:
            no_results_message = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "no-result-h"))
            )
            assert no_results_message.is_displayed(), "Thông báo không hiển thị khi không có sản phẩm khớp với từ khóa."
            assert "Tìm kiếm không có kết quả" in no_results_message.text, \
                f"Nội dung thông báo không đúng: {no_results_message.text}"

            print("Thông báo hiển thị chính xác: Tìm kiếm không có kết quả")

        except Exception as e:
            print(
                f"Không tìm thấy thông báo phù hợp khi tìm kiếm từ khóa không tồn tại '{nonexistent_keyword}'. Lỗi: {e}")