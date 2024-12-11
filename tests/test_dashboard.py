import datetime
import time

from selenium.common import TimeoutException, NoSuchElementException
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



class TestDashBoard:

    def test_dashboard(self, driver):

        try:
            # Mở trang web
            driver.get("http://localhost/Webbanhang-main/index.html")
            time.sleep(1)

            # Đăng nhập vào hệ thống
            login(driver, "hgbaodev", "123456")
            time.sleep(4)

            # Mở trang admin
            click_element(driver, By.CLASS_NAME, "text-dndk")
            time.sleep(2)

            click_element(driver, By.XPATH, "//a[contains(text(), 'Quản lý cửa hàng')]")
            time.sleep(2)

            # Lấy số liệu từ dashboard
            amount_user = int(driver.find_element(By.ID, "amount-user").text.strip())
            amount_product = int(driver.find_element(By.ID, "amount-product").text.strip())
            doanh_thu = driver.find_element(By.ID, "doanh-thu").text.strip()

            print(f"Dashboard: Users: {amount_user}, Products: {amount_product}, Revenue: {doanh_thu}")

            # Mở danh mục sản phẩm
            click_element(driver, By.XPATH, "//div[@class='hidden-sidebar' and text()='Sản phẩm']")
            time.sleep(1)

            # Biến đếm tổng số sản phẩm
            total_products_counted = 0

            while True:
                # Đếm số lượng sản phẩm hiện tại trên trang
                products = driver.find_elements(By.CLASS_NAME, "list")
                total_products_counted += len(products)

                # Cuộn xuống cuối trang để đảm bảo các sản phẩm được tải đầy đủ
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)

                # Kiểm tra nút phân trang tiếp theo (nếu có)
                try:
                    # Xác định trang hiện tại
                    current_page = driver.find_element(By.XPATH, "//li[@class='page-nav-item active']/a").text.strip()
                    next_page_number = int(current_page) + 1  # Tính toán số trang tiếp theo

                    # Tìm nút của trang tiếp theo
                    next_page = driver.find_element(By.XPATH,
                                                    f"//li[@class='page-nav-item']/a[text()='{next_page_number}']")
                    next_page.click()
                    time.sleep(2)  # Đợi trang tiếp theo tải xong

                except NoSuchElementException:
                    # Nếu không tìm thấy nút của trang tiếp theo, dừng vòng lặp
                    break

            # In tổng số sản phẩm đếm được
            print(f"Tổng số sản phẩm đếm được: {total_products_counted}")

            # So sánh số lượng sản phẩm trên dashboard với số đếm được
            assert total_products_counted == amount_product, (
                f"Lỗi: Số sản phẩm trên dashboard ({amount_product}) không khớp với số đếm được ({total_products_counted})."
            )

            # Mở danh mục khách hàng
            click_element(driver, By.XPATH, "//div[@class='hidden-sidebar' and text()='Khách hàng']")
            time.sleep(3)

            # Đếm số lượng khách hàng trong trang hiện tại
            customers = driver.find_elements(By.XPATH,
                                             "//tbody[@id='show-user']/tr[td]")  # Chỉ lấy các hàng có dữ liệu thực
            total_customers_counted = len(customers)

            # In tổng số khách hàng đếm được
            print(f"Tổng số khách hàng đếm được: {total_customers_counted}")

            # So sánh số lượng khách hàng trên dashboard với số đếm được
            assert total_customers_counted == amount_user, (
                f"Lỗi: Số khách hàng trên dashboard ({amount_user}) không khớp với số đếm được ({total_customers_counted})."
            )

            # Mở danh mục đơn hàng
            click_element(driver, By.XPATH,
                          "//li[contains(@class, 'sidebar-list-item') and .//div[@class='hidden-sidebar'][contains(text(), 'Đơn hàng')]]")
            time.sleep(4)

            # Biến đếm tổng doanh thu từ các đơn hàng
            total_orders_revenue = 0

            # Lấy tất cả các dòng trong bảng đơn hàng
            orders = driver.find_elements(By.XPATH, "//tbody[@id='showOrder']//tr")

            # Duyệt qua từng đơn hàng và lấy tổng tiền
            for order in orders:
                try:
                    # Tìm kiếm cột 'Tổng tiền' trong mỗi đơn hàng (Cột thứ 4)
                    total_price_cell = order.find_element(By.XPATH, ".//td[4]")  # Cột 'Tổng tiền'

                    # Lấy giá trị tiền từ cột 'Tổng tiền', loại bỏ các ký tự không cần thiết
                    total_price_text = total_price_cell.text.strip()

                    # Làm sạch giá trị tiền
                    total_price_clean = total_price_text.replace("₫", "").replace("\u00a0", "").replace(".", "").strip()

                    # Kiểm tra nếu giá trị là một số hợp lệ
                    if total_price_clean.isdigit():
                        total_orders_revenue += int(total_price_clean)  # Cộng vào tổng doanh thu
                    else:
                        print(f"Giá trị không hợp lệ: {total_price_clean}")

                except Exception as e:
                    print(f"Lỗi khi xử lý đơn hàng: {str(e)}")

            # In ra tổng doanh thu từ các đơn hàng
            print(f"Tổng doanh thu từ các đơn hàng: {total_orders_revenue}₫")

            # So sánh tổng doanh thu từ đơn hàng với doanh thu trên dashboard
            dashboard_revenue = int(doanh_thu.replace(".", "").replace("₫", "").strip())  # Làm sạch và chuyển thành số
            assert total_orders_revenue == dashboard_revenue, (
                f"Lỗi: Doanh thu từ đơn hàng ({total_orders_revenue}₫) không khớp với doanh thu trên dashboard ({dashboard_revenue}₫)."
            )


        finally:
            # Đảm bảo luôn logout sau khi kiểm tra xong
            logout_admin(driver)

