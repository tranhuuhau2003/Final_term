import random
import time

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


def click_element(driver, by, value):
    element = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((by, value))
    )
    ActionChains(driver).move_to_element(element).click().perform()


def fill_input(driver, by, value, input_value):
    field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((by, value))
    )
    field.clear()
    field.send_keys(input_value)


def clear_and_send_keys(driver, by, locator, input_value):

    # Tìm trường input tìm kiếm
    search_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((by, locator))
    )

    search_input.clear()

    search_input.send_keys(input_value)
    time.sleep(3)


def select_dropdown_option(driver, by, locator, option_text):

    try:
        dropdown = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((by, locator))
        )
        dropdown.click()

        if by == By.ID:
            option_locator = (By.XPATH, f"//select[@id='{locator}']/option[text()='{option_text}']")
        elif by == By.NAME:
            option_locator = (By.XPATH, f"//select[@name='{locator}']/option[text()='{option_text}']")
        else:
            raise ValueError("Hiện tại chỉ hỗ trợ định vị bằng ID hoặc NAME")

        option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(option_locator)
        )
        option.click()

    except Exception as e:
        raise Exception(f"Không thể chọn option '{option_text}' trong dropdown: {e}")


def check_toast_message(driver, message_class, expected_text):

    try:
        time.sleep(2)
        toast_message = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, message_class))
        )

        if toast_message.is_displayed() and expected_text in toast_message.text.strip():
            result = True
        else:
            result = False
    except Exception:
        result = False

    time.sleep(2)

    return result


def check_error_message(driver, message_class, expected_text):
    try:
        error_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, message_class))
        )

        assert error_message.is_displayed(), f"Không hiển thị thông báo lỗi với class '{message_class}'."

        assert expected_text in error_message.text, \
            f"Thông báo lỗi không đúng. Mong đợi '{expected_text}', nhưng nhận được: {error_message.text}"

        print(f"Thông báo lỗi hiển thị đúng: {expected_text}")

    except AssertionError as e:
        print(f"Lỗi khi kiểm tra thông báo lỗi: {str(e)}")
        raise

def register_account(driver, fullname, phone, password):

        driver.get("http://localhost/Webbanhang-main/index.html")
        time.sleep(2)
        click_element(driver, By.CLASS_NAME, "text-dndk")
        click_element(driver, By.ID, "signup")

        fill_input(driver, By.ID, "fullname", fullname)
        fill_input(driver, By.ID, "phone", phone)
        fill_input(driver, By.ID, "password", password)
        fill_input(driver, By.ID, "password_confirmation", password)
        time.sleep(2)

        checkbox = driver.find_element(By.ID, "checkbox-signup")
        driver.execute_script("arguments[0].click();", checkbox)
        time.sleep(1)

        click_element(driver, By.ID, "signup-button")
        time.sleep(2)


def login(driver, phone_number, password):
    click_element(driver, By.CLASS_NAME, "text-dndk")

    click_element(driver, By.ID, "login")

    fill_input(driver, By.ID, "phone-login", phone_number)
    fill_input(driver, By.ID, "password-login", password)

    click_element(driver, By.ID, "login-button")


def logout(driver):

    try:
        account_status = driver.find_element(By.CLASS_NAME, "text-tk").text

        if "Tài khoản" in account_status:
            print("Người dùng chưa đăng nhập, không cần đăng xuất.")
            return False

        click_element(driver, By.CLASS_NAME, "text-dndk")
        time.sleep(1)

        click_element(driver, By.ID, "logout")
        time.sleep(2)

        logout_element = WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element((By.CLASS_NAME, "text-tk"), "Tài khoản")
        )
        return logout_element
    except Exception as e:
        print(f"Lỗi khi thực hiện đăng xuất: {e}")
        return False


def logout_admin(driver):

    try:
        try:
            WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "/html/body/div[5]/div/button"))
            )
            close_popup_button = driver.find_element(By.XPATH, "/html/body/div[5]/div/button")
            close_popup_button.click()
            time.sleep(1)
        except Exception:
            pass

        try:
            WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.modal-close"))
            )
            close_popup_button = driver.find_element(By.CSS_SELECTOR, "button.modal-close")
            close_popup_button.click()
            time.sleep(1)
        except Exception:
            pass

        time.sleep(1)
        click_element(driver, By.ID, "logout-acc")
        time.sleep(2)

        WebDriverWait(driver, 10).until(
            lambda d: "index.html" in d.current_url
        )
        return True
    except Exception:
        return False

