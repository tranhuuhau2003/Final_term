import time

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait

from Final_term.utils.driver_helper import init_driver, close_driver  # Import từ driver_helper
from Final_term.utils.helper import click_element, fill_input, check_toast_message, logout_admin, \
    navigate_to_product_category, select_dropdown_option, clear_and_send_keys


@pytest.fixture
def driver():
    driver = init_driver()  # Gọi hàm khởi tạo driver từ file driver_helper
    yield driver  # Cung cấp driver cho test
    close_driver(driver)  # Đóng driver sau khi test xong

class TestProductManagement:

    def test_add_product(self, driver):
        try:
            navigate_to_product_category(driver, "hgbaodev", "123456")

            click_element(driver, By.ID, "btn-add-product")

            fill_input(driver, By.ID, "ten-mon", "Món mới")

            select_dropdown_option(driver, By.ID, "chon-mon", "Món mặn")
            fill_input(driver, By.ID, "gia-moi", "100000")
            fill_input(driver, By.ID, "mo-ta", "Mô tả món ăn mới")

            click_element(driver, By.ID, "add-product-button")

            toast_success = check_toast_message(driver, "toast__msg", "Thêm sản phẩm thành công!")
            assert toast_success, "Thông báo thêm sản phẩm không hiển thị!"

            product_list = driver.find_element(By.XPATH, "//div[@id='show-product']")

            product_found = False
            product_items = product_list.find_elements(By.XPATH, ".//div[@class='list']")
            for product in product_items:
                product_name_in_list = product.find_element(By.XPATH, ".//div[@class='list-info']/h4").text
                if product_name_in_list == "Món mới":
                    product_found = True
                    break

            assert product_found, "Sản phẩm chưa được thêm vào danh sách"
            print("Thêm sản phẩm thành công!")
        finally:
            logout_admin(driver)


    def test_edit_product_information(self, driver):

        try:
            navigate_to_product_category(driver, "hgbaodev", "123456")

            product_name = "Rau xào ngũ sắc"  # Tên sản phẩm cần sửa
            product_row = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//h4[text()='{product_name}']/ancestor::div[@class='list']"))
            )

            edit_button = product_row.find_element(By.CLASS_NAME, "btn-edit")
            edit_button.click()
            time.sleep(2)

            new_name = "Rau xào ngũ sắc"
            new_description = "Món ăn ngon"
            new_category = "Món chay"
            new_price = "300000"

            fill_input(driver, By.ID, "ten-mon", new_name)
            select_dropdown_option(driver, By.ID, "chon-mon", "Món mặn")
            fill_input(driver, By.ID, "mo-ta", new_description)
            fill_input(driver, By.ID, "gia-moi", new_price)

            click_element(driver, By.ID, "update-product-button")

            toast_success = check_toast_message(driver, "toast__msg", "Sửa sản phẩm thành công!")
            assert toast_success, "Thông báo sửa sản phẩm không hiển thị!"

            clear_and_send_keys(driver, By.ID, "form-search-product", "Rau xào ngũ sắc")

            search_results = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "list"))
            )
            assert len(search_results) > 0, f"Không tìm thấy sản phẩm vừa chỉnh sửa"

            for result in search_results:
                product_name_element = result.find_element(By.CLASS_NAME, "list-info").find_element(By.TAG_NAME, "h4")
                product_name = product_name_element.text.strip().lower()  # Lấy tên sản phẩm và chuẩn hóa
                assert new_name.lower() in product_name, f"Sản phẩm '{product_name}' không khớp với từ khóa '{new_name}'"

                product_description_element = result.find_element(By.CLASS_NAME, "list-info").find_element( By.CLASS_NAME, "list-note")
                product_description = product_description_element.text.strip().lower()  # Lấy mô tả và chuẩn hóa
                assert new_description.lower() in product_description, f"Mô tả sản phẩm không khớp với '{new_description}'"

                product_category_element = result.find_element(By.CLASS_NAME, "list-info").find_element(By.CLASS_NAME,"list-category")
                product_category = product_category_element.text.strip().lower()  # Lấy loại món và chuẩn hóa
                assert new_category.lower() in product_category, f"Loại món không khớp với '{new_category}'"

                product_price_element = result.find_element(By.CLASS_NAME, "list-right").find_element(By.CLASS_NAME,"list-current-price")
                product_price = product_price_element.text.strip().replace('đ', '').replace(',','').lower()  # Lấy giá và chuẩn hóa
                assert new_price in product_price, f"Giá sản phẩm không khớp với '{new_price}'"

            print(f"Sửa thông tin sản phẩm thành công!")

        finally:
            logout_admin(driver)

    def test_delete_product(self, driver):
        try:
            navigate_to_product_category(driver, "hgbaodev", "123456")

            product_list = driver.find_element(By.XPATH, "//div[@id='show-product']")
            first_product_item = product_list.find_element(By.XPATH, ".//div[@class='list']")

            product_name = first_product_item.find_element(By.XPATH, ".//div[@class='list-info']/h4").text

            assert product_name, "Không tìm thấy sản phẩm trong danh sách."
            print(f"Đã tìm thấy sản phẩm: {product_name}")

            delete_button = first_product_item.find_element(By.XPATH, ".//button[@class='btn-delete']")
            delete_button.click()

            time.sleep(1)
            alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
            alert.accept()  # Nhấn OK trong thông báo xác nhận xóa

            toast_success = check_toast_message(driver, "toast__msg", "Xóa sản phẩm thành công !")
            assert toast_success, "Thông báo sửa sản phẩm không hiển thị!"

            is_invisible = WebDriverWait(driver, 10).until(
                EC.invisibility_of_element_located((By.XPATH, f"//div[contains(text(), '{product_name}')]"))
            )
            assert is_invisible, f"Sản phẩm '{product_name}' vẫn chưa bị xóa."
            print(f"Sản phẩm '{product_name}' đã được xóa thành công.")

        finally:
            logout_admin(driver)

    def test_search_existing_product(self, driver):

        try:
            navigate_to_product_category(driver, "hgbaodev", "123456")

            existing_products = ["nấm", "nấm chay", "đậu hũ xào nấm chay"]

            for product in existing_products:
                print(f"Tìm kiếm sản phẩm: {product}")

                clear_and_send_keys(driver, By.ID, "form-search-product", product)

                search_results = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "list")) )
                assert len(search_results) > 0, f"Không tìm thấy sản phẩm nào với từ khóa: {product}"

                for result in search_results:
                    product_name_element = result.find_element(By.CLASS_NAME, "list-info").find_element(By.TAG_NAME,"h4")
                    product_name = product_name_element.text.lower()
                    assert product.lower() in product_name, f"Sản phẩm '{product_name}' không khớp với từ khóa '{product}'"

                print(f"Tìm kiếm sản phẩm '{product}' thành công. Tất cả kết quả đều khớp!")

        finally:
            logout_admin(driver)

    def test_search_nonexistent_product(self, driver):

        try:
            navigate_to_product_category(driver, "hgbaodev", "123456")

            nonexistent_keywords = ["bún mắm", "cơm cuộn"]

            for nonexistent_keyword in nonexistent_keywords:
                print(f"Tìm kiếm sản phẩm không tồn tại: {nonexistent_keyword}")

                clear_and_send_keys(driver, By.ID, "form-search-product", nonexistent_keyword)

                no_results_message = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "no-result-h"))
                )
                assert "Không có sản phẩm để hiển thị" in no_results_message.text, f"Nội dung thông báo không đúng: {no_results_message.text}"

                print(f"Thông báo chính xác khi tìm kiếm sản phẩm không tồn tại.")

        finally:
            logout_admin(driver)

    # fail-vì xuất hiện các sản phẩm đã xóa trong các danh mục khác
    def test_filter_by_category(self, driver):
        navigate_to_product_category(driver, "hgbaodev", "123456")

        select_dropdown_option(driver, By.ID, "the-loai", "Đã xóa")

        product_list = driver.find_element(By.XPATH, "//div[@id='show-product']")
        deleted_product_items = product_list.find_elements(By.XPATH, ".//div[@class='list']")
        deleted_products = [item.find_element(By.XPATH, ".//div[@class='list-info']/h4").text for item in deleted_product_items]

        category_select = driver.find_element(By.ID, "the-loai")
        category_options = category_select.find_elements(By.TAG_NAME, "option")

        for option in category_options:
            category_name = option.text
            if category_name == "Đã xóa":
                continue

            category_select.click()  # Mở combobox
            option.click()
            time.sleep(2)

            product_list = driver.find_element(By.XPATH, "//div[@id='show-product']")
            product_items = product_list.find_elements(By.XPATH, ".//div[@class='list']")
            product_names = [item.find_element(By.XPATH, ".//div[@class='list-info']/h4").text for item in product_items]

            for deleted_product in deleted_products:
                if deleted_product in product_names:
                    assert False, f"Sản phẩm '{deleted_product}' từ danh mục 'Đã xóa' xuất hiện trong danh mục '{category_name}'"

        print("Kiểm thử lọc sản phẩm theo danh mục thành công.")



    def test_reset_product_page(self, driver):

        try:
            navigate_to_product_category(driver, "hgbaodev", "123456")

            select_dropdown_option(driver, By.ID, "the-loai", "Món chay")

            click_element(driver, By.ID, "btn-cancel-product")
            time.sleep(2)

            selected_option = WebDriverWait(driver, 10).until(lambda d: Select(d.find_element(By.ID, "the-loai")).first_selected_option)

            assert selected_option.text == "Tất cả", "Dropdown không reset về giá trị 'Tất cả'. Làm mới trang quản lý sản phẩm thất bại!"

            print("Làm mới trang quản lý sản phẩm thành công.")

        finally:
            logout_admin(driver)
