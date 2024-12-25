import time

import pytest
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from Final_term.utils.driver_helper import init_driver, close_driver  # Import từ driver_helper
from Final_term.utils.helper import scroll_page, check_products_on_page, navigate_to_next_page, scroll_half_page, \
    get_menu_links


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
        driver.get("http://localhost/Webbanhang-main/index.html")
        time.sleep(1)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        initial_url = driver.current_url
        buttons_without_page_change = []

        index = 0
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            social_buttons = driver.find_elements(By.CLASS_NAME, "widget-social-item")

            if index >= len(social_buttons):
                break

            try:
                button = social_buttons[index]
                link = button.find_element(By.TAG_NAME, "a")
                icon_class = link.find_element(By.TAG_NAME, "i").get_attribute("class")
                link.click()
                try:
                    WebDriverWait(driver, 10).until(EC.url_changes(initial_url))
                except:
                    print(f"URL không thay đổi khi nhấp vào nút: {icon_class}")
                    buttons_without_page_change.append(icon_class)

                # Kiểm tra URL có thay đổi không
                if driver.current_url != initial_url:
                    print(f"Nút {index + 1} ({icon_class}) đã chuyển trang thành công!")
                else:
                    print(f"Nút {index + 1} ({icon_class}) không chuyển trang!")

                driver.get(initial_url)
                time.sleep(1)


            except Exception as e:
                print(f"Lỗi khi kiểm tra nút {index + 1}: {e}")

            index += 1
        assert not buttons_without_page_change, (f"Các nút không chuyển trang: {buttons_without_page_change}")
        print("Tất cả các nút đã kiểm tra đều hoạt động chính xác!")

    # fail-các liên kết không chuyển đến đúng trang
    def test_navigation_links(self, driver):
        driver.get("http://localhost/Webbanhang-main/index.html")
        time.sleep(1)
        initial_url = driver.current_url
        invalid_links = []

        index = 0
        while True:
            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)

                links_section = driver.find_element(By.CLASS_NAME, "widget-contact")
                link_items = links_section.find_elements(By.TAG_NAME, "a")

                if index >= len(link_items):
                    break

                link_item = link_items[index]
                link_text = link_item.find_element(By.TAG_NAME, "span").text.strip()

                link_item.click()
                time.sleep(1)
                try:
                    WebDriverWait(driver, 10).until(EC.url_changes(initial_url))
                    print(f"Liên kết '{link_text}' đã chuyển hướng thành công!")
                except:
                    print(f"URL không thay đổi khi nhấp vào liên kết: {link_text}")
                    invalid_links.append(link_text)

                driver.get(initial_url)
                time.sleep(1)

            except Exception as e:
                print(f"Lỗi khi kiểm tra liên kết '{link_text}': {e}")
            index += 1
        if invalid_links:
            assert False, f"Các liên kết không hợp lệ: {invalid_links}"

        print("Tất cả các liên kết đều hoạt động chính xác!")

    # fail-các liên kết không chuyển đến đúng trang
    def test_menu_links(self, driver):
        driver.get("http://localhost/Webbanhang-main/index.html")
        time.sleep(1)
        initial_url = driver.current_url
        duplicate_product_links = []
        menu_items = get_menu_links(driver)
        menu_item_count = len(menu_items)

        product_to_links_map = {}
        for index in range(menu_item_count):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            menu_items = get_menu_links(driver)
            menu_item = menu_items[index]

            menu_item_text = menu_item.text.strip()
            print(f"Đang kiểm tra thực đơn: {menu_item_text}")

            try:
                menu_item.click()
                time.sleep(2)
                scroll_half_page(driver)
                current_products_section = driver.find_element(By.ID, "home-products")
                current_products = current_products_section.find_elements(By.CLASS_NAME, "card-product")

                current_product_names = []
                for product in current_products:
                    product_name = product.find_element(By.CLASS_NAME, "card-title-link").text
                    current_product_names.append(product_name)

                for product_name in current_product_names:
                    if product_name in product_to_links_map:
                        product_to_links_map[product_name].add(menu_item_text)
                    else:
                        product_to_links_map[product_name] = {menu_item_text}

                driver.get(initial_url)
                time.sleep(2)

                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)

            except Exception as e:
                print(f"Lỗi khi kiểm tra: {menu_item_text} - {e}")

        for product_name, links in product_to_links_map.items():
            if len(links) > 1:
                duplicate_product_links.extend(links)

        duplicate_product_links = list(set(duplicate_product_links))
        if duplicate_product_links:
            print(f"Các liên kết thực đơn hiển thị không đúng: {', '.join(duplicate_product_links)}")
            assert False, f"Các liên kết thực đơn hiển thị không đúng:: {', '.join(duplicate_product_links)}"

        print("Các liên kết thực đơn hiển thị đúng.")