def add_customer(driver, fullname, phone, password):
    click_element(driver, By.XPATH, "//button[@id='btn-add-user']")

    fill_input(driver, By.ID, "fullname", fullname)
    fill_input(driver, By.ID, "phone", phone)
    fill_input(driver, By.ID, "password", password)

    click_element(driver, By.ID, "signup-button")

def scroll_to_element(driver, element):
    driver.execute_script("arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});", element)
    time.sleep(1)

def add_to_cart(driver):
    try:
        click_element(driver, By.CSS_SELECTOR, "i.fa-light.fa-basket-shopping")
        time.sleep(2)
        existing_products = {}

        empty_cart_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".gio-hang-trong"))
        )

        if empty_cart_message.is_displayed():
            print("Giỏ hàng hiện tại rỗng.")
            click_element(driver, By.CSS_SELECTOR, "i.fa-sharp.fa-solid.fa-xmark")
        else:
            cart_items = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".cart-item"))
            )

            print("Sản phẩm hiện có trong giỏ hàng:")
            for item in cart_items:
                cart_product_name = item.find_element(By.CSS_SELECTOR, ".cart-item-title").text.strip()
                quantity_input = item.find_element(By.CSS_SELECTOR, ".input-qty")
                product_quantity = int(quantity_input.get_attribute("value"))
                existing_products[cart_product_name] = product_quantity
                print(f"- {cart_product_name}: {product_quantity}")

            click_element(driver, By.CSS_SELECTOR, "i.fa-sharp.fa-solid.fa-xmark")

        # Tiến hành thêm món vào giỏ hàng nếu giỏ hàng không rỗng
        # Tìm tất cả các nút "Đặt món" để có thể thêm sản phẩm vào giỏ hàng
        order_buttons = WebDriverWait(driver, 10).until(
            EC.visibility_of_all_elements_located((By.XPATH, "//button[contains(@class, 'order-item')]"))
        )

        selected_button = random.choice(order_buttons)
        scroll_to_element(driver, selected_button)  # Cuộn trang đến vị trí nút "Đặt món"

        selected_button.click()
        time.sleep(1)

        product_name = selected_button.find_element(By.XPATH, "../../..//div[@class='card-title']/a").text.strip()
        print(f"Sản phẩm được chọn để thêm vào giỏ hàng: {product_name}")

        click_element(driver, By.ID, "add-cart")
        time.sleep(1)

        click_element(driver, By.CSS_SELECTOR, "i.fa-light.fa-basket-shopping")
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".cart-container"))
        )

        # Lấy danh sách các sản phẩm trong giỏ hàng để kiểm tra
        cart_items = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".cart-item"))
        )

        product_found = False
        product_quantity = 0

        for item in cart_items:
            cart_product_name = item.find_element(By.CSS_SELECTOR, ".cart-item-title").text.strip()
            if cart_product_name == product_name:
                product_found = True
                quantity_input = item.find_element(By.CSS_SELECTOR, ".input-qty")
                product_quantity = int(quantity_input.get_attribute("value"))
                break  # Nếu đã tìm thấy sản phẩm thì thoát khỏi vòng lặp

        if product_found:
            if product_name in existing_products:
                product_quantity = existing_products[product_name] + 1
            print(f"Sản phẩm '{product_name}' đã được thêm vào giỏ hàng với tổng số lượng: {product_quantity}.")
        else:
            product_quantity = 1
            print(f"Sản phẩm '{product_name}' không có trong giỏ hàng trước đó. Đã thêm mới với số lượng: {product_quantity}.")

        expected_quantity = product_quantity
        for item in cart_items:
            cart_product_name = item.find_element(By.CSS_SELECTOR, ".cart-item-title").text.strip()
            if cart_product_name == product_name:
                quantity_input = item.find_element(By.CSS_SELECTOR, ".input-qty")
                displayed_quantity = int(quantity_input.get_attribute("value"))
                assert expected_quantity == displayed_quantity, \
                    f"Số lượng sản phẩm '{product_name}' trong giỏ hàng không khớp. Mong đợi {expected_quantity}, nhận được {displayed_quantity}."
                print(f"Số lượng sản phẩm '{product_name}' trong giỏ hàng khớp với mong đợi: {displayed_quantity}.")
                break

        click_element(driver, By.CSS_SELECTOR, "i.fa-sharp.fa-solid.fa-xmark")

        return product_name, product_quantity

    except Exception as e:
        print(f"Đã xảy ra lỗi trong hàm add_to_cart: {e}")
        raise

