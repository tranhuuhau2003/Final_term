import random
import time
from selenium.common import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from Final_term.utils.helper import click_element, fill_input, check_toast_message, check_error_message, login, add_customer, logout, logout_admin, add_to_cart, add_multiple_to_cart, update_product_quantity_in_cart, check_cart_quantity, scroll_to_element, check_filtered_products, check_sorted_products
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

    def test_filter_product(self, driver):

        # Mở trang web
        driver.get("http://localhost/Webbanhang-main/index.html")
        time.sleep(2)

        # Nhấn vào nút Lọc
        click_element(driver, By.CSS_SELECTOR, "button.filter-btn")
        time.sleep(2)

        # Lấy combobox và danh sách các tùy chọn
        combobox = driver.find_element(By.ID, "advanced-search-category-select")
        options = combobox.find_elements(By.TAG_NAME, "option")

        # Duyệt qua từng tùy chọn trong combobox
        for option in options:
            # Bỏ qua tùy chọn "Tất cả" nếu không muốn kiểm tra
            if option.text == "Tất cả":
                continue

            # Chọn tùy chọn hiện tại
            option.click()
            time.sleep(2)

            # Lấy danh sách sản phẩm sau khi lọc
            products_section = driver.find_element(By.ID, "home-products")
            products = products_section.find_elements(By.CLASS_NAME, "card-product")

            # Assert kiểm tra nếu không có sản phẩm sau khi lọc
            assert len(products) > 0, f"Không có sản phẩm hiển thị sau khi chọn '{option.text}' trong combobox."

            # Kiểm tra phân trang nếu có sản phẩm
            page_count = 0
            while True:
                # Lấy danh sách sản phẩm trên trang hiện tại
                products = products_section.find_elements(By.CLASS_NAME, "card-product")
                if len(products) > 0:
                    page_count += 1  # Tăng số trang khi có sản phẩm trên trang hiện tại

                # Tìm các nút phân trang
                try:
                    # Cuộn đến 2/3 chiều cao của trang sau mỗi lần kiểm tra sản phẩm
                    scroll_height = driver.execute_script("return document.body.scrollHeight")
                    scroll_position = scroll_height * 2 / 3
                    driver.execute_script(f"window.scrollTo(0, {scroll_position});")
                    time.sleep(2)

                    pagination = driver.find_element(By.CLASS_NAME, "page-nav-list")
                    pages = pagination.find_elements(By.CLASS_NAME, "page-nav-item")

                    # Nếu có nhiều hơn một trang, kiểm tra và click vào trang kế tiếp
                    active_page = pagination.find_element(By.CLASS_NAME, "active")  # Trang hiện tại
                    current_page_number = int(active_page.find_element(By.TAG_NAME, "a").text)  # Số trang hiện tại
                    next_page_number = current_page_number + 1  # Trang kế tiếp là trang hiện tại + 1
                    next_page = None

                    # Tìm trang kế tiếp
                    for page in pages:
                        page_number = int(page.find_element(By.TAG_NAME, "a").text)
                        if page_number == next_page_number:  # Tìm trang có số trang = trang hiện tại + 1
                            next_page = page
                            break

                    if next_page:
                        click_element(driver, By.XPATH, f"//a[text()='{next_page_number}']")  # Click vào trang kế tiếp
                        time.sleep(2)

                        # Cuộn lại 2/3 chiều cao của trang
                        driver.execute_script(f"window.scrollTo(0, {scroll_position});")
                        time.sleep(2)
                    else:
                        # Nếu không còn trang kế tiếp
                        break  # Dừng nếu không có trang kế tiếp

                except Exception:
                    break

            print(f"Đã kiểm tra {page_count} trang cho sản phẩm của loại '{option.text}'.")

        print("Kiểm tra lọc sản phẩm hoàn tất!")

    def test_filter_product_price(self, driver):

        # Mở trang web
        driver.get("http://localhost/Webbanhang-main/index.html")
        time.sleep(1)

        # Nhấn vào nút Lọc
        click_element(driver, By.CSS_SELECTOR, "button.filter-btn")
        time.sleep(1)

        # Nhập giá thấp nhất và giá cao nhất
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
        time.sleep(3)

        # Lấy danh sách các sản phẩm hiển thị
        products_section = driver.find_element(By.ID, "home-products")
        products = products_section.find_elements(By.CLASS_NAME, "card-product")

        # Kiểm tra giá của từng sản phẩm
        for product in products:
            # Lấy giá sản phẩm
            price_element = product.find_element(By.CLASS_NAME, "current-price")
            product_price_text = price_element.text.strip().replace("₫", "").replace(",", "").strip()

            # Loại bỏ dấu chấm trong giá (nếu có)
            product_price_text = product_price_text.replace(".", "")

            try:
                # Chuyển giá sang kiểu số nguyên
                product_price = int(product_price_text)
            except ValueError:
                print(f"Lỗi khi chuyển đổi giá '{product_price_text}' thành số.")
                continue

            # Assert giá của sản phẩm phải nằm trong khoảng giá lọc
            assert min_price <= product_price <= max_price, \
                f"Giá sản phẩm '{product.text}' ({product_price}₫) không nằm trong khoảng từ {min_price}₫ đến {max_price}₫."

        print("Kiểm tra lọc sản phẩm theo giá thành công!")

    def test_sort_by_price_ascending(self, driver):

        # Mở trang web
        driver.get("http://localhost/Webbanhang-main/index.html")
        time.sleep(1)  # Thêm thời gian chờ lâu hơn để trang tải hoàn toàn

        # Nhấn vào nút Lọc
        click_element(driver, By.CSS_SELECTOR, "button.filter-btn")
        time.sleep(1)  # Thêm thời gian chờ sau khi nhấn nút lọc

        # Nhấn nút sắp xếp theo giá từ thấp đến cao
        sort_ascending_btn = driver.find_element(By.ID, "sort-ascending")
        sort_ascending_btn.click()
        time.sleep(1)  # Thêm thời gian chờ để sắp xếp xong trước khi lấy sản phẩm

        # Biến lưu giá của sản phẩm trên mỗi trang
        prev_price = 0
        page_count = 1  # Đếm số trang đã kiểm tra

        while True:
            # Lấy danh sách các sản phẩm hiển thị
            products_section = driver.find_element(By.ID, "home-products")
            products = products_section.find_elements(By.CLASS_NAME, "card-product")

            # Kiểm tra giá của từng sản phẩm
            for product in products:
                # Lấy giá sản phẩm
                price_element = product.find_element(By.CLASS_NAME, "current-price")
                product_price_text = price_element.text.strip().replace("₫", "").replace(",", "").strip()

                # Loại bỏ dấu chấm (nếu có) và chuyển đổi giá thành số nguyên
                product_price_text = product_price_text.replace(".", "")
                try:
                    product_price = int(product_price_text)
                except ValueError:
                    print(f"Lỗi khi chuyển đổi giá '{product_price_text}' thành số.")
                    continue

                # In ra giá sản phẩm đã kiểm tra
                print(f"Kiểm tra giá sản phẩm: {product.text} - {product_price}₫")

                # Kiểm tra nếu giá sản phẩm nhỏ hơn hoặc bằng giá sản phẩm trước đó (sắp xếp giá từ thấp đến cao)
                assert product_price >= prev_price, \
                    f"Giá sản phẩm '{product.text}' ({product_price}₫) không theo thứ tự từ thấp đến cao."

                # Cập nhật giá sản phẩm hiện tại
                prev_price = product_price

            # Cuộn trang tới khi gặp phần phân trang
            try:
                # Cuộn trang cho đến khi gặp phần phân trang
                while True:
                    # Kiểm tra xem phần phân trang có xuất hiện chưa
                    try:
                        pagination = driver.find_element(By.CLASS_NAME, "page-nav-list")
                        pages = pagination.find_elements(By.CLASS_NAME, "page-nav-item")
                        break  # Dừng cuộn khi gặp phần phân trang
                    except:
                        # Nếu phần phân trang chưa xuất hiện, cuộn thêm một đoạn
                        driver.execute_script("window.scrollBy(0, 300);")  # Cuộn một đoạn
                        time.sleep(2)  # Đợi lâu hơn để trang kịp tải thêm sản phẩm

                # Tìm số trang kế tiếp
                active_page = pagination.find_element(By.CLASS_NAME, "active")  # Trang hiện tại
                current_page_number = int(active_page.find_element(By.TAG_NAME, "a").text)  # Số trang hiện tại
                next_page_number = current_page_number + 1  # Trang kế tiếp là trang hiện tại + 1
                next_page = None

                # Tìm trang kế tiếp
                for page in pages:
                    page_number = int(page.find_element(By.TAG_NAME, "a").text)
                    if page_number == next_page_number:  # Tìm trang có số trang = trang hiện tại + 1
                        next_page = page
                        break

                if next_page:
                    # Thêm time.sleep trước khi nhấn vào trang tiếp theo
                    time.sleep(2)  # Thêm thời gian chờ trước khi nhấn vào trang kế tiếp

                    # Nhấp vào trang kế tiếp
                    click_element(driver, By.XPATH, f"//a[text()='{next_page_number}']")  # Click vào trang kế tiếp
                    time.sleep(2)  # Thêm thời gian chờ sau khi nhấn vào trang kế tiếp

                    page_count += 1
                else:
                    # Nếu không còn trang kế tiếp
                    break  # Dừng nếu không có trang kế tiếp

            except Exception as e:
                print(f"Lỗi khi cuộn hoặc phân trang: {str(e)}")
                break

        print(f"Đã kiểm tra {page_count} trang cho sản phẩm.")
        print("Kiểm tra sắp xếp sản phẩm theo giá từ thấp đến cao thành công!")

    def test_sort_by_price_descending(self, driver):

        # Mở trang web
        driver.get("http://localhost/Webbanhang-main/index.html")
        time.sleep(1)  # Thêm thời gian chờ lâu hơn để trang tải hoàn toàn

        # Nhấn vào nút Lọc
        click_element(driver, By.CSS_SELECTOR, "button.filter-btn")
        time.sleep(1)  # Thêm thời gian chờ sau khi nhấn nút lọc

        # Nhấn nút sắp xếp theo giá từ cao đến thấp
        sort_descending_btn = driver.find_element(By.ID, "sort-descending")
        sort_descending_btn.click()
        time.sleep(2)

        # Biến lưu giá của sản phẩm trên mỗi trang
        prev_price = float('inf')  # Sử dụng giá ban đầu là vô cùng lớn
        page_count = 1  # Đếm số trang đã kiểm tra

        while True:
            # Lấy danh sách các sản phẩm hiển thị
            products_section = driver.find_element(By.ID, "home-products")
            products = products_section.find_elements(By.CLASS_NAME, "card-product")

            # Kiểm tra giá của từng sản phẩm
            for product in products:
                # Lấy giá sản phẩm
                price_element = product.find_element(By.CLASS_NAME, "current-price")
                product_price_text = price_element.text.strip().replace("₫", "").replace(",", "").strip()

                # Loại bỏ dấu chấm (nếu có) và chuyển đổi giá thành số nguyên
                product_price_text = product_price_text.replace(".", "")
                try:
                    product_price = int(product_price_text)
                except ValueError:
                    print(f"Lỗi khi chuyển đổi giá '{product_price_text}' thành số.")
                    continue

                # In ra giá sản phẩm đã kiểm tra
                print(f"Kiểm tra giá sản phẩm: {product.text} - {product_price}₫")

                # Kiểm tra nếu giá sản phẩm lớn hơn hoặc bằng giá sản phẩm trước đó (sắp xếp giá từ cao đến thấp)
                assert product_price <= prev_price, \
                    f"Giá sản phẩm '{product.text}' ({product_price}₫) không theo thứ tự từ cao đến thấp."

                # Cập nhật giá sản phẩm hiện tại
                prev_price = product_price

            # Cuộn trang tới khi gặp phần phân trang
            try:
                # Cuộn trang cho đến khi gặp phần phân trang
                while True:
                    # Kiểm tra xem phần phân trang có xuất hiện chưa
                    try:
                        pagination = driver.find_element(By.CLASS_NAME, "page-nav-list")
                        pages = pagination.find_elements(By.CLASS_NAME, "page-nav-item")
                        break  # Dừng cuộn khi gặp phần phân trang
                    except:
                        # Nếu phần phân trang chưa xuất hiện, cuộn thêm một đoạn
                        driver.execute_script("window.scrollBy(0, 300);")  # Cuộn một đoạn
                        time.sleep(2)  # Đợi lâu hơn để trang kịp tải thêm sản phẩm

                # Tìm số trang kế tiếp
                active_page = pagination.find_element(By.CLASS_NAME, "active")  # Trang hiện tại
                current_page_number = int(active_page.find_element(By.TAG_NAME, "a").text)  # Số trang hiện tại
                next_page_number = current_page_number + 1  # Trang kế tiếp là trang hiện tại + 1
                next_page = None

                # Tìm trang kế tiếp
                for page in pages:
                    page_number = int(page.find_element(By.TAG_NAME, "a").text)
                    if page_number == next_page_number:  # Tìm trang có số trang = trang hiện tại + 1
                        next_page = page
                        break

                if next_page:
                    # Thêm time.sleep trước khi nhấn vào trang tiếp theo
                    time.sleep(2)  # Thêm thời gian chờ trước khi nhấn vào trang kế tiếp

                    # Nhấp vào trang kế tiếp
                    click_element(driver, By.XPATH, f"//a[text()='{next_page_number}']")  # Click vào trang kế tiếp
                    time.sleep(2)  # Thêm thời gian chờ sau khi nhấn vào trang kế tiếp

                    page_count += 1
                else:
                    # Nếu không còn trang kế tiếp
                    break  # Dừng nếu không có trang kế tiếp

            except Exception as e:
                print(f"Lỗi khi cuộn hoặc phân trang: {str(e)}")
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
