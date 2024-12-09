# Tui làm đăng nhập,đăng kí ,đăng xuất,giỏ hàng( bao gồm thanh toán),tài khoản của tôi,tìm kiếm món ăn ở trang chủ,chức năng khách hàng của admin  oke ko mn
import random
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


def click_element(driver, by, value):
    """Click vào một phần tử."""
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((by, value))
    )
    ActionChains(driver).move_to_element(element).click().perform()


def fill_input(driver, by, value, input_value):
    """Điền giá trị vào input."""
    field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((by, value))
    )
    field.clear()  # Đảm bảo input trống trước khi nhập
    field.send_keys(input_value)
    # time.sleep(1)


def check_toast_message(driver, message_class, expected_text):
    """
    Kiểm tra thông báo (toast message) xuất hiện và nội dung có khớp hay không.

    Parameters:
        driver: Đối tượng WebDriver của Selenium.
        message_class: Tên class của thông báo cần kiểm tra.
        expected_text: Văn bản mong đợi trong thông báo.

    Raises:
        AssertionError: Nếu thông báo không xuất hiện hoặc nội dung không khớp.
    """
    try:
        # Chờ toast message xuất hiện
        toast_message = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, message_class))
        )

        # Kiểm tra xem toast message có hiển thị không
        assert toast_message.is_displayed(), f"Không hiển thị thông báo. '{expected_text}"

        # Kiểm tra nội dung của thông báo
        actual_text = toast_message.text.strip()
        assert expected_text in actual_text, f"Nội dung thông báo không khớp. Mong đợi: '{expected_text}', Thực tế: '{actual_text}'"

        print(f"Thông báo hiển thị đúng ")
    except Exception as e:
        raise AssertionError(f"Lỗi khi kiểm tra thông báo: {e}")


def check_error_message(driver, message_class, expected_text):
    """Kiểm tra thông báo lỗi."""
    try:
        # Đợi và lấy thông báo lỗi
        error_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, message_class))
        )

        # Kiểm tra thông báo lỗi có hiển thị không
        assert error_message.is_displayed(), f"Không hiển thị thông báo lỗi với class '{message_class}'."

        # Kiểm tra nội dung thông báo lỗi
        assert expected_text in error_message.text, \
            f"Thông báo lỗi không đúng. Mong đợi '{expected_text}', nhưng nhận được: {error_message.text}"

        print(f"Thông báo lỗi hiển thị đúng: {expected_text}")

    except AssertionError as e:
        print(f"Lỗi khi kiểm tra thông báo lỗi: {str(e)}")
        raise  # Ném lỗi lên để thông báo cho người kiểm thử


def login(driver, phone_number, password):
    """
    Hàm đăng nhập vào tài khoản.

    :param driver: Đối tượng WebDriver
    :param phone_number: Số điện thoại đăng nhập
    :param password: Mật khẩu đăng nhập
    """
    # Nhấn vào "Đăng nhập / Đăng ký"
    click_element(driver, By.CLASS_NAME, "text-dndk")

    # Nhấn vào "Đăng nhập"
    click_element(driver, By.ID, "login")

    # Điền số điện thoại và mật khẩu
    fill_input(driver, By.ID, "phone-login", phone_number)
    fill_input(driver, By.ID, "password-login", password)

    # Nhấn nút "Đăng nhập"
    click_element(driver, By.ID, "login-button")


def logout(driver):
    """
    Hàm thực hiện thao tác đăng xuất.

    Args:
        driver (WebDriver): Đối tượng WebDriver của trình duyệt hiện tại.

    Returns:
        bool: True nếu đăng xuất thành công, False nếu không.
    """
    try:
        # Lấy nội dung text của element "text-tk"
        account_status = driver.find_element(By.CLASS_NAME, "text-tk").text

        # Kiểm tra trạng thái: nếu nội dung là "Tài khoản", nghĩa là chưa đăng nhập
        if "Tài khoản" in account_status:
            print("Người dùng chưa đăng nhập, không cần đăng xuất.")
            return False

        # Nhấn vào "Tài khoản"
        click_element(driver, By.CLASS_NAME, "text-dndk")
        time.sleep(1)

        # Nhấn vào "Thoát tài khoản"
        click_element(driver, By.ID, "logout")
        time.sleep(2)

        # Kiểm tra trạng thái sau khi đăng xuất: nội dung "Tài khoản" phải quay lại
        logout_element = WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element((By.CLASS_NAME, "text-tk"), "Tài khoản")
        )
        return logout_element
    except Exception as e:
        print(f"Lỗi khi thực hiện đăng xuất: {e}")
        return False