def add_multiple_to_cart(driver):
    try:
        added_products = []

        for _ in range(3):
            order_buttons = WebDriverWait(driver, 10).until(
                EC.visibility_of_all_elements_located((By.XPATH, "//button[contains(@class, 'order-item')]"))
            )
            time.sleep(2)

            selected_button = random.choice(order_buttons)
            selected_button.click()
            time.sleep(2)

            click_element(driver, By.ID, "add-cart")
            time.sleep(2)

            product_name = selected_button.text.strip()
            added_products.append(product_name)

            click_element(driver, By.CSS_SELECTOR, "i.fa-sharp.fa-solid.fa-xmark")
            time.sleep(2)

        return added_products

    except Exception as e:
        print(f"Đã xảy ra lỗi trong hàm add_multiple_to_cart: {e}")
        raise

def update_product_quantity_in_cart(driver, added_products):
    try:
        click_element(driver, By.CSS_SELECTOR, "i.fa-light.fa-basket-shopping")
        time.sleep(2)

        for product_name in added_products:
            product_item = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//div[contains(text(), '{product_name}')]"))
            )

            increase_button = product_item.find_element(By.CSS_SELECTOR, ".plus.is-form")

            quantity_to_add = random.randint(1, 10)
            for _ in range(quantity_to_add):
                increase_button.click()
                time.sleep(1)

        click_element(driver, By.CSS_SELECTOR, "i.fa-sharp.fa-solid.fa-xmark")
        time.sleep(2)
    except Exception as e:
        print(f"Đã xảy ra lỗi trong hàm update_product_quantity_in_cart: {e}")
        raise

def check_cart_quantity(driver, added_products):
    try:
        click_element(driver, By.CSS_SELECTOR, "i.fa-light.fa-basket-shopping")
        time.sleep(2)

        for product_name in added_products:
            product_item = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//div[contains(text(), '{product_name}')]"))
            )

            quantity_span = product_item.find_element(By.CSS_SELECTOR, ".quantity span")
            current_quantity = int(quantity_span.text.strip())

            print(f"Sản phẩm '{product_name}' có số lượng là: {current_quantity}")

        click_element(driver, By.CSS_SELECTOR, "i.fa-sharp.fa-solid.fa-xmark")
        time.sleep(2)

    except Exception as e:
        print(f"Đã xảy ra lỗi trong hàm check_cart_quantity: {e}")
        raise

def check_sorted_products(driver, ascending=True):
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

def navigate_to_product_category(driver, username, password):
    driver.get("http://localhost/Webbanhang-main/index.html")

    login(driver, username, password)
    time.sleep(4)

    click_element(driver, By.CLASS_NAME, "text-dndk")

    click_element(driver, By.XPATH, "//a[contains(text(), 'Quản lý cửa hàng')]")
    time.sleep(1)

    click_element(driver, By.XPATH, "//div[@class='hidden-sidebar' and text()='Sản phẩm']")
    time.sleep(2)

def navigate_to_product_orders(driver, username, password):

    driver.get("http://localhost/Webbanhang-main/index.html")

    login(driver, username, password)
    time.sleep(4)

    click_element(driver, By.CLASS_NAME, "text-dndk")

    click_element(driver, By.XPATH, "//a[contains(text(), 'Quản lý cửa hàng')]")
    time.sleep(1)

    click_element(driver, By.XPATH, "//div[@class='hidden-sidebar' and text()='Đơn hàng']")
    time.sleep(2)

def navigate_to_product_statistics(driver, username, password):

    driver.get("http://localhost/Webbanhang-main/index.html")

    login(driver, username, password)
    time.sleep(4)

    click_element(driver, By.CLASS_NAME, "text-dndk")

    click_element(driver, By.XPATH, "//a[contains(text(), 'Quản lý cửa hàng')]")
    time.sleep(1)

    click_element(driver, By.XPATH, "//div[@class='hidden-sidebar' and text()='Thống kê']")
    time.sleep(2)


# test_dashboard
def go_to_next_page(driver):
    try:
        current_page = int(driver.find_element(By.XPATH, "//li[@class='page-nav-item active']/a").text.strip())
        next_page = driver.find_element(By.XPATH, f"//li[@class='page-nav-item']/a[text()='{current_page + 1}']")
        next_page.click()
        time.sleep(2)
        return True
    except NoSuchElementException:
        return False

