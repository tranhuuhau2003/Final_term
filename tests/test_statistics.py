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



class TestStatistics:
    def test_search_product_in_statistics(self, driver):

        try:
            # Mở trang web
            driver.get("http://localhost/Webbanhang-main/index.html")

            # Đăng nhập
            login(driver, "hgbaodev", "123456")
            time.sleep(4)

            # Điều hướng đến trang thống kê
            click_element(driver, By.CLASS_NAME, "text-dndk")
            time.sleep(2)

            # Chờ "Quản lý cửa hàng" xuất hiện và nhấn vào
            click_element(driver, By.XPATH, "//a[contains(text(), 'Quản lý cửa hàng')]")
            time.sleep(1)

            # Mở danh mục sản phẩm
            click_element(driver, By.XPATH, "//div[@class='hidden-sidebar' and text()='Thống kê']")
            time.sleep(1)


            # Danh sách món ăn mẫu để tìm kiếm
            existing_dishes = ["rau xào ngũ sắc"]

            # Tìm kiếm món ăn tồn tại
            for dish in existing_dishes:
                print(f"Tìm kiếm món ăn: {dish}")

                # Chờ trường tìm kiếm món ăn xuất hiện
                search_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "form-search-tk"))
                )
                search_input.clear()  # Xóa nội dung cũ nếu có
                search_input.send_keys(dish)  # Nhập từ khóa tìm kiếm
                time.sleep(2)  # Chờ kích hoạt sự kiện tìm kiếm

                # Kiểm tra kết quả tìm kiếm
                search_results = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, "//tbody[@id='showTk']/tr"))
                )
                assert len(search_results) > 0, f"Không tìm thấy món ăn nào với từ khóa: {dish}"

                for result in search_results:
                    product_name_element = result.find_element(By.XPATH, ".//td[2]//p")
                    product_name = product_name_element.text.lower()
                    assert dish.lower() in product_name, f"Món ăn '{product_name}' không khớp với từ khóa '{dish}'"

                print(f"Tìm kiếm món ăn '{dish}' thành công. Tất cả kết quả đều khớp!")

            # Kiểm tra tìm kiếm không có kết quả
            nonexistent_dishes = ["bánh mì thịt", "sushi tươi"]

            for nonexistent_dish in nonexistent_dishes:
                print(f"Tìm kiếm món ăn không tồn tại: {nonexistent_dish}")

                # Tìm trường tìm kiếm và nhập từ khóa không tồn tại
                search_input.clear()  # Xóa nội dung cũ
                search_input.send_keys(nonexistent_dish)  # Nhập từ khóa không tồn tại
                time.sleep(2)

                # Kiểm tra bảng không có kết quả (không có thẻ <tr> trong tbody)
                show_tk_table = driver.find_element(By.ID, "showTk")
                rows = show_tk_table.find_elements(By.TAG_NAME, "tr")
                assert len(
                    rows) == 0, f"Có kết quả tìm kiếm cho món ăn '{nonexistent_dish}', nhưng không có món ăn khớp."

                print(f"Không có kết quả tìm kiếm cho món ăn '{nonexistent_dish}'.")

        finally:
            # Đảm bảo logout sau khi kiểm tra
            logout_admin(driver)

    def test_search_existing_products(self, driver):

        try:
            # Mở trang web
            driver.get("http://localhost/Webbanhang-main/index.html")

            # Đăng nhập
            login(driver, "hgbaodev", "123456")
            time.sleep(4)

            # Điều hướng đến trang thống kê
            click_element(driver, By.CLASS_NAME, "text-dndk")
            time.sleep(1)

            click_element(driver, By.XPATH, "//a[contains(text(), 'Quản lý cửa hàng')]")
            time.sleep(1)

            click_element(driver, By.XPATH, "//div[@class='hidden-sidebar' and text()='Thống kê']")
            time.sleep(1)

            # Danh sách món ăn mẫu để tìm kiếm
            existing_dishes = ["rau xào ngũ sắc"]

            for dish in existing_dishes:
                print(f"Tìm kiếm món ăn: {dish}")

                # Chờ trường tìm kiếm món ăn xuất hiện
                search_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "form-search-tk"))
                )
                search_input.clear()
                search_input.send_keys(dish)
                time.sleep(2)

                # Kiểm tra kết quả tìm kiếm
                search_results = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, "//tbody[@id='showTk']/tr"))
                )
                assert len(search_results) > 0, f"Không tìm thấy món ăn nào với từ khóa: {dish}"

                for result in search_results:
                    product_name_element = result.find_element(By.XPATH, ".//td[2]//p")
                    product_name = product_name_element.text.lower()
                    assert dish.lower() in product_name, f"Món ăn '{product_name}' không khớp với từ khóa '{dish}'"

                print(f"Tìm kiếm món ăn '{dish}' thành công. Tất cả kết quả đều khớp!")

        finally:
            logout_admin(driver)

    def test_search_nonexistent_products(self, driver):

        try:
            # Mở trang web
            driver.get("http://localhost/Webbanhang-main/index.html")

            # Đăng nhập
            login(driver, "hgbaodev", "123456")
            time.sleep(4)

            # Điều hướng đến trang thống kê
            click_element(driver, By.CLASS_NAME, "text-dndk")
            time.sleep(1)

            click_element(driver, By.XPATH, "//a[contains(text(), 'Quản lý cửa hàng')]")
            time.sleep(1)

            click_element(driver, By.XPATH, "//div[@class='hidden-sidebar' and text()='Thống kê']")
            time.sleep(1)

            # Danh sách món ăn không tồn tại
            nonexistent_dishes = ["bánh mì thịt", "sushi tươi"]

            for nonexistent_dish in nonexistent_dishes:
                print(f"Tìm kiếm món ăn không tồn tại: {nonexistent_dish}")

                # Tìm trường tìm kiếm và nhập từ khóa không tồn tại
                search_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "form-search-tk"))
                )
                search_input.clear()
                search_input.send_keys(nonexistent_dish)
                time.sleep(2)

                # Kiểm tra bảng không có kết quả
                show_tk_table = driver.find_element(By.ID, "showTk")
                rows = show_tk_table.find_elements(By.TAG_NAME, "tr")
                assert len(
                    rows) == 0, f"Có kết quả tìm kiếm cho món ăn '{nonexistent_dish}', nhưng không có món ăn khớp."

                print(f"Không có kết quả tìm kiếm cho món ăn '{nonexistent_dish}'.")

        finally:
            logout_admin(driver)

    def test_filter_by_category_in_statistics(self, driver):

        try:
            # Mở trang web
            driver.get("http://localhost/Webbanhang-main/index.html")

            # Đăng nhập
            login(driver, "hgbaodev", "123456")
            time.sleep(4)

            # Điều hướng đến trang thống kê
            click_element(driver, By.CLASS_NAME, "text-dndk")
            time.sleep(1)

            click_element(driver, By.XPATH, "//a[contains(text(), 'Quản lý cửa hàng')]")
            time.sleep(1)

            click_element(driver, By.XPATH, "//div[@class='hidden-sidebar' and text()='Thống kê']")
            time.sleep(1)

            # Lấy dropdown danh mục
            category_select = driver.find_element(By.ID, "the-loai-tk")
            category_options = category_select.find_elements(By.TAG_NAME, "option")

            # Biến lưu trữ danh sách sản phẩm theo danh mục
            category_products = {}

            # Lặp qua tất cả danh mục (bỏ qua "Tất cả")
            for option in category_options:
                category_name = option.text.strip()
                if category_name == "Tất cả":
                    continue  # Bỏ qua danh mục "Tất cả"

                # Chọn danh mục
                category_select.click()  # Mở combobox
                option.click()  # Chọn danh mục
                time.sleep(2)  # Chờ danh sách sản phẩm thay đổi

                # Lấy danh sách sản phẩm trong danh mục
                product_table = driver.find_element(By.ID, "showTk")
                product_rows = product_table.find_elements(By.TAG_NAME, "tr")
                products = [
                    row.find_element(By.XPATH, ".//td[2]//p").text.strip() for row in product_rows
                ]

                # Lưu danh sách sản phẩm vào biến tương ứng với danh mục
                category_products[category_name] = products
                print(f"Danh mục '{category_name}' có {len(products)} sản phẩm: {products}")

            # So sánh các danh mục với nhau
            for category1, products1 in category_products.items():
                for category2, products2 in category_products.items():
                    if category1 == category2:
                        continue  # Bỏ qua so sánh cùng danh mục

                    # Tìm sản phẩm trùng lặp giữa hai danh mục
                    duplicates = set(products1).intersection(set(products2))
                    assert not duplicates, \
                        f"Sản phẩm trùng lặp giữa danh mục '{category1}' và '{category2}': {duplicates}"

            print("Kiểm thử lọc sản phẩm theo danh mục trong trang thống kê thành công.")
        finally:
            # Đảm bảo logout sau khi kiểm tra
            logout_admin(driver)

    def test_sort_by_sales_ascending(self, driver):

        # Mở trang web
        driver.get("http://localhost/Webbanhang-main/index.html")

        # Đăng nhập
        login(driver, "hgbaodev", "123456")
        time.sleep(4)

        # Điều hướng đến trang thống kê
        click_element(driver, By.CLASS_NAME, "text-dndk")
        time.sleep(1)

        click_element(driver, By.XPATH, "//a[contains(text(), 'Quản lý cửa hàng')]")
        time.sleep(1)

        click_element(driver, By.XPATH, "//div[@class='hidden-sidebar' and text()='Thống kê']")
        time.sleep(1)

        # Nhấn vào nút tăng dần
        sort_ascending_btn = driver.find_element(By.CSS_SELECTOR, "button[onclick='thongKe(1)']")
        sort_ascending_btn.click()
        time.sleep(2)  # Thêm thời gian chờ để thống kê xong

        # Biến lưu số lượng bán của sản phẩm
        prev_sales = 0

        # Lấy danh sách các sản phẩm trong bảng kết quả
        results_table = driver.find_element(By.ID, "showTk")
        rows = results_table.find_elements(By.TAG_NAME, "tr")

        # Kiểm tra số lượng bán của từng sản phẩm
        for row in rows:
            # Lấy số lượng bán của sản phẩm (cột số lượng bán)
            sales_cell = row.find_elements(By.TAG_NAME, "td")[2]  # Cột số lượng bán
            sales_text = sales_cell.text.strip()

            # Bỏ qua các dòng không có dữ liệu (nếu có)
            if not sales_text:
                continue

            try:
                sales = int(sales_text)  # Chuyển số lượng bán thành số
            except ValueError:
                print(f"Lỗi khi chuyển đổi số liệu '{sales_text}' thành số.")
                continue

            # Lấy tên sản phẩm từ cột thứ 2 (cột tên sản phẩm)
            product_name_cell = row.find_elements(By.TAG_NAME, "td")[1]
            product_name = product_name_cell.text.strip()

            # In ra số lượng bán của sản phẩm
            print(f"Kiểm tra số lượng bán của {product_name}: {sales}")

            # Kiểm tra nếu số lượng bán của sản phẩm nhỏ hơn hoặc bằng số lượng bán của sản phẩm trước đó
            assert sales >= prev_sales, \
                f"Số lượng bán của sản phẩm '{product_name}' ({sales}) không theo thứ tự từ thấp đến cao."

            # Cập nhật số lượng bán của sản phẩm hiện tại
            prev_sales = sales

        print("Kiểm tra thống kê theo số lượng bán từ thấp đến cao thành công!")

    def test_sort_by_sales_descending(self, driver):

        # Mở trang web
        driver.get("http://localhost/Webbanhang-main/index.html")

        # Đăng nhập
        login(driver, "hgbaodev", "123456")
        time.sleep(4)

        # Điều hướng đến trang thống kê
        click_element(driver, By.CLASS_NAME, "text-dndk")
        time.sleep(1)

        click_element(driver, By.XPATH, "//a[contains(text(), 'Quản lý cửa hàng')]")
        time.sleep(1)

        click_element(driver, By.XPATH, "//div[@class='hidden-sidebar' and text()='Thống kê']")
        time.sleep(1)

        # Nhấn vào nút giảm dần (nút giảm dần có thể khác, bạn cần thay thế đúng nút nếu cần)
        sort_descending_btn = driver.find_element(By.CSS_SELECTOR,
                                                  "button[onclick='thongKe(0)']")  # Giả sử đây là nút giảm dần
        sort_descending_btn.click()
        time.sleep(2)  # Thêm thời gian chờ để thống kê xong

        # Biến lưu số lượng bán của sản phẩm
        prev_sales = float('inf')  # Khởi tạo với giá trị rất lớn

        # Lấy danh sách các sản phẩm trong bảng kết quả
        results_table = driver.find_element(By.ID, "showTk")
        rows = results_table.find_elements(By.TAG_NAME, "tr")

        # Kiểm tra số lượng bán của từng sản phẩm
        for row in rows:
            # Lấy số lượng bán của sản phẩm (cột số lượng bán)
            sales_cell = row.find_elements(By.TAG_NAME, "td")[2]  # Cột số lượng bán
            sales_text = sales_cell.text.strip()

            # Bỏ qua các dòng không có dữ liệu (nếu có)
            if not sales_text:
                continue

            try:
                sales = int(sales_text)  # Chuyển số lượng bán thành số
            except ValueError:
                print(f"Lỗi khi chuyển đổi số liệu '{sales_text}' thành số.")
                continue

            # Lấy tên sản phẩm từ cột thứ 2 (cột tên sản phẩm)
            product_name_cell = row.find_elements(By.TAG_NAME, "td")[1]
            product_name = product_name_cell.text.strip()

            # In ra số lượng bán của sản phẩm
            print(f"Kiểm tra số lượng bán của {product_name}: {sales}")

            # Kiểm tra nếu số lượng bán của sản phẩm lớn hơn hoặc bằng số lượng bán của sản phẩm trước đó
            assert sales <= prev_sales, \
                f"Số lượng bán của sản phẩm '{product_name}' ({sales}) không theo thứ tự từ cao đến thấp."

            # Cập nhật số lượng bán của sản phẩm hiện tại
            prev_sales = sales

        print("Kiểm tra thống kê theo số lượng bán từ cao đến thấp thành công!")