def logout_admin(driver):
    """
    Hàm thực hiện đăng xuất khỏi trang admin và kiểm tra trạng thái sau khi đăng xuất.
    Nếu có popup che phủ màn hình, nhấn vào nút đóng popup trước khi tiến hành đăng xuất.

    Args:
        driver (WebDriver): WebDriver hiện tại.

    Returns:
        bool: True nếu đăng xuất thành công, False nếu thất bại.
    """
    try:
        # Đóng popup nếu có
        try:
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "/html/body/div[5]/div/button"))
            )
            close_popup_button = driver.find_element(By.XPATH, "/html/body/div[5]/div/button")
            close_popup_button.click()
            time.sleep(1)
        except Exception:
            pass  # Không có popup hoặc không thể đóng

        # Đóng popup che nút đăng xuất nếu có
        try:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.modal-close"))
            )
            close_popup_button = driver.find_element(By.CSS_SELECTOR, "button.modal-close")
            close_popup_button.click()
            time.sleep(1)
        except Exception:
            pass  # Không có popup che nút đăng xuất

        time.sleep(1)
        # Nhấn vào nút "Đăng xuất"
        click_element(driver, By.ID, "logout-acc")
        time.sleep(2)


        # Kiểm tra URL để xác nhận đăng xuất
        WebDriverWait(driver, 10).until(
            lambda d: "index.html" in d.current_url
        )
        return True
    except Exception:
        return False


def add_customer(driver, fullname, phone, password):
    """
    Hàm thêm một khách hàng mới vào danh sách khách hàng.

    :param driver: Đối tượng WebDriver
    :param fullname: Tên khách hàng
    :param phone: Số điện thoại khách hàng
    :param password: Mật khẩu của khách hàng
    """
    # Nhấn vào nút "Thêm khách hàng"
    click_element(driver, By.XPATH, "//button[@id='btn-add-user']")

    # Điền thông tin khách hàng mới
    fill_input(driver, By.ID, "fullname", fullname)
    fill_input(driver, By.ID, "phone", phone)
    fill_input(driver, By.ID, "password", password)

    # Nhấn nút "Đăng ký"
    click_element(driver, By.ID, "signup-button")

def scroll_to_element(driver, element):
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", element)
    time.sleep(1)  # Đợi cuộn xong



