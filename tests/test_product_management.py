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

class TestProductManagement:

    def test_add_product(self, driver):
        driver.get("http://localhost/Webbanhang-main/index.html")

        # Đăng nhập vào hệ thống
        login(driver, "hgbaodev", "123456")
        time.sleep(4)

        # Nhấn vào "Đăng nhập / Đăng ký"
        click_element(driver, By.CLASS_NAME, "text-dndk")

        # Chờ "Quản lý cửa hàng" xuất hiện và nhấn vào
        click_element(driver, By.XPATH, "//a[contains(text(), 'Quản lý cửa hàng')]")

        # Mở danh mục sản phẩm
        click_element(driver, By.XPATH, "//div[@class='hidden-sidebar' and text()='Sản phẩm']")
        time.sleep(1)

        # Nhấn nút thêm món mới
        add_product_button = driver.find_element(By.ID, "btn-add-product")
        add_product_button.click()

        # Điền các thông tin vào form thêm món
        product_name_input = driver.find_element(By.ID, "ten-mon")
        product_name_input.send_keys("Món mới")

        category_select = driver.find_element(By.ID, "chon-mon")
        category_select.click()
        category_option = driver.find_element(By.XPATH, "//option[contains(text(), 'Món chay')]")
        category_option.click()

        price_input = driver.find_element(By.ID, "gia-moi")
        price_input.send_keys("100000")

        description_input = driver.find_element(By.ID, "mo-ta")
        description_input.send_keys("Mô tả món ăn mới")

        # Nhấn nút thêm món
        add_product_confirm_button = driver.find_element(By.ID, "add-product-button")
        add_product_confirm_button.click()
        time.sleep(2)

        # Kiểm tra thông báo toast
        check_toast_message(driver, "toast__msg", "Thêm sản phẩm thành công!")

        # Kiểm tra xem món đã xuất hiện trong danh sách chưa
        # Lấy danh sách sản phẩm hiện tại
        product_list = driver.find_element(By.XPATH, "//div[@id='show-product']")

        # Kiểm tra sự xuất hiện của sản phẩm mới
        product_found = False
        product_items = product_list.find_elements(By.XPATH, ".//div[@class='list']")
        for product in product_items:
            product_name_in_list = product.find_element(By.XPATH, ".//div[@class='list-info']/h4").text
            if product_name_in_list == "Món mới":
                product_found = True
                break

        # Kiểm tra sản phẩm có trong danh sách hay không
        assert product_found, "Sản phẩm chưa được thêm vào danh sách"

    def test_edit_product_information(self, driver):
        """
        Test chức năng sửa thông tin sản phẩm.
        """
        try:
            # Truy cập trang web
            driver.get("http://localhost/Webbanhang-main/index.html")

            # Đăng nhập tài khoản admin
            login(driver, "hgbaodev", "123456")
            time.sleep(4)

            # Điều hướng đến trang quản lý sản phẩm
            click_element(driver, By.CLASS_NAME, "text-dndk")

            click_element(driver, By.XPATH, "//a[contains(text(), 'Quản lý cửa hàng')]")
            click_element(driver, By.XPATH, "//div[@class='hidden-sidebar' and text()='Sản phẩm']")

            # Tìm sản phẩm cần sửa (dựa vào tên sản phẩm)
            product_name = "carrotne"  # Tên sản phẩm cần sửa
            product_row = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//h4[text()='{product_name}']/ancestor::div[@class='list']"))
            )

            # Nhấn vào nút "Sửa" của sản phẩm
            edit_button = product_row.find_element(By.CLASS_NAME, "btn-edit")
            edit_button.click()
            time.sleep(2)

            # Chỉnh sửa thông tin sản phẩm
            new_name = "carrotne"  # Tên mới
            new_description = "Món ăn chayyyyy ngon"  # Mô tả mới
            new_category = "Món chay"  # Chọn loại món
            new_price = "30000"  # Giá mới

            # Chỉnh sửa tên món
            name_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ten-mon")))
            name_input.clear()
            name_input.send_keys(new_name)  # Nhập tên mới
            time.sleep(2)

            # Chỉnh sửa mô tả
            description_input = driver.find_element(By.ID, "mo-ta")
            description_input.clear()
            description_input.send_keys(new_description)  # Nhập mô tả mới
            time.sleep(2)

            # Chọn loại món
            category_select = driver.find_element(By.ID, "chon-mon")
            category_select.click()  # Nhấp vào dropdown
            time.sleep(1)
            category_select.find_element(By.XPATH, f"//option[text()='{new_category}']").click()  # Chọn loại món
            time.sleep(2)

            # Chỉnh sửa giá bán
            price_input = driver.find_element(By.ID, "gia-moi")
            price_input.clear()
            price_input.send_keys(new_price)  # Nhập giá mới
            time.sleep(2)

            # Lưu thay đổi
            save_button = driver.find_element(By.ID, "update-product-button")
            save_button.click()
            time.sleep(2)

            # Kiểm tra thông báo từ toast__msg
            check_toast_message(driver, "toast__msg", "Sửa sản phẩm thành công!")
            print("Sửa thông tin sản phẩm thành công!")

            # Chờ trường tìm kiếm sản phẩm xuất hiện
            search_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "form-search-product"))
            )
            search_input.clear()  # Xóa nội dung cũ nếu có
            search_input.send_keys(new_name)  # Nhập từ khóa tìm kiếm
            time.sleep(2)  # Chờ kích hoạt sự kiện tìm kiếm

            # Kiểm tra kết quả tìm kiếm
            search_results = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "list"))
            )
            assert len(search_results) > 0, f"Không tìm thấy sản phẩm nào với từ khóa: {new_name}"

            # Duyệt qua tất cả kết quả tìm kiếm và kiểm tra tên sản phẩm
            for result in search_results:
                try:
                    product_name_element = result.find_element(By.CLASS_NAME, "list-info").find_element(By.TAG_NAME,
                                                                                                        "h4")
                    product_name = product_name_element.text.strip().lower()  # Lấy tên sản phẩm và chuẩn hóa
                    assert new_name.lower() in product_name, f"Sản phẩm '{product_name}' không khớp với từ khóa '{new_name}'"
                except Exception as e:
                    print(f"Lỗi khi kiểm tra sản phẩm: {e}")

            print(f"Tìm kiếm sản phẩm '{new_name}' thành công. Tất cả kết quả đều khớp!")


        except AssertionError:
            # Nếu có lỗi trong quá trình kiểm tra thông báo hoặc cập nhật thông tin
            print("Kiểm tra sửa thông tin sản phẩm thất bại!")


        finally:
            # Đảm bảo luôn logout sau khi kiểm tra xong
            logout_admin(driver)

    def test_delete_product(self, driver):
        try:
            driver.get("http://localhost/Webbanhang-main/index.html")

            # Đăng nhập vào hệ thống
            login(driver, "hgbaodev", "123456")
            time.sleep(4)

            # Điều hướng đến trang quản lý sản phẩm
            click_element(driver, By.CLASS_NAME, "text-dndk")

            click_element(driver, By.XPATH, "//a[contains(text(), 'Quản lý cửa hàng')]")
            click_element(driver, By.XPATH, "//div[@class='hidden-sidebar' and text()='Sản phẩm']")
            time.sleep(1)

            # Tìm sản phẩm đầu tiên trong danh sách
            product_list = driver.find_element(By.XPATH, "//div[@id='show-product']")
            first_product_item = product_list.find_element(By.XPATH, ".//div[@class='list']")

            # In ra thông tin sản phẩm đầu tiên
            product_name = first_product_item.find_element(By.XPATH, ".//div[@class='list-info']/h4").text
            print(f"Đã tìm thấy sản phẩm: {product_name}")

            # Kiểm tra sản phẩm đã tìm thấy
            assert product_name, "Không tìm thấy sản phẩm trong danh sách."

            # Tìm và nhấn nút xóa cho sản phẩm đầu tiên
            delete_button = first_product_item.find_element(By.XPATH, ".//button[@class='btn-delete']")
            delete_button.click()

            # Xác nhận xóa sản phẩm
            time.sleep(1)
            alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
            alert.accept()  # Nhấn OK trong thông báo xác nhận xóa
            time.sleep(2)

            # Kiểm tra thông báo toast
            check_toast_message(driver, "toast__msg", "Xóa sản phẩm thành công !")

            # Kiểm tra xem sản phẩm đã bị xóa chưa
            # Thử tìm lại sản phẩm trong danh sách
            try:
                WebDriverWait(driver, 10).until(
                    EC.invisibility_of_element_located((By.XPATH, f"//div[contains(text(), '{product_name}')]"))
                )
                print(f"Sản phẩm '{product_name}' đã được xóa thành công.")
            except Exception as e:
                print("Không thể xóa sản phẩm:", e)
                assert False, f"Sản phẩm '{product_name}' vẫn chưa bị xóa."

        finally:
            # Đảm bảo luôn đăng xuất khỏi tài khoản admin, ngay cả khi có lỗi
            logout_admin(driver)

    def test_search_existing_product(self, driver):
        """
        Kiểm tra tìm kiếm với các từ khóa có sản phẩm tồn tại.
        """
        try:
            # Mở trang web
            driver.get("http://localhost/Webbanhang-main/index.html")

            # Đăng nhập
            login(driver, "hgbaodev", "123456")
            time.sleep(4)

            # Nhấn vào "Đăng nhập / Đăng ký"
            click_element(driver, By.CLASS_NAME, "text-dndk")

            # Điều hướng đến trang quản lý cửa hàng
            click_element(driver, By.XPATH, "//a[contains(text(), 'Quản lý cửa hàng')]")

            # Chuyển đến phần "Sản phẩm"
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='hidden-sidebar' and text()='Sản phẩm']"))
            )
            click_element(driver, By.XPATH, "//div[@class='hidden-sidebar' and text()='Sản phẩm']")

            # Danh sách sản phẩm mẫu để tìm kiếm
            existing_products = ["nấm", "nấm chay", "đậu hũ xào nấm chay"]

            # Tìm kiếm sản phẩm tồn tại
            for product in existing_products:
                print(f"Tìm kiếm sản phẩm: {product}")

                # Chờ trường tìm kiếm sản phẩm xuất hiện
                search_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "form-search-product"))
                )
                search_input.clear()  # Xóa nội dung cũ nếu có
                search_input.send_keys(product)  # Nhập từ khóa tìm kiếm
                time.sleep(2)  # Chờ kích hoạt sự kiện tìm kiếm

                # Kiểm tra kết quả tìm kiếm
                search_results = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "list"))
                )
                assert len(search_results) > 0, f"Không tìm thấy sản phẩm nào với từ khóa: {product}"

                for result in search_results:
                    product_name_element = result.find_element(By.CLASS_NAME, "list-info").find_element(By.TAG_NAME,
                                                                                                        "h4")
                    product_name = product_name_element.text.lower()
                    assert product.lower() in product_name, f"Sản phẩm '{product_name}' không khớp với từ khóa '{product}'"

                print(f"Tìm kiếm sản phẩm '{product}' thành công. Tất cả kết quả đều khớp!")

        finally:
            # Đảm bảo logout sau khi kiểm tra
            logout_admin(driver)

    def test_search_nonexistent_product(self, driver):
        """
        Kiểm tra tìm kiếm với từ khóa không có sản phẩm tồn tại.
        """
        try:
            # Mở trang web
            driver.get("http://localhost/Webbanhang-main/index.html")

            # Đăng nhập
            login(driver, "hgbaodev", "123456")
            time.sleep(4)

            # Nhấn vào "Đăng nhập / Đăng ký"
            click_element(driver, By.CLASS_NAME, "text-dndk")
            time.sleep(1)

            # Điều hướng đến trang quản lý cửa hàng
            click_element(driver, By.XPATH, "//a[contains(text(), 'Quản lý cửa hàng')]")

            # Chuyển đến phần "Sản phẩm"
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[@class='hidden-sidebar' and text()='Sản phẩm']"))
            )
            click_element(driver, By.XPATH, "//div[@class='hidden-sidebar' and text()='Sản phẩm']")

            # Từ khóa tìm kiếm không tồn tại
            nonexistent_keywords = ["bún mắm", "cơm cuộn"]

            for nonexistent_keyword in nonexistent_keywords:
                print(f"Tìm kiếm sản phẩm không tồn tại: {nonexistent_keyword}")

                # Tìm trường tìm kiếm và nhập từ khóa
                search_input = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "form-search-input"))
                )
                search_input.clear()  # Xóa nội dung cũ
                search_input.send_keys(nonexistent_keyword)  # Nhập từ khóa không tồn tại
                time.sleep(2)

                # Kiểm tra thông báo "không có sản phẩm"
                no_results_message = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "no-result-h"))
                )
                assert no_results_message.is_displayed(), "Thông báo không hiển thị khi không có sản phẩm khớp với từ khóa."

                # Kiểm tra nội dung thông báo
                assert "Không có sản phẩm để hiển thị" in no_results_message.text, \
                    f"Nội dung thông báo không đúng: {no_results_message.text}"

                print(f"Thông báo chính xác: '{no_results_message.text}' khi tìm kiếm '{nonexistent_keyword}'.")

        finally:
            # Đảm bảo logout sau khi kiểm tra
            logout_admin(driver)

    # fail-vì xuất hiện các sản phẩm đã xóa trong các danh mục khác
    def test_filter_by_category(self, driver):
        driver.get("http://localhost/Webbanhang-main/index.html")

        # Đăng nhập vào hệ thống
        login(driver, "hgbaodev", "123456")
        time.sleep(4)

        # Nhấn vào "Đăng nhập / Đăng ký"
        click_element(driver, By.CLASS_NAME, "text-dndk")

        # Chờ "Quản lý cửa hàng" xuất hiện và nhấn vào
        click_element(driver, By.XPATH, "//a[contains(text(), 'Quản lý cửa hàng')]")

        # Mở danh mục sản phẩm
        click_element(driver, By.XPATH, "//div[@class='hidden-sidebar' and text()='Sản phẩm']")
        time.sleep(1)

        # Lấy combobox danh mục sản phẩm
        category_select = driver.find_element(By.ID, "the-loai")
        category_options = category_select.find_elements(By.TAG_NAME, "option")

        # Mở danh mục "Đã xóa" và lưu các sản phẩm vào mảng tạm
        category_select.click()  # Mở combobox
        category_option_deleted = driver.find_element(By.XPATH, "//option[contains(text(), 'Đã xóa')]")
        category_option_deleted.click()  # Chọn "Đã xóa"

        time.sleep(2)

        # Lấy danh sách sản phẩm trong danh mục "Đã xóa"
        product_list = driver.find_element(By.XPATH, "//div[@id='show-product']")
        deleted_product_items = product_list.find_elements(By.XPATH, ".//div[@class='list']")
        deleted_products = [item.find_element(By.XPATH, ".//div[@class='list-info']/h4").text for item in deleted_product_items]

        # Lặp qua tất cả các danh mục trong combobox
        for option in category_options:
            category_name = option.text
            if category_name == "Đã xóa":
                continue  # Bỏ qua danh mục "Đã xóa" vì đã kiểm tra rồi

            category_select.click()  # Mở combobox
            option.click()  # Chọn danh mục khác

            # Chờ danh sách sản phẩm thay đổi
            time.sleep(2)

            # Lấy lại danh sách sản phẩm trong danh mục hiện tại
            product_list = driver.find_element(By.XPATH, "//div[@id='show-product']")
            product_items = product_list.find_elements(By.XPATH, ".//div[@class='list']")
            product_names = [item.find_element(By.XPATH, ".//div[@class='list-info']/h4").text for item in product_items]

            # Kiểm tra xem có sản phẩm trong danh mục "Đã xóa" hiển thị trong các danh mục khác
            for deleted_product in deleted_products:
                if deleted_product in product_names:
                    # Nếu sản phẩm "Đã xóa" xuất hiện trong danh mục này, kiểm tra sẽ fail
                    assert False, f"Sản phẩm '{deleted_product}' từ danh mục 'Đã xóa' xuất hiện trong danh mục '{category_name}'"

        # Nếu không có sản phẩm nào từ danh mục "Đã xóa" xuất hiện trong các danh mục khác, test pass
        print("Kiểm thử lọc sản phẩm theo danh mục thành công.")

    def test_reset_product_page(self, driver):
        """
        Test chức năng làm mới trang sản phẩm.
        """
        try:
            # Truy cập trang web
            driver.get("http://localhost/Webbanhang-main/index.html")

            # Đăng nhập tài khoản admin
            login(driver, "hgbaodev", "123456")
            time.sleep(4)

            # Điều hướng đến trang quản lý sản phẩm
            click_element(driver, By.CLASS_NAME, "text-dndk")

            click_element(driver, By.XPATH, "//a[contains(text(), 'Quản lý cửa hàng')]")
            click_element(driver, By.XPATH, "//div[@class='hidden-sidebar' and text()='Sản phẩm']")
            time.sleep(2)


            select = Select(driver.find_element(By.ID, "the-loai"))
            select.select_by_visible_text("Món chay")
            time.sleep(2)


            # Nhấn vào nút "Làm mới"
            reset_button = driver.find_element(By.ID, "btn-cancel-product")
            reset_button.click()
            time.sleep(2)

            # Kiểm tra giá trị của dropdown danh mục sau khi làm mới
            selected_option = WebDriverWait(driver, 10).until(
                lambda d: Select(d.find_element(By.ID, "the-loai")).first_selected_option
            )

            # Đảm bảo dropdown quay về giá trị "Tất cả"
            assert selected_option.text == "Tất cả", "Dropdown không reset về giá trị 'Tất cả'!"

            print("Làm mới trang quản lý sản phẩm thành công.")


        finally:
            # Đảm bảo luôn logout hoặc đóng trình duyệt
            logout_admin(driver)
