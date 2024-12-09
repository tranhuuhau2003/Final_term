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
from selenium.webdriver.common.by import By
from datetime import datetime



@pytest.fixture
def driver():
    """
    Khởi tạo WebDriver với profile Chrome được định trước.
    """
    profile_path = "C:\\Users\\user\\AppData\\Local\\Google\\Chrome\\User Data"
    profile_directory = "Default"  # Đây là profile mà bạn muốn sử dụng (ví dụ: "Default", "Profile 1",...)

    options = webdriver.ChromeOptions()
    options.add_argument(f"user-data-dir={profile_path}")  # Chỉ định thư mục chứa profile
    options.add_argument(f"profile-directory={profile_directory}")  # Chỉ định tên thư mục profile

    driver = webdriver.Chrome(options=options)
    driver.maximize_window()

    try:
        yield driver  # Cung cấp driver cho test
    finally:
        driver.quit()  # Đóng trình duyệt

@pytest.fixture
def setup_and_teardown(driver):
    """
    Fixture đảm bảo logout sau mỗi test.
    """
    try:
        yield driver  # Sử dụng driver từ fixture `driver`
    finally:
        # Đăng xuất trước khi teardown
        try:
            logout_admin(driver)
        except Exception as e:
            print(f"Không thể đăng xuất: {e}")

class TestStatistics:
    def test_search_product_in_statistics(self, driver):
        """
        Kiểm tra tìm kiếm tên món trong trang thống kê với các từ khóa có sản phẩm tồn tại.
        """
        try:
            # Mở trang web
            driver.get("http://localhost/Webbanhang-main/index.html")

            # Đăng nhập
            login(driver, "hgbaodev", "123456")
            time.sleep(4)

            # Điều hướng đến trang thống kê
            click_element(driver, By.CLASS_NAME, "text-dndk")

            # Chờ "Quản lý cửa hàng" xuất hiện và nhấn vào
            click_element(driver, By.XPATH, "//a[contains(text(), 'Quản lý cửa hàng')]")

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
        """
        Kiểm tra tìm kiếm sản phẩm tồn tại trong trang thống kê.
        """
        try:
            # Mở trang web
            driver.get("http://localhost/Webbanhang-main/index.html")

            # Đăng nhập
            login(driver, "hgbaodev", "123456")
            time.sleep(4)

            # Điều hướng đến trang thống kê
            click_element(driver, By.CLASS_NAME, "text-dndk")
            click_element(driver, By.XPATH, "//a[contains(text(), 'Quản lý cửa hàng')]")
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
        """
        Kiểm tra tìm kiếm sản phẩm không tồn tại trong trang thống kê.
        """
        try:
            # Mở trang web
            driver.get("http://localhost/Webbanhang-main/index.html")

            # Đăng nhập
            login(driver, "hgbaodev", "123456")
            time.sleep(4)

            # Điều hướng đến trang thống kê
            click_element(driver, By.CLASS_NAME, "text-dndk")
            click_element(driver, By.XPATH, "//a[contains(text(), 'Quản lý cửa hàng')]")
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
        """
        Kiểm tra chức năng lọc theo danh mục trong trang thống kê.
        Đảm bảo không có sản phẩm nào xuất hiện ở nhiều hơn một danh mục (trừ danh mục "Tất cả").
        """
        try:
            # Mở trang web
            driver.get("http://localhost/Webbanhang-main/index.html")

            # Đăng nhập
            login(driver, "hgbaodev", "123456")
            time.sleep(4)

            # Điều hướng đến trang thống kê
            click_element(driver, By.CLASS_NAME, "text-dndk")
            click_element(driver, By.XPATH, "//a[contains(text(), 'Quản lý cửa hàng')]")
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