def add_to_cart(driver):
    try:
        # Mở giỏ hàng để lấy danh sách sản phẩm hiện có
        click_element(driver, By.CSS_SELECTOR, "i.fa-light.fa-basket-shopping")
        time.sleep(2)  # Chờ giỏ hàng mở

        # Khởi tạo từ điển để lưu tên và số lượng các sản phẩm hiện có trong giỏ hàng
        existing_products = {}

        # Kiểm tra xem giỏ hàng có rỗng không
        empty_cart_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".gio-hang-trong"))
        )

        if empty_cart_message.is_displayed():
            print("Giỏ hàng hiện tại rỗng.")
            # Đóng giỏ hàng nếu giỏ hàng rỗng
            click_element(driver, By.CSS_SELECTOR, "i.fa-sharp.fa-solid.fa-xmark")
            # time.sleep(2)  # Chờ giỏ hàng đóng
        else:
            # Lấy danh sách các sản phẩm trong giỏ hàng
            cart_items = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".cart-item"))
            )

            # Lưu tên và số lượng các sản phẩm hiện có trong giỏ hàng vào từ điển
            print("Sản phẩm hiện có trong giỏ hàng:")
            for item in cart_items:
                cart_product_name = item.find_element(By.CSS_SELECTOR, ".cart-item-title").text.strip()
                quantity_input = item.find_element(By.CSS_SELECTOR, ".input-qty")
                product_quantity = int(quantity_input.get_attribute("value"))
                existing_products[cart_product_name] = product_quantity
                print(f"- {cart_product_name}: {product_quantity}")

            # Đóng giỏ hàng sau khi lấy danh sách sản phẩm
            click_element(driver, By.CSS_SELECTOR, "i.fa-sharp.fa-solid.fa-xmark")
            # time.sleep(2)  # Chờ giỏ hàng đóng

        # Tiến hành thêm món vào giỏ hàng nếu giỏ hàng không rỗng
        # Tìm tất cả các nút "Đặt món" để có thể thêm sản phẩm vào giỏ hàng
        order_buttons = WebDriverWait(driver, 10).until(
            EC.visibility_of_all_elements_located((By.XPATH, "//button[contains(@class, 'order-item')]"))
        )

        # Chọn một nút ngẫu nhiên từ danh sách các nút "Đặt món"
        selected_button = random.choice(order_buttons)
        scroll_to_element(driver, selected_button)  # Cuộn trang đến vị trí nút "Đặt món"

        selected_button.click()  # Nhấn nút "Đặt món"
        time.sleep(1)  # Chờ sau khi nhấn "Đặt món"

        # Lấy tên sản phẩm đã chọn để thêm vào giỏ hàng
        product_name = selected_button.find_element(By.XPATH, "../../..//div[@class='card-title']/a").text.strip()
        print(f"Sản phẩm được chọn để thêm vào giỏ hàng: {product_name}")

        # Nhấn vào nút "Thêm vào giỏ hàng"
        click_element(driver, By.ID, "add-cart")
        time.sleep(1)  # Chờ sau khi nhấn "Thêm vào giỏ hàng"

        # Mở giỏ hàng để kiểm tra sản phẩm vừa thêm
        click_element(driver, By.CSS_SELECTOR, "i.fa-light.fa-basket-shopping")
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".cart-container"))
        )  # Đợi giỏ hàng hiển thị
        # time.sleep(2)  # Chờ giỏ hàng mở

        # Lấy danh sách các sản phẩm trong giỏ hàng để kiểm tra
        cart_items = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".cart-item"))
        )

        product_found = False  # Biến đánh dấu xem sản phẩm có được tìm thấy trong giỏ hàng
        product_quantity = 0  # Biến lưu số lượng của sản phẩm tìm thấy

        # Kiểm tra xem sản phẩm vừa thêm có có mặt trong giỏ hàng không
        for item in cart_items:
            cart_product_name = item.find_element(By.CSS_SELECTOR, ".cart-item-title").text.strip()
            if cart_product_name == product_name:
                product_found = True
                quantity_input = item.find_element(By.CSS_SELECTOR, ".input-qty")
                product_quantity = int(quantity_input.get_attribute("value"))
                break  # Nếu đã tìm thấy sản phẩm thì thoát khỏi vòng lặp

        # Kiểm tra lại số lượng sản phẩm nếu sản phẩm đã có sẵn trong giỏ hàng trước đó
        if product_found:
            if product_name in existing_products:
                # Sản phẩm đã có trong giỏ hàng, cộng số lượng hiện tại với số lượng mới thêm vào
                product_quantity = existing_products[product_name] + 1
            print(f"Sản phẩm '{product_name}' đã được thêm vào giỏ hàng với tổng số lượng: {product_quantity}.")
        else:
            # Nếu sản phẩm không có trong giỏ hàng trước đó, số lượng mong muốn sẽ là 1 (số lượng vừa thêm vào)
            product_quantity = 1
            print(f"Sản phẩm '{product_name}' không có trong giỏ hàng trước đó. Đã thêm mới với số lượng: {product_quantity}.")

        # Kiểm tra số lượng hiển thị trong giỏ hàng
        expected_quantity = product_quantity
        for item in cart_items:
            cart_product_name = item.find_element(By.CSS_SELECTOR, ".cart-item-title").text.strip()
            if cart_product_name == product_name:
                quantity_input = item.find_element(By.CSS_SELECTOR, ".input-qty")
                displayed_quantity = int(quantity_input.get_attribute("value"))
                # Kiểm tra số lượng hiển thị trong giỏ hàng với số lượng mong đợi
                assert expected_quantity == displayed_quantity, \
                    f"Số lượng sản phẩm '{product_name}' trong giỏ hàng không khớp. Mong đợi {expected_quantity}, nhận được {displayed_quantity}."
                print(f"Số lượng sản phẩm '{product_name}' trong giỏ hàng khớp với mong đợi: {displayed_quantity}.")
                break

        # Đóng giỏ hàng
        click_element(driver, By.CSS_SELECTOR, "i.fa-sharp.fa-solid.fa-xmark")
        # time.sleep(2)  # Chờ giỏ hàng đóng

        # Trả về kết quả: tên sản phẩm và số lượng đã thêm vào giỏ hàng
        return product_name, product_quantity

    except Exception as e:
        # Nếu có lỗi, in ra thông báo lỗi và ném lỗi lên
        print(f"Đã xảy ra lỗi trong hàm add_to_cart: {e}")
        raise  # Ném lại lỗi để có thể xử lý ngoài hàm này


