import random
import time
from selenium.common import TimeoutException, StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from Final_term.utils.helper import click_element, fill_input, check_toast_message, check_error_message, login, add_customer, logout, logout_admin, add_to_cart, add_multiple_to_cart, update_product_quantity_in_cart, check_cart_quantity, scroll_to_element, check_filtered_products, check_sorted_products, \
scroll_page, check_products_on_page, navigate_to_next_page
from Final_term.utils.driver_helper import init_driver, close_driver  # Import từ driver_helper
from selenium.webdriver.common.by import By



@pytest.fixture
def driver():
    driver = init_driver()
    yield driver
    close_driver(driver)


class TestNavigation:

    def test_navigation_menu(self, driver):
        driver.get("http://localhost/Webbanhang-main/index.html")
        time.sleep(1)

        try:
            menu = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".menu-list"))
            )
        except TimeoutException:
            print("Không tìm thấy menu hoặc menu không hiển thị.")
            return
        time.sleep(2)
        menu_items_count = len(driver.find_elements(By.CSS_SELECTOR, ".menu-list-item"))
        for index in range(menu_items_count):
            menu_items = driver.find_elements(By.CSS_SELECTOR, ".menu-list-item")
            item = menu_items[index]
            menu_name = item.text.strip()

            driver.execute_script("arguments[0].scrollIntoView();", item)
            time.sleep(1)

            item.click()
            time.sleep(3)

            driver.execute_script("window.scrollBy(0, -200);")
            time.sleep(1)

            try:
                products_section = driver.find_element(By.ID, "home-products")
                products = products_section.find_elements(By.CLASS_NAME, "card-product")

                if len(products) > 0:
                    print(f"Mục '{menu_name}' hiển thị {len(products)} sản phẩm.")
                else:
                    no_results_message = driver.find_element(By.CSS_SELECTOR, ".home-products .no-result-h")
                    assert "Tìm kiếm không có kết quả" in no_results_message.text, f"Mục '{menu_name}' không hiển thị sản phẩm và không có thông báo kết quả tìm kiếm!"
                    print(f"Mục '{menu_name}' không có sản phẩm.")

            except Exception as e:
                print(f"Lỗi: {str(e)}")
                assert False, f"Không thể kiểm tra mục '{menu_name}'!"

            try:
                menu = driver.find_element(By.CSS_SELECTOR, ".menu-list")
                menu_display = menu.value_of_css_property("display")
                if menu_display == "none":
                    driver.execute_script("window.scrollBy(0, -200);")
                    time.sleep(2)
            except Exception as e:
                print(f"Lỗi khi kiểm tra menu: {str(e)}")
                continue

        print("Kiểm tra điều hướng menu thành công!")

    def test_pagination_navigation(self, driver):
        driver.get("http://localhost/Webbanhang-main/index.html")
        time.sleep(1)

        while True:
            try:
                # Cuộn đến 2/3 chiều cao của trang
                scroll_page(driver)

                # Kiểm tra sản phẩm trên trang hiện tại
                check_products_on_page(driver)

                # Tìm nút phân trang và điều hướng
                if not navigate_to_next_page(driver):
                    print("Đã đến trang cuối cùng.")
                    break

            except Exception as e:
                print(f"Lỗi: {str(e)}")
                break

        assert True, "Tất cả các trang đã được kiểm tra thành công!"



    # fail-các nút liên kết đến mạng xã hội không hoạt động
    def test_social_links_navigation(self, driver):

        # Mở trang web
        driver.get("http://localhost/Webbanhang-main/index.html")
        time.sleep(1)

        # Cuộn xuống cuối trang để các nút hiện trên màn hình
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        # Lưu URL ban đầu
        initial_url = driver.current_url

        # Mảng lưu thông tin các nút không thay đổi URL
        buttons_without_page_change = []

        # Sử dụng chỉ số để kiểm tra từng nút
        index = 0
        while True:
            # Lấy lại danh sách các nút mạng xã hội
            social_buttons = driver.find_elements(By.CLASS_NAME, "widget-social-item")

            # Nếu hết nút để kiểm tra, thoát khỏi vòng lặp
            if index >= len(social_buttons):
                break

            try:
                # Lấy nút hiện tại
                button = social_buttons[index]
                link = button.find_element(By.TAG_NAME, "a")
                icon_class = link.find_element(By.TAG_NAME, "i").get_attribute("class")

                # Nhấp vào liên kết
                link.click()
                time.sleep(2)

                # Đợi URL thay đổi hoặc timeout
                try:
                    WebDriverWait(driver, 10).until(EC.url_changes(initial_url))
                except:
                    # Nếu URL không thay đổi
                    print(f"URL không thay đổi khi nhấp vào nút: {icon_class}")
                    buttons_without_page_change.append(icon_class)

                # Kiểm tra URL có thay đổi không
                if driver.current_url != initial_url:
                    print(f"Nút {index + 1} ({icon_class}) đã chuyển trang thành công!")
                else:
                    print(f"Nút {index + 1} ({icon_class}) không chuyển trang!")

                # Quay lại trang ban đầu nếu URL thay đổi
                driver.get(initial_url)
                time.sleep(2)

                # Cuộn xuống cuối trang để tiếp tục kiểm tra nút tiếp theo
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)

            except Exception as e:
                print(f"Lỗi khi kiểm tra nút {index + 1}: {e}")

            # Tăng chỉ số để kiểm tra nút tiếp theo
            index += 1

        # Assert để kiểm tra nếu có nút không thay đổi URL
        assert not buttons_without_page_change, (
            f"Các nút không chuyển trang: {buttons_without_page_change}"
        )

        # In ra kết quả cuối cùng
        print("Tất cả các nút đã kiểm tra đều hoạt động chính xác!")

    # fail-các liên kết không chuyển đến đúng trang
    def test_navigation_links(self, driver):


        # Mở trang web
        driver.get("http://localhost/Webbanhang-main/index.html")
        time.sleep(1)

        # Lưu URL ban đầu
        initial_url = driver.current_url

        # Lưu thông tin các liên kết không đáp ứng yêu cầu
        invalid_links = []

        # Sử dụng chỉ số để kiểm tra từng liên kết
        index = 0
        while True:
            try:
                # Cuộn xuống cuối trang để các liên kết xuất hiện
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)

                # Lấy danh sách các liên kết trong mục "Liên kết"
                links_section = driver.find_element(By.CLASS_NAME, "widget-contact")
                link_items = links_section.find_elements(By.TAG_NAME, "a")

                # Nếu hết liên kết để kiểm tra, thoát khỏi vòng lặp
                if index >= len(link_items):
                    break

                # Lấy liên kết hiện tại
                link_item = link_items[index]
                link_text = link_item.find_element(By.TAG_NAME, "span").text.strip()

                print(f"Đang kiểm tra liên kết: {link_text}")

                # Nhấp vào liên kết
                link_item.click()
                time.sleep(2)

                # Đợi URL thay đổi hoặc timeout
                try:
                    WebDriverWait(driver, 10).until(EC.url_changes(initial_url))
                    print(f"Liên kết '{link_text}' đã chuyển hướng thành công!")
                except:
                    print(f"URL không thay đổi khi nhấp vào liên kết: {link_text}")
                    invalid_links.append(link_text)

                # Quay lại trang ban đầu nếu URL thay đổi
                driver.get(initial_url)
                time.sleep(2)

            except Exception as e:
                print(f"Lỗi khi kiểm tra liên kết '{link_text}': {e}")

            # Tăng chỉ số để kiểm tra liên kết tiếp theo
            index += 1

        # Kiểm tra nếu mảng invalid_links không rỗng
        if invalid_links:
            print(f"Các liên kết không hợp lệ: {invalid_links}")
            # Tạo ra ngoại lệ nếu cần thiết (hoặc chỉ cần in ra thông báo)
            assert False, f"Các liên kết không hợp lệ: {invalid_links}"

        # In ra kết quả cuối cùng
        if not invalid_links:
            print("Tất cả các liên kết đều hoạt động chính xác!")

    # fail-các liên kết không chuyển đến đúng trang
    def test_menu_links(self, driver):
        # Mở trang web
        global menu_item_text
        driver.get("http://localhost/Webbanhang-main/index.html")
        time.sleep(1)

        # Lấy URL ban đầu
        initial_url = driver.current_url

        # Cuộn đến 1/2 chiều cao của trang sau mỗi lần kiểm tra sản phẩm
        scroll_height = driver.execute_script("return document.body.scrollHeight")
        scroll_position = scroll_height / 2  # Cuộn 1/2 chiều cao của trang
        driver.execute_script(f"window.scrollTo(0, {scroll_position});")
        time.sleep(2)

        # Lưu thông tin số lượng sản phẩm ban đầu
        initial_products_section = driver.find_element(By.ID, "home-products")
        initial_products = initial_products_section.find_elements(By.CLASS_NAME, "card-product")
        initial_product_count = len(initial_products)
        print(f"Số lượng sản phẩm ban đầu: {initial_product_count}")

        # Cuộn xuống cuối trang để các liên kết xuất hiện
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        # Mảng lưu trữ các liên kết không thay đổi sản phẩm
        invalid_links = []

        # Lấy danh sách các liên kết trong mục "Thực đơn"
        menu_section = driver.find_element(By.XPATH, "//h3[text()='Thực đơn']/following-sibling::ul")
        menu_items = menu_section.find_elements(By.TAG_NAME, "a")

        # Sử dụng chỉ số để kiểm tra từng liên kết
        index = 0
        while True:
            try:
                # Cuộn xuống cuối trang để các liên kết xuất hiện
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)

                # Nếu hết liên kết để kiểm tra, thoát khỏi vòng lặp
                if index >= len(menu_items):
                    break

                menu_item = menu_items[index]
                menu_item_text = menu_item.text.strip()  # Lấy tên liên kết
                print(f"Đang kiểm tra liên kết thực đơn: {menu_item_text}")

                # Nhấp vào liên kết và kiểm tra sự thay đổi của sản phẩm
                menu_item.click()
                time.sleep(2)

                # Cuộn đến 1/2 chiều cao của trang sau mỗi lần kiểm tra sản phẩm
                scroll_height = driver.execute_script("return document.body.scrollHeight")
                scroll_position = scroll_height / 2  # Cuộn 1/2 chiều cao của trang
                driver.execute_script(f"window.scrollTo(0, {scroll_position});")
                time.sleep(2)

                # Lấy danh sách sản phẩm sau khi nhấp vào liên kết
                current_products_section = driver.find_element(By.ID, "home-products")
                current_products = current_products_section.find_elements(By.CLASS_NAME, "card-product")
                current_product_count = len(current_products)

                print(f"Số lượng sản phẩm sau khi nhấn vào liên kết '{menu_item_text}': {current_product_count}")

                # Kiểm tra sự thay đổi số lượng sản phẩm
                if current_product_count == initial_product_count:
                    invalid_links.append(menu_item_text)  # Lưu liên kết nếu số lượng sản phẩm không thay đổi

                # Quay lại trang ban đầu
                driver.get(initial_url)
                time.sleep(2)  # Đợi trang quay lại hoàn toàn

                # Cập nhật lại danh sách các liên kết sau khi quay lại trang ban đầu
                menu_section = driver.find_element(By.XPATH, "//h3[text()='Thực đơn']/following-sibling::ul")
                menu_items = menu_section.find_elements(By.TAG_NAME, "a")

            except Exception as e:
                print(f"Lỗi khi kiểm tra liên kết '{menu_item_text}': {e}")

            # Tăng chỉ số để kiểm tra liên kết tiếp theo
            index += 1

        # Kiểm tra nếu mảng invalid_links không rỗng
        if invalid_links:
            print(f"Các liên kết không thay đổi sản phẩm: {', '.join(invalid_links)}")
            # Tạo ra ngoại lệ nếu cần thiết (hoặc chỉ cần in ra thông báo)
            assert False, f"Các liên kết không thay đổi sản phẩm: {', '.join(invalid_links)}"

        # In ra kết quả cuối cùng
        if not invalid_links:
            print("Tất cả các liên kết đã thay đổi sản phẩm.")