# code chưa sửa xong
    def test_filter_statistics_by_date_with_modal1(self, driver):
        """
        Kiểm tra chức năng lọc theo ngày trong trang thống kê khi dữ liệu ngày nằm trong modal.
        """
        try:
            # Mở trang web
            driver.get("http://localhost/Webbanhang-main/index.html")

            # Đăng nhập
            login(driver, "hgbaodev", "123456")
            time.sleep(4)

            # Điều hướng đến trang thống kê
            click_element(driver, By.CLASS_NAME, "text-dndk")
            click_element(driver, By.XPATH, "//a[contains(text(), 'Quản lý cửa hàng')]")
            click_element(driver, By.XPATH, "//div[@class='hidden-sidebar' and text()='Thống kê']")
            time.sleep(1)

            # Nhập ngày kết thúc
            fill_input(driver, By.ID, "time-end-tk", "12-20-2024")  # Nhập ngày theo định dạng MM-DD-YYYY
            time.sleep(2)

            # Nhập ngày bắt đầu
            fill_input(driver, By.ID, "time-start-tk", "12-01-2024")  # Nhập ngày theo định dạng MM-DD-YYYY
            time.sleep(2)

            # Đợi bảng dữ liệu xuất hiện
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "showTk")))
                table = driver.find_element(By.ID, "showTk")
                rows = table.find_elements(By.TAG_NAME, "tr")

                if len(rows) == 0:
                    print("Bảng không có dữ liệu, kiểm thử thành công.")
                    assert True, "Bảng không có dữ liệu, không cần kiểm tra thêm."
                    return

                # Chuyển đổi ngày bắt đầu và kết thúc thành datetime
                start_date = datetime.strptime("12-01-2024", "%m-%d-%Y")
                end_date = datetime.strptime("12-20-2024", "%m-%d-%Y")

                valid_count = 0
                # Duyệt qua từng hàng để mở modal và kiểm tra logic ngày
                for i, row in enumerate(rows):
                    try:
                        # Nhấp vào nút "Chi tiết" trong hàng để mở modal
                        detail_button = row.find_element(By.XPATH, ".//td/button[contains(text(), 'Chi tiết')]")
                        detail_button.click()

                        # Đợi modal xuất hiện
                        WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CLASS_NAME, "modal-container"))
                        )

                        # Lấy danh sách hàng trong modal
                        modal_table = driver.find_element(By.ID, "show-product-order-detail")
                        modal_rows = modal_table.find_elements(By.TAG_NAME, "tr")

                        for j, modal_row in enumerate(modal_rows):
                            try:
                                # Lấy ngày từ cột "Ngày đặt"
                                date_text = modal_row.find_element(By.XPATH, "./td[4]").text.strip()
                                date_obj = datetime.strptime(date_text, "%d/%m/%Y")  # Định dạng dd/MM/yyyy

                                if start_date <= date_obj <= end_date:
                                    print(f"Hàng {i + 1}, dòng chi tiết {j + 1}: {date_text} hợp lệ.")
                                    valid_count += 1
                                else:
                                    print(
                                        f"Hàng {i + 1}, dòng chi tiết {j + 1}: {date_text} không nằm trong khoảng ngày lọc."
                                    )
                            except Exception as e:
                                print(f"Lỗi xử lý dòng chi tiết {j + 1} trong hàng {i + 1}: {e}")

                        # Đóng modal
                        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "modal-close")))
                        close_button = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.CLASS_NAME, "modal-close")))

                        driver.execute_script("arguments[0].scrollIntoView(true);", close_button)
                        driver.execute_script("document.querySelector('.modal-close').click();")

                        # Đợi modal đóng
                        WebDriverWait(driver, 10).until(
                            EC.invisibility_of_element_located((By.CLASS_NAME, "modal-container"))
                        )


                    except Exception as e:
                        print(f"Lỗi xử lý hàng {i + 1}: {e}")

                # Kiểm tra kết quả lọc
                assert valid_count > 0, "Không có dữ liệu nào trong khoảng ngày lọc."
                print(f"Tìm thấy {valid_count} dữ liệu hợp lệ.")

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

    def test_sort_by_sales_ascending(self, driver):
        """
        Kiểm tra chức năng thống kê sản phẩm theo số lượng bán từ thấp đến cao.
        """
        # Mở trang web
        driver.get("http://localhost/Webbanhang-main/index.html")

        # Đăng nhập
        login(driver, "hgbaodev", "123456")
        time.sleep(4)

        # Điều hướng đến trang thống kê
        click_element(driver, By.CLASS_NAME, "text-dndk")
        click_element(driver, By.XPATH, "//a[contains(text(), 'Quản lý cửa hàng')]")
        click_element(driver, By.XPATH, "//div[@class='hidden-sidebar' and text()='Thống kê']")
        time.sleep(1)

        # Nhấn vào nút tăng dần
        sort_ascending_btn = driver.find_element(By.CSS_SELECTOR, "button[onclick='thongKe(1)']")
        sort_ascending_btn.click()
        time.sleep(1)  # Thêm thời gian chờ để thống kê xong

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
        """
        Kiểm tra chức năng thống kê sản phẩm theo số lượng bán từ cao đến thấp.
        """
        # Mở trang web
        driver.get("http://localhost/Webbanhang-main/index.html")

        # Đăng nhập
        login(driver, "hgbaodev", "123456")
        time.sleep(4)

        # Điều hướng đến trang thống kê
        click_element(driver, By.CLASS_NAME, "text-dndk")
        click_element(driver, By.XPATH, "//a[contains(text(), 'Quản lý cửa hàng')]")
        click_element(driver, By.XPATH, "//div[@class='hidden-sidebar' and text()='Thống kê']")
        time.sleep(1)

        # Nhấn vào nút giảm dần (nút giảm dần có thể khác, bạn cần thay thế đúng nút nếu cần)
        sort_descending_btn = driver.find_element(By.CSS_SELECTOR,
                                                  "button[onclick='thongKe(0)']")  # Giả sử đây là nút giảm dần
        sort_descending_btn.click()
        time.sleep(1)  # Thêm thời gian chờ để thống kê xong

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