def add_multiple_to_cart(driver):
    try:
        # Danh sách các sản phẩm đã thêm vào giỏ hàng
        added_products = []

        # Lặp lại 3 lần để thêm 3 sản phẩm ngẫu nhiên
        for _ in range(3):
            # Tìm tất cả các nút "Đặt món"
            order_buttons = WebDriverWait(driver, 10).until(
                EC.visibility_of_all_elements_located((By.XPATH, "//button[contains(@class, 'order-item')]"))
            )
            time.sleep(2)  # Chờ các nút hiển thị

            # Chọn một nút ngẫu nhiên từ danh sách nút "Đặt món" và nhấn
            selected_button = random.choice(order_buttons)
            selected_button.click()
            time.sleep(2)  # Chờ sau khi nhấn "Đặt món"

            # Nhấn vào nút "Thêm vào giỏ hàng"
            click_element(driver, By.ID, "add-cart")
            time.sleep(2)  # Chờ sau khi thêm vào giỏ hàng

            # Lưu thông tin sản phẩm đã thêm vào giỏ hàng
            product_name = selected_button.text.strip()
            added_products.append(product_name)

            # Đóng giỏ hàng
            click_element(driver, By.CSS_SELECTOR, "i.fa-sharp.fa-solid.fa-xmark")
            time.sleep(2)  # Chờ giỏ hàng đóng

        return added_products

    except Exception as e:
        print(f"Đã xảy ra lỗi trong hàm add_multiple_to_cart: {e}")
        raise

def update_product_quantity_in_cart(driver, added_products):
    try:
        # Mở giỏ hàng
        click_element(driver, By.CSS_SELECTOR, "i.fa-light.fa-basket-shopping")
        time.sleep(2)  # Chờ giỏ hàng mở

        # Lặp qua từng sản phẩm đã thêm và tăng số lượng ngẫu nhiên từ 1 đến 10
        for product_name in added_products:
            # Tìm sản phẩm trong giỏ hàng theo tên (hoặc bạn có thể dùng các thông tin khác như ID)
            product_item = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//div[contains(text(), '{product_name}')]"))
            )

            # Lấy nút tăng số lượng của sản phẩm
            increase_button = product_item.find_element(By.CSS_SELECTOR, ".plus.is-form")

            # Tăng số lượng sản phẩm ngẫu nhiên từ 1 đến 10
            quantity_to_add = random.randint(1, 10)
            for _ in range(quantity_to_add):
                increase_button.click()
                time.sleep(1)  # Chờ mỗi lần tăng số lượng

        # Đóng giỏ hàng
        click_element(driver, By.CSS_SELECTOR, "i.fa-sharp.fa-solid.fa-xmark")
        time.sleep(2)  # Chờ giỏ hàng đóng

    except Exception as e:
        print(f"Đã xảy ra lỗi trong hàm update_product_quantity_in_cart: {e}")
        raise

def check_cart_quantity(driver, added_products):
    try:
        # Mở giỏ hàng
        click_element(driver, By.CSS_SELECTOR, "i.fa-light.fa-basket-shopping")
        time.sleep(2)  # Chờ giỏ hàng mở

        # Lặp qua từng sản phẩm đã thêm và kiểm tra số lượng
        for product_name in added_products:
            # Tìm sản phẩm trong giỏ hàng theo tên
            product_item = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//div[contains(text(), '{product_name}')]"))
            )

            # Lấy số lượng sản phẩm từ giỏ hàng
            quantity_span = product_item.find_element(By.CSS_SELECTOR, ".quantity span")
            current_quantity = int(quantity_span.text.strip())

            print(f"Sản phẩm '{product_name}' có số lượng là: {current_quantity}")
            # Bạn có thể thêm kiểm tra assert ở đây nếu cần thiết
            # assert current_quantity == expected_quantity, f"Số lượng sản phẩm {product_name} không đúng!"

        # Đóng giỏ hàng
        click_element(driver, By.CSS_SELECTOR, "i.fa-sharp.fa-solid.fa-xmark")
        time.sleep(2)  # Chờ giỏ hàng đóng

    except Exception as e:
        print(f"Đã xảy ra lỗi trong hàm check_cart_quantity: {e}")
        raise



def check_filtered_products(driver, min_price, max_price):
    """Kiểm tra sản phẩm sau khi lọc theo giá."""
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

        # Kiểm tra xem giá sản phẩm có nằm trong khoảng lọc không
        assert min_price <= product_price <= max_price, \
            f"Giá sản phẩm '{product.text}' ({product_price}₫) không nằm trong khoảng {min_price}₫ đến {max_price}₫."

def check_sorted_products(driver, ascending=True):
    """Kiểm tra sản phẩm sau khi sắp xếp theo giá."""
    prev_price = 0 if ascending else float('inf')
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

        # Kiểm tra nếu sắp xếp theo giá tăng dần
        if ascending:
            assert product_price >= prev_price, \
                f"Giá sản phẩm '{product.text}' ({product_price}₫) không theo thứ tự từ thấp đến cao."
        else:
            assert product_price <= prev_price, \
                f"Giá sản phẩm '{product.text}' ({product_price}₫) không theo thứ tự từ cao đến thấp."

        # Cập nhật giá sản phẩm hiện tại
        prev_price = product_price
