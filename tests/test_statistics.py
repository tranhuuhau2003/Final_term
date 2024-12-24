import datetime
import time

from selenium.common import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import pytest
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from Final_term.utils.helper import click_element, fill_input, check_toast_message, check_error_message, login, \
    add_customer, logout, logout_admin, add_to_cart, add_multiple_to_cart, update_product_quantity_in_cart, \
    check_cart_quantity, scroll_to_element, navigate_to_product_statistics, clear_and_send_keys
from Final_term.utils.driver_helper import init_driver, close_driver  # Import từ driver_helper
from selenium.webdriver.common.by import By
from datetime import datetime



@pytest.fixture
def driver():
    driver = init_driver()
    yield driver
    close_driver(driver)



class TestStatistics:

    def test_search_product_in_statistics(self, driver):
        try:
            global search_input
            navigate_to_product_statistics(driver, "hgbaodev", "123456")

            existing_dishes = ["Trà đào chanh sả"]
            for dish in existing_dishes:
                print(f"Tìm kiếm món ăn: {dish}")
                clear_and_send_keys(driver, By.ID, "form-search-tk", dish)

                search_results = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, "//tbody[@id='showTk']/tr"))
                )
                assert len(search_results) > 0, f"Không tìm thấy món ăn nào với từ khóa: {dish}"

                for result in search_results:
                    product_name = result.find_element(By.XPATH, ".//td[2]//p").text.lower()
                    assert dish.lower() in product_name, f"Món ăn '{product_name}' không khớp với từ khóa '{dish}'"

                print(f"Tìm kiếm món ăn '{dish}' thành công. Tất cả kết quả đều khớp!")

            print("Kiểm thử tìm kiếm sản phẩm tồn tại trong thống kê thành công.")
        finally:
            logout_admin(driver)

    def test_search_nonexistent_products(self, driver):
        try:
            navigate_to_product_statistics(driver, "hgbaodev", "123456")
            nonexistent_dishes = ["bánh mì thịt", "sushi tươi"]
            for nonexistent_dish in nonexistent_dishes:
                print(f"Tìm kiếm món ăn không tồn tại: {nonexistent_dish}")
                clear_and_send_keys(driver, By.ID, "form-search-tk", nonexistent_dish)

                rows = driver.find_element(By.ID, "showTk").find_elements(By.TAG_NAME, "tr")
                assert len(rows) == 0, f"Có kết quả tìm kiếm cho món ăn '{nonexistent_dish}', nhưng không có món ăn khớp."

                print(f"Không có kết quả tìm kiếm cho món ăn '{nonexistent_dish}'.")
            print("Kiểm thử tìm kiếm sản phẩm không tồn tại trong thống kê thành công.")
        finally:
            logout_admin(driver)

    def test_filter_by_category_in_statistics(self, driver):

        try:
            navigate_to_product_statistics(driver, "hgbaodev", "123456")

            category_select = driver.find_element(By.ID, "the-loai-tk")
            category_options = category_select.find_elements(By.TAG_NAME, "option")

            category_products = {}

            for option in category_options:
                category_name = option.text.strip()
                if category_name == "Tất cả":
                    continue  # Bỏ qua danh mục "Tất cả"

                category_select.click()
                option.click()
                time.sleep(2)

                product_table = driver.find_element(By.ID, "showTk")
                product_rows = product_table.find_elements(By.TAG_NAME, "tr")
                products = [row.find_element(By.XPATH, ".//td[2]//p").text.strip() for row in product_rows]

                category_products[category_name] = products
                print(f"Danh mục '{category_name}' có {len(products)} sản phẩm: {products}")

            for category1, products1 in category_products.items():
                for category2, products2 in category_products.items():
                    if category1 == category2:
                        continue

                    duplicates = set(products1).intersection(set(products2))
                    assert not duplicates, f"Sản phẩm trùng lặp giữa danh mục '{category1}' và '{category2}': {duplicates}"

            print("Kiểm thử lọc sản phẩm theo danh mục trong trang thống kê thành công.")
        finally:
            logout_admin(driver)

    def test_sort_by_sales_ascending(self, driver):
        try:
            navigate_to_product_statistics(driver, "hgbaodev", "123456")
            click_element(driver, By.CSS_SELECTOR, "button[onclick='thongKe(1)']")
            prev_sales = 0

            results_table = driver.find_element(By.ID, "showTk")
            rows = results_table.find_elements(By.TAG_NAME, "tr")

            for row in rows:
                sales_cell = row.find_elements(By.TAG_NAME, "td")[2]  # Cột số lượng bán
                sales_text = sales_cell.text.strip()
                if not sales_text:
                    continue
                try:
                    sales = int(sales_text)
                except ValueError:
                    print(f"Lỗi khi chuyển đổi số liệu '{sales_text}' thành số.")
                    continue

                product_name_cell = row.find_elements(By.TAG_NAME, "td")[1]
                product_name = product_name_cell.text.strip()

                print(f"Kiểm tra số lượng bán của {product_name}: {sales}")

                assert sales >= prev_sales, f"Số lượng bán của sản phẩm '{product_name}' ({sales}) không theo thứ tự từ thấp đến cao."

                prev_sales = sales

            print("Kiểm tra thống kê theo số lượng bán từ thấp đến cao thành công!")
        finally:
            logout_admin(driver)

    def test_sort_by_sales_descending(self, driver):
        try:
            navigate_to_product_statistics(driver, "hgbaodev", "123456")
            click_element(driver, By.CSS_SELECTOR,"button[onclick='thongKe(0)']")

            prev_sales = float('inf')

            results_table = driver.find_element(By.ID, "showTk")
            rows = results_table.find_elements(By.TAG_NAME, "tr")

            for row in rows:
                sales_cell = row.find_elements(By.TAG_NAME, "td")[2]
                sales_text = sales_cell.text.strip()

                if not sales_text:
                    continue

                try:
                    sales = int(sales_text)
                except ValueError:
                    print(f"Lỗi khi chuyển đổi số liệu '{sales_text}' thành số.")
                    continue

                product_name_cell = row.find_elements(By.TAG_NAME, "td")[1]
                product_name = product_name_cell.text.strip()

                print(f"Kiểm tra số lượng bán của {product_name}: {sales}")

                assert sales <= prev_sales, f"Số lượng bán của sản phẩm '{product_name}' ({sales}) không theo thứ tự từ cao đến thấp."

                prev_sales = sales

            print("Kiểm tra thống kê theo số lượng bán từ cao đến thấp thành công!")
        finally:
            logout_admin(driver)