def calculate_orders_revenue(driver):
    total_revenue = 0
    orders = driver.find_elements(By.XPATH, "//tbody[@id='showOrder']//tr")
    for order in orders:
        try:
            total_price_text = order.find_element(By.XPATH, ".//td[4]").text.strip()
            total_price_clean = total_price_text.replace("₫", "").replace("\u00a0", "").replace(".", "").strip()
            if total_price_clean.isdigit():
                total_revenue += int(total_price_clean)
        except Exception as e:
            print(f"Lỗi khi xử lý đơn hàng: {e}")
    return total_revenue

def navigate_to_product_dashboard(driver, username, password):

    driver.get("http://localhost/Webbanhang-main/index.html")

    login(driver, username, password)
    time.sleep(4)

    click_element(driver, By.CLASS_NAME, "text-dndk")

    click_element(driver, By.XPATH, "//a[contains(text(), 'Quản lý cửa hàng')]")
    time.sleep(1)

    click_element(driver, By.XPATH, "//div[@class='hidden-sidebar' and text()='Trang tổng quan']")
    time.sleep(2)


def scroll_page(driver):
    scroll_height = driver.execute_script("return document.body.scrollHeight")
    scroll_position = scroll_height * 2 / 3
    driver.execute_script(f"window.scrollTo(0, {scroll_position});")
    time.sleep(2)

def check_products_on_page(driver):
    products_section = driver.find_element(By.ID, "home-products")
    products = products_section.find_elements(By.CLASS_NAME, "card-product")

    assert len(products) > 0, "Không có sản phẩm trên trang hiện tại!"
    print(f"Trang hiện tại có {len(products)} sản phẩm.")

def navigate_to_next_page(driver):
    try:
        pagination = driver.find_element(By.CLASS_NAME, "page-nav-list")
        pages = pagination.find_elements(By.CLASS_NAME, "page-nav-item")
        active_page = pagination.find_element(By.CLASS_NAME, "active")
        current_page_number = int(active_page.find_element(By.TAG_NAME, "a").text)
        next_page_number = current_page_number + 1

        for page in pages:
            try:
                page_number = int(page.find_element(By.TAG_NAME, "a").text)
                if page_number == next_page_number:
                    page.click()
                    time.sleep(2)
                    return True
            except ValueError:
                continue
        return False

    except Exception:
        return False


# test_customer_management
def navigate_to_product_customer(driver, username, password):

    driver.get("http://localhost/Webbanhang-main/index.html")

    login(driver, username, password)
    time.sleep(4)

    click_element(driver, By.CLASS_NAME, "text-dndk")

    click_element(driver, By.XPATH, "//a[contains(text(), 'Quản lý cửa hàng')]")
    time.sleep(1)

    click_element(driver, By.XPATH, "//div[@class='hidden-sidebar' and text()='Khách hàng']")
    time.sleep(2)



# Test_navigation
def scroll_half_page(driver):
    scroll_height = driver.execute_script("return document.body.scrollHeight")
    scroll_position = scroll_height / 2
    driver.execute_script(f"window.scrollTo(0, {scroll_position});")
    time.sleep(2)

def get_menu_links(driver):

    menu_section = driver.find_element(By.XPATH, "//h3[text()='Thực đơn']/following-sibling::ul")
    return menu_section.find_elements(By.TAG_NAME, "a")



# Test_search_and_filter
def filter_products_by_price(driver, min_price, max_price):

    min_price_input = driver.find_element(By.ID, "min-price")
    max_price_input = driver.find_element(By.ID, "max-price")

    min_price_input.clear()
    min_price_input.send_keys(str(min_price))
    max_price_input.clear()
    max_price_input.send_keys(str(max_price))

    price_filter_btn = driver.find_element(By.ID, "advanced-search-price-btn")
    price_filter_btn.click()
    time.sleep(2)

def sort_products(driver, ascending=True):
    sort_button_id = "sort-ascending" if ascending else "sort-descending"
    sort_button = driver.find_element(By.ID, sort_button_id)
    sort_button.click()
    time.sleep(2)

def enter_price(driver, min_price, max_price):
    """Nhập giá vào các trường nhập liệu."""
    min_price_input = driver.find_element(By.ID, "min-price")
    max_price_input = driver.find_element(By.ID, "max-price")
    min_price_input.clear()
    min_price_input.send_keys(str(min_price))
    max_price_input.clear()
    max_price_input.send_keys(str(max_price))

