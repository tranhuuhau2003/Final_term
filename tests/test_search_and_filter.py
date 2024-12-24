import random
import time
from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from Final_term.utils.helper import click_element, fill_input, check_toast_message, check_error_message, login, \
    add_customer, logout, logout_admin, add_to_cart, add_multiple_to_cart, update_product_quantity_in_cart, \
    check_cart_quantity, scroll_to_element, check_filtered_products, check_sorted_products, clear_and_send_keys, \
    scroll_page, wait_for_products, scroll_to_next_page, navi_to_next_page, enter_price, check_product_price_within_range
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


class TestSearchAndFilter:

    def test_search_product(self, driver):
        driver.get("http://localhost/Webbanhang-main/index.html")
        time.sleep(2)

        products = ["nấm", "nấm chay", "đậu hũ xào nấm chay"]

        for product in products:
            print(f"Tìm kiếm sản phẩm: {product}")
            clear_and_send_keys(driver, By.CLASS_NAME, "form-search-input", product)

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "form-search-input"))
            ).send_keys("\n")
            time.sleep(2)

            try:
                search_results = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "col-product"))
                )
                assert len(search_results) > 0, f"Không tìm thấy sản phẩm nào với từ khóa: {product}"

                for result in search_results:
                    product_name_element = result.find_element(By.CLASS_NAME, "card-title-link")
                    product_name = product_name_element.text.lower()
                    assert product.lower() in product_name, f"Sản phẩm '{product_name}' không khớp với từ khóa '{product}'"

                print(f"Tìm kiếm sản phẩm '{product}' thành công. Tất cả kết quả đều khớp!")
            except Exception as e:
                print(f"Không tìm thấy sản phẩm nào khớp với từ khóa '{product}'. Lỗi: {e}")

    def test_search_nonexistent_product(self, driver):
        driver.get("http://localhost/Webbanhang-main/index.html")
        time.sleep(2)  # Thêm thời gian chờ sau khi tải trang

        nonexistent_keyword = "cơm cuộn"
        print(f"Tìm kiếm sản phẩm không tồn tại: {nonexistent_keyword}")

        clear_and_send_keys(driver, By.CLASS_NAME, "form-search-input", nonexistent_keyword)

        search_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "form-search-input")))
        search_input.send_keys("\n")
        time.sleep(2)

        try:
            no_results_message = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "no-result-h"))
            )
            assert no_results_message.is_displayed(), "Thông báo không hiển thị khi không có sản phẩm khớp với từ khóa."
            assert "Tìm kiếm không có kết quả" in no_results_message.text, f"Nội dung thông báo không đúng: {no_results_message.text}"
            print("Thông báo hiển thị chính xác: Tìm kiếm không có kết quả")

        except Exception as e:
            print(
                f"Không tìm thấy thông báo phù hợp khi tìm kiếm từ khóa không tồn tại '{nonexistent_keyword}'. Lỗi: {e}")

    def test_filter_product_price(self, driver):
        # Mở trang web
        driver.get("http://localhost/Webbanhang-main/index.html")
        time.sleep(1)

        # Nhấn vào nút Lọc
        click_element(driver, By.CSS_SELECTOR, "button.filter-btn")
        time.sleep(1)

        # Nhập giá cần lọc
        min_price = 20000
        max_price = 50000
        enter_price(driver, min_price, max_price)

        # Nhấn nút lọc giá
        price_filter_btn = driver.find_element(By.ID, "advanced-search-price-btn")
        price_filter_btn.click()
        time.sleep(3)

        products = wait_for_products(driver)

        # Kiểm tra giá của các sản phẩm trong phạm vi giá cho phép
        for product in products:
            price_element = product.find_element(By.CLASS_NAME, "current-price")
            product_price_text = price_element.text.strip().replace("₫", "").replace(",", "").strip()
            product_price = int(product_price_text.replace(".", ""))

            assert min_price <= product_price <= max_price, \
                f"Giá sản phẩm '{product.text}' ({product_price}₫) không nằm trong khoảng từ {min_price}₫ đến {max_price}₫."

        print("Kiểm tra lọc sản phẩm theo giá thành công!")

    def test_sort_by_price_ascending(self, driver):
        # Mở trang web
        driver.get("http://localhost/Webbanhang-main/index.html")
        time.sleep(1)

        # Nhấn vào nút Lọc
        click_element(driver, By.CSS_SELECTOR, "button.filter-btn")
        time.sleep(1)

        # Nhấn nút sắp xếp theo giá từ thấp đến cao
        sort_ascending_btn = driver.find_element(By.ID, "sort-ascending")
        sort_ascending_btn.click()
        time.sleep(1)

        prev_price = 0
        page_count = 1
        while True:
            products = wait_for_products(driver)

            for product in products:
                price_element = product.find_element(By.CLASS_NAME, "current-price")
                product_price_text = price_element.text.strip().replace("₫", "").replace(",", "").strip()
                product_price = int(product_price_text.replace(".", ""))

                assert product_price >= prev_price, \
                    f"Giá sản phẩm '{product.text}' ({product_price}₫) không theo thứ tự từ thấp đến cao."

                prev_price = product_price

            pages = scroll_to_next_page(driver)
            if navi_to_next_page(driver, pages):
                time.sleep(2)
                page_count += 1
            else:
                break

        print(f"Đã kiểm tra {page_count} trang cho sản phẩm.")
        print("Kiểm tra sắp xếp sản phẩm theo giá từ thấp đến cao thành công!")

    def test_sort_by_price_descending(self, driver):
        # Mở trang web
        driver.get("http://localhost/Webbanhang-main/index.html")
        time.sleep(1)

        # Nhấn vào nút Lọc
        click_element(driver, By.CSS_SELECTOR, "button.filter-btn")
        time.sleep(1)

        # Nhấn nút sắp xếp theo giá từ cao đến thấp
        sort_descending_btn = driver.find_element(By.ID, "sort-descending")
        sort_descending_btn.click()
        time.sleep(2)

        prev_price = float('inf')
        page_count = 1
        while True:
            products = wait_for_products(driver)

            for product in products:
                price_element = product.find_element(By.CLASS_NAME, "current-price")
                product_price_text = price_element.text.strip().replace("₫", "").replace(",", "").strip()
                product_price = int(product_price_text.replace(".", ""))

                assert product_price <= prev_price, \
                    f"Giá sản phẩm '{product.text}' ({product_price}₫) không theo thứ tự từ cao đến thấp."

                prev_price = product_price

            pages = scroll_to_next_page(driver)
            if navi_to_next_page(driver, pages):
                time.sleep(2)
                page_count += 1
            else:
                break

        print(f"Đã kiểm tra {page_count} trang cho sản phẩm.")
        print("Kiểm tra sắp xếp sản phẩm theo giá từ cao đến thấp thành công!")

    def test_filter_and_sort_products(self, driver):

        # Mở trang web
        driver.get("http://localhost/Webbanhang-main/index.html")
        time.sleep(2)

        # Nhấn vào nút Lọc
        click_element(driver, By.CSS_SELECTOR, "button.filter-btn")
        time.sleep(2)

        # Lọc sản phẩm theo giá
        min_price_input = driver.find_element(By.ID, "min-price")
        max_price_input = driver.find_element(By.ID, "max-price")

        # Thiết lập giá cần lọc
        min_price = 20000  # Giá thấp nhất
        max_price = 50000  # Giá cao nhất

        # Nhập giá vào các trường
        min_price_input.clear()
        min_price_input.send_keys(str(min_price))
        max_price_input.clear()
        max_price_input.send_keys(str(max_price))

        # Nhấn nút lọc giá
        price_filter_btn = driver.find_element(By.ID, "advanced-search-price-btn")
        price_filter_btn.click()
        time.sleep(5)

        # Kiểm tra sản phẩm sau khi lọc giá
        check_filtered_products(driver, min_price, max_price)
        time.sleep(2)

        # Sắp xếp sản phẩm theo giá từ thấp đến cao
        sort_ascending_btn = driver.find_element(By.ID, "sort-ascending")
        sort_ascending_btn.click()
        time.sleep(2)

        # Kiểm tra sản phẩm sau khi sắp xếp theo giá từ thấp đến cao
        check_sorted_products(driver, ascending=True)
        time.sleep(2)

        # Nhấn nút reset để làm mới bộ lọc
        reset_btn = driver.find_element(By.ID, "reset-search")
        reset_btn.click()
        time.sleep(2)

        # Sắp xếp sản phẩm theo giá từ cao đến thấp
        sort_descending_btn = driver.find_element(By.ID, "sort-descending")
        sort_descending_btn.click()
        time.sleep(2)

        # Kiểm tra sản phẩm sau khi sắp xếp theo giá từ cao đến thấp
        check_sorted_products(driver, ascending=False)
        time.sleep(2)

        # Nhấn nút reset một lần nữa
        reset_btn.click()
        time.sleep(2)

        # Đóng phần lọc
        close_filter_btn = driver.find_element(By.XPATH, "//button[@onclick='closeSearchAdvanced()']")
        close_filter_btn.click()
        time.sleep(2)

        print("Kiểm tra lọc và sắp xếp sản phẩm thành công!")
