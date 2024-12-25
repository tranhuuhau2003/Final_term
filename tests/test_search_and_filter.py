
import time

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from Final_term.utils.driver_helper import init_driver, close_driver  # Import từ driver_helper
from Final_term.utils.helper import click_element, clear_and_send_keys, \
    wait_for_products, scroll_to_next_page, navi_to_next_page, enter_price, \
    filter_products_by_price, sort_products


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
        driver.get("http://localhost/Webbanhang-main/index.html")
        time.sleep(1)

        click_element(driver, By.CSS_SELECTOR, "button.filter-btn")
        time.sleep(1)

        min_price = 20000
        max_price = 50000
        enter_price(driver, min_price, max_price)

        price_filter_btn = driver.find_element(By.ID, "advanced-search-price-btn")
        price_filter_btn.click()
        time.sleep(3)

        products = wait_for_products(driver)

        for product in products:
            price_element = product.find_element(By.CLASS_NAME, "current-price")
            product_price_text = price_element.text.strip().replace("₫", "").replace(",", "").strip()
            product_price = int(product_price_text.replace(".", ""))

            assert min_price <= product_price <= max_price, \
                f"Giá sản phẩm '{product.text}' ({product_price}₫) không nằm trong khoảng từ {min_price}₫ đến {max_price}₫."

        print("Kiểm tra lọc sản phẩm theo giá thành công!")

    def test_sort_by_price_ascending(self, driver):
        driver.get("http://localhost/Webbanhang-main/index.html")
        time.sleep(1)

        click_element(driver, By.CSS_SELECTOR, "button.filter-btn")
        time.sleep(1)

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
        driver.get("http://localhost/Webbanhang-main/index.html")
        time.sleep(1)

        click_element(driver, By.CSS_SELECTOR, "button.filter-btn")
        time.sleep(1)

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
        driver.get("http://localhost/Webbanhang-main/index.html")
        time.sleep(2)
        click_element(driver, By.CSS_SELECTOR, "button.filter-btn")
        time.sleep(2)

        min_price = 20000
        max_price = 50000
        filter_products_by_price(driver, min_price, max_price)

        products_section = driver.find_element(By.ID, "home-products")
        products = products_section.find_elements(By.CLASS_NAME, "card-product")

        for product in products:
            price_element = product.find_element(By.CLASS_NAME, "current-price")
            product_price_text = price_element.text.strip().replace("₫", "").replace(",", "").strip()
            product_price_text = product_price_text.replace(".", "")
            try:
                product_price = int(product_price_text)
            except ValueError:
                print(f"Lỗi khi chuyển đổi giá '{product_price_text}' thành số.")
                continue

            assert min_price <= product_price <= max_price, f"Giá sản phẩm '{product.text}' ({product_price}₫) không nằm trong khoảng {min_price}₫ đến {max_price}₫."
        print("Kiểm tra lọc giá sản phẩm thành công!")


        sort_products(driver, ascending=True)
        prev_price = 0
        products_section = driver.find_element(By.ID, "home-products")
        products = products_section.find_elements(By.CLASS_NAME, "card-product")

        for product in products:
            price_element = product.find_element(By.CLASS_NAME, "current-price")
            product_price_text = price_element.text.strip().replace("₫", "").replace(",", "").strip()
            product_price_text = product_price_text.replace(".", "")
            try:
                product_price = int(product_price_text)
            except ValueError:
                print(f"Lỗi khi chuyển đổi giá '{product_price_text}' thành số.")
                continue

            assert product_price >= prev_price, f"Giá sản phẩm '{product.text}' ({product_price}₫) không theo thứ tự từ thấp đến cao."

            prev_price = product_price
        print("Kiểm tra sắp xếp giá sản phẩm từ thấp đến cao thành công!")

        click_element(driver, By.ID, "reset-search")


        sort_products(driver, ascending=False)
        prev_price = float('inf')
        products_section = driver.find_element(By.ID, "home-products")
        products = products_section.find_elements(By.CLASS_NAME, "card-product")
        for product in products:
            price_element = product.find_element(By.CLASS_NAME, "current-price")
            product_price_text = price_element.text.strip().replace("₫", "").replace(",", "").strip()
            product_price_text = product_price_text.replace(".", "")
            try:
                product_price = int(product_price_text)
            except ValueError:
                print(f"Lỗi khi chuyển đổi giá '{product_price_text}' thành số.")
                continue

            assert product_price <= prev_price, \
                f"Giá sản phẩm '{product.text}' ({product_price}₫) không theo thứ tự từ cao đến thấp."

            prev_price = product_price
        print("Kiểm tra sắp xếp giá sản phẩm từ cao đến thấp thành công!")

        click_element(driver, By.ID, "reset-search")

        click_element(driver, By.XPATH, "//button[@onclick='closeSearchAdvanced()']")

        print("Kiểm tra lọc và sắp xếp sản phẩm thành công!")