def wait_for_products(driver):
    time.sleep(2)
    return driver.find_element(By.ID, "home-products").find_elements(By.CLASS_NAME, "card-product")

def scroll_to_next_page(driver):
    try:
        pagination = driver.find_element(By.CLASS_NAME, "page-nav-list")
        pages = pagination.find_elements(By.CLASS_NAME, "page-nav-item")
        return pages
    except Exception as e:
        print(f"Lỗi khi tìm phân trang: {str(e)}")
        return []

def navi_to_next_page(driver, products_section):
    try:
        # Lấy danh sách sản phẩm trên trang hiện tại
        products = products_section.find_elements(By.CLASS_NAME, "card-product")
        page_count = 0  # Khởi tạo số trang

        if len(products) > 0:
            page_count += 1  # Tăng số trang nếu có sản phẩm

        pagination = driver.find_element(By.CLASS_NAME, "page-nav-list")
        pages = pagination.find_elements(By.CLASS_NAME, "page-nav-item")

        # Nếu có nhiều hơn một trang, kiểm tra và click vào trang kế tiếp
        active_page = pagination.find_element(By.CLASS_NAME, "active")  # Trang hiện tại
        current_page_number = int(active_page.find_element(By.TAG_NAME, "a").text)  # Số trang hiện tại
        next_page_number = current_page_number + 1  # Trang kế tiếp là trang hiện tại + 1
        next_page = None

        for page in pages:
            page_number = int(page.find_element(By.TAG_NAME, "a").text)
            if page_number == next_page_number:  # Tìm trang có số trang = trang hiện tại + 1
                next_page = page
                break

        if next_page:
            scroll_height = driver.execute_script("return document.body.scrollHeight")
            scroll_position = scroll_height * 2 / 3
            driver.execute_script(f"window.scrollTo(0, {scroll_position});")
            time.sleep(2)

            click_element(driver, By.XPATH, f"//a[text()='{next_page_number}']")
            time.sleep(2)

            driver.execute_script(f"window.scrollTo(0, {scroll_position});")
            time.sleep(2)

            return True

        else:
            return False

    except Exception as e:
        print(f"Lỗi khi chuyển trang: {str(e)}")
        return False


# test shopping cart

def open_cart_and_login(driver, url, username, password):
    driver.get(url)
    time.sleep(2)

    login(driver, username, password)
    time.sleep(4)

    click_element(driver, By.CSS_SELECTOR, "i.fa-light.fa-basket-shopping")
    time.sleep(2)


def get_cart_items(driver):
    return WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".cart-item"))
    )


def increase_quantity(random_item, random_increments):
    for _ in range(random_increments):
        increase_button = random_item.find_element(By.CSS_SELECTOR, ".plus.is-form")
        increase_button.click()
        time.sleep(1)

def decrease_quantity(random_item_to_decrease, random_decrements):
    for _ in range(random_decrements):
        decrease_button = random_item_to_decrease.find_element(By.CSS_SELECTOR, ".minus.is-form")
        decrease_button.click()
        time.sleep(1)
def close_cart(driver):
    click_element(driver, By.CSS_SELECTOR, "i.fa-sharp.fa-solid.fa-xmark")
    time.sleep(2)


def calculate_cart_total(driver):
    cart_items = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".cart-item")))
    total_price = sum(
        float(item.find_element(By.CSS_SELECTOR, ".cart-item-price").get_attribute("data-price")) *
        int(item.find_element(By.CSS_SELECTOR, ".input-qty").get_attribute("value"))
        for item in cart_items
    )
    return total_price

def get_displayed_total_price(driver):
    total_price_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".cart-total-price .text-price")))
    total_price = float(total_price_element.text.strip().replace(".", "").replace("₫", ""))
    return total_price

def proceed_to_checkout(driver):
    driver.find_element(By.CSS_SELECTOR, "button.thanh-toan").click()
    time.sleep(2)
    driver.find_element(By.ID, "giaotannoi").click()  # Select delivery option
    time.sleep(2)
    date_options = WebDriverWait(driver, 10).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div.date-order a.pick-date")))
    random.choice(date_options).click()
    time.sleep(2)

def enter_recipient_details(driver):
    fill_input(driver, By.ID, "tennguoinhan", "Nguyễn Văn A")
    fill_input(driver, By.ID, "sdtnhan", "0901234567")
    fill_input(driver, By.ID, "diachinhan", "Số 123, Đường ABC, Quận XYZ, TP.HCM")
