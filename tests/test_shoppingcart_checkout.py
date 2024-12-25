import random
import re
import time

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from Final_term.utils.driver_helper import init_driver, close_driver  # Import từ driver_helper
from Final_term.utils.helper import *


@pytest.fixture
def driver():
    """
    Khởi tạo WebDriver và đóng WebDriver sau khi test xong.
    """
    driver = init_driver()  # Gọi hàm khởi tạo driver từ file driver_helper
    yield driver  # Cung cấp driver cho test
    close_driver(driver)  # Đóng driver sau khi test xong



class TestShoppingcartCheckout:

    def test_add_product(self, driver):
        try:
            open_cart_and_login(driver, "http://localhost/Webbanhang-main/index.html", "hgbaodev", "123456")

            added_product_name, added_product_quantity = add_to_cart(driver)
            print(f"Sản phẩm '{added_product_name}' đã được thêm vào giỏ hàng với số lượng {added_product_quantity}.")

        except Exception as e:
            print(f"Lỗi khi kiểm thử thêm sản phẩm: {e}")
        finally:
            logout(driver)

    def test_increase_quantity(self, driver):
        try:
            open_cart_and_login(driver, "http://localhost/Webbanhang-main/index.html", "hgbaodev", "123456")

            cart_items = get_cart_items(driver)
            if not cart_items:
                print("Giỏ hàng không có sản phẩm.")
                return

            random_item = random.choice(cart_items)
            cart_product_name = random_item.find_element(By.CSS_SELECTOR, ".cart-item-title").text.strip()

            scroll_to_element(driver, random_item)
            time.sleep(3)

            quantity_input = random_item.find_element(By.CSS_SELECTOR, ".input-qty")
            initial_quantity = int(quantity_input.get_attribute("value"))
            print(f"Sản phẩm '{cart_product_name}' có số lượng ban đầu: {initial_quantity}")

            random_increments = random.randint(1, 10)
            print(f"Tăng {random_increments} lần cho '{cart_product_name}'.")

            increase_quantity(random_item, random_increments)

            updated_quantity = int(quantity_input.get_attribute("value"))
            expected_quantity = initial_quantity + random_increments
            assert updated_quantity == expected_quantity, \
                f"Số lượng không đúng sau khi tăng, mong đợi: {expected_quantity}, nhận được: {updated_quantity}"
            print(f"Sản phẩm '{cart_product_name}' tăng thành công lên: {updated_quantity}")

            close_cart(driver)

        except Exception as e:
            print(f"Đã xảy ra lỗi trong quá trình test: {e}")
            raise

        finally:
            logout(driver)

    def test_decrease_quantity(self, driver):
        try:
            open_cart_and_login(driver, "http://localhost/Webbanhang-main/index.html", "hgbaodev", "123456")

            cart_items = get_cart_items(driver)
            if not cart_items:
                print("Giỏ hàng không có sản phẩm.")
                return

            random_item_to_decrease = random.choice(cart_items)
            cart_product_name_to_decrease = random_item_to_decrease.find_element(By.CSS_SELECTOR,
                                                                                 ".cart-item-title").text.strip()

            scroll_to_element(driver, random_item_to_decrease)
            time.sleep(3)

            quantity_input_to_decrease = random_item_to_decrease.find_element(By.CSS_SELECTOR, ".input-qty")
            initial_quantity_to_decrease = int(quantity_input_to_decrease.get_attribute("value"))
            print(f"Sản phẩm '{cart_product_name_to_decrease}' có số lượng ban đầu: {initial_quantity_to_decrease}")

            random_decrements = random.randint(1, 5)
            print(f"Giảm {random_decrements} lần cho '{cart_product_name_to_decrease}'.")

            expected_quantity_after_decrease = initial_quantity_to_decrease - random_decrements
            if expected_quantity_after_decrease < 1:
                expected_quantity_after_decrease = 1

            decrease_quantity(random_item_to_decrease, random_decrements)

            updated_quantity_after_decrease = int(quantity_input_to_decrease.get_attribute("value"))

            assert updated_quantity_after_decrease == expected_quantity_after_decrease, \
                f"Số lượng không đúng sau khi giảm, mong đợi: {expected_quantity_after_decrease}, nhận được: {updated_quantity_after_decrease}"
            print(
                f"Sản phẩm '{cart_product_name_to_decrease}' giảm thành công xuống: {updated_quantity_after_decrease}")

            close_cart(driver)

        except Exception as e:
            print(f"Đã xảy ra lỗi trong quá trình test: {e}")
            raise

        finally:
            logout(driver)

    def test_delete_product(self, driver):
        try:
            driver.get("http://localhost/Webbanhang-main/index.html")
            time.sleep(2)

            login(driver, "hgbaodev", "123456")
            time.sleep(4)

            product_name, product_quantity = add_to_cart(driver)

            click_element(driver, By.CSS_SELECTOR, "i.fa-light.fa-basket-shopping")
            time.sleep(2)

            cart_items = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".cart-item"))
            )

            for item in cart_items:
                cart_product_name = item.find_element(By.CSS_SELECTOR, ".cart-item-title").text.strip()
                if cart_product_name == product_name:
                    delete_button = WebDriverWait(item, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, ".cart-item-delete"))
                    )
                    delete_button.click()
                    time.sleep(2)

                    cart_items_after_delete = WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".cart-item"))
                    )

                    assert not any(item for item in cart_items_after_delete if product_name in item.text), \
                        f"Sản phẩm '{product_name}' vẫn còn trong giỏ hàng sau khi xoá."

                    print(f"Sản phẩm '{product_name}' đã được xoá thành công khỏi giỏ hàng.")
                    break
            else:
                print(f"Sản phẩm '{product_name}' không có trong giỏ hàng để xoá.")

            click_element(driver, By.CSS_SELECTOR, "i.fa-sharp.fa-solid.fa-xmark")
            time.sleep(2)

        finally:
            logout(driver)


    def test_payment_on_delivery(self, driver):
        try:
            driver.get("http://localhost/Webbanhang-main/index.html")
            time.sleep(2)
            login(driver, "hgbaodev", "123456")
            time.sleep(4)

            products_in_cart = []
            for _ in range(1):
                product_name, product_quantity = add_to_cart(driver)
                products_in_cart.append({"name": product_name, "quantity": product_quantity})

            print("Sản phẩm trong giỏ hàng:", products_in_cart)

            click_element(driver, By.CSS_SELECTOR, "i.fa-light.fa-basket-shopping")
            time.sleep(2)
            cart_items = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".cart-item")))

            calculated_total_price = sum(
                float(item.find_element(By.CSS_SELECTOR, ".cart-item-price").get_attribute("data-price")) *
                int(item.find_element(By.CSS_SELECTOR, ".input-qty").get_attribute("value"))
                for item in cart_items
            )

            print(f"Tổng tiền giỏ hàng tính toán: {calculated_total_price}₫")

            total_price_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".cart-total-price .text-price")))
            total_price = float(total_price_element.text.strip().replace(".", "").replace("₫", ""))

            print(f"Tổng tiền giỏ hàng hiển thị: {total_price}₫")
            assert calculated_total_price == total_price, f"Tổng tiền sai. Tính: {calculated_total_price}, Hiển thị: {total_price}"

            click_element(driver, By.CSS_SELECTOR, "button.thanh-toan")
            time.sleep(2)
            click_element(driver, By.ID, "giaotannoi")
            time.sleep(2)

            date_options = WebDriverWait(driver, 10).until(
                EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div.date-order a.pick-date")))
            random.choice(date_options).click()
            time.sleep(2)

            fill_input(driver, By.ID, "tennguoinhan", "Nguyễn Văn A")
            fill_input(driver, By.ID, "sdtnhan", "0901234567")
            fill_input(driver, By.ID, "diachinhan", "Số 123, Đường ABC, Quận XYZ, TP.HCM")
            time.sleep(2)

            order_total = float(driver.find_element(By.CSS_SELECTOR, "#checkout-cart-total").text.strip().replace(".", "").replace("₫",""))
            shipping_fee = float(driver.find_element(By.CSS_SELECTOR, ".chk-ship .price-detail span").text.strip().replace(".","").replace("₫", ""))
            final_total = float(driver.find_element(By.CSS_SELECTOR, "#checkout-cart-price-final").text.strip().replace(".", "").replace("₫",""))

            print(f"Tổng tiền hàng: {order_total}₫")
            print(f"Phí vận chuyển: {shipping_fee}₫")
            print(f"Tổng tiền cuối cùng: {final_total}₫")

            expected_final_total = order_total + shipping_fee
            assert final_total == expected_final_total, f"Tổng tiền không đúng. Tính: {expected_final_total}, Hiển thị: {final_total}"

            click_element(driver, By.CSS_SELECTOR, ".complete-checkout-btn")
            time.sleep(2)

            click_element(driver, By.CLASS_NAME, "text-dndk")
            time.sleep(2)
            click_element(driver, By.XPATH, '//a[@onclick="orderHistory()"]')
            time.sleep(2)

            order_history_elements = driver.find_elements(By.CLASS_NAME, "order-history-group")
            assert order_history_elements, "Không có đơn hàng nào."

            latest_order = order_history_elements[0]
            product_name_from_history = latest_order.find_element(By.CLASS_NAME, "order-history-info").find_element(By.TAG_NAME, "h4").text.strip()
            quantity_from_history = latest_order.find_element(By.CLASS_NAME, "order-history-quantity").text.strip()

            product_found = False

            for product in products_in_cart:
                product_name_from_history_cleaned = product_name_from_history.rstrip('!')
                quantity_from_history_cleaned = quantity_from_history.lstrip('x')

                if product["name"] == product_name_from_history_cleaned and str(
                        product["quantity"]) == quantity_from_history_cleaned:
                    product_found = True
                    break
            assert product_found, f"Sản phẩm {products_in_cart[0]['name']} không khớp trong lịch sử đơn hàng."
            print("Thông tin sản phẩm khớp với lịch sử đơn hàng.")

        except Exception as e:
            print(f"Đã xảy ra lỗi trong quá trình test: {e}")
            raise

        finally:
            logout(driver)


    def test_pay_until_pick_up(self, driver):
        driver.get("http://localhost/Webbanhang-main/index.html")
        login(driver, "hgbaodev", "123456")
        print("Đăng nhập thành công.")
        time.sleep(4)

        product_name, product_quantity = add_to_cart(driver)
        print(f"Sản phẩm {product_name} đã được thêm vào giỏ hàng.")

        basket_icon = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "i.fa-light.fa-basket-shopping"))  # Chọn biểu tượng giỏ hàng
        )
        basket_icon.click()
        print("Nhấn vào giỏ hàng.")
        time.sleep(2)

        cart_items = driver.find_elements(By.CSS_SELECTOR, ".cart-list .cart-item")

        calculated_total_price = 0
        print("Đang tính tổng tiền...")

        for item in cart_items:
            price_element = item.find_element(By.CSS_SELECTOR, ".cart-item-price")
            price = price_element.get_attribute("data-price")
            price = float(price.strip())

            quantity_element = item.find_element(By.CSS_SELECTOR, ".input-qty")
            quantity = int(quantity_element.get_attribute("value"))

            calculated_total_price += price * quantity

        total_price_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".cart-total-price .text-price")))
        total_price = total_price_element.text.strip()
        total_price = float(total_price.replace(".", "").replace("₫", "").strip())  # Chuyển đổi giá trị thành số

        if calculated_total_price == total_price:
            print(f"Tổng tiền tính đúng: {calculated_total_price} ₫")
        else:
            print(
                f"Tổng tiền không đúng. Tổng tiền tính toán: {calculated_total_price} ₫, Tổng tiền hiển thị: {total_price} ₫")

        checkout_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.thanh-toan"))
        )
        checkout_button.click()
        print("Nhấn vào nút thanh toán.")
        time.sleep(2)

        pickup_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "tudenlay"))
        )
        pickup_button.click()
        print("Nhấn vào nút tự đến lấy.")
        time.sleep(2)

        date_options = WebDriverWait(driver, 10).until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div.date-order a.pick-date"))
        )
        random_date = random.choice(date_options)
        random_date.click()
        print("Chọn ngày giao hàng.")
        time.sleep(3)

        print("Cuộn đến phần thông tin người nhận.")

        radio_buttons = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input[type='radio'][name='chinhanh']"))
        )

        selected_radio_button = random.choice(radio_buttons)

        driver.execute_script("arguments[0].click();", selected_radio_button)
        print("Đã nhấn vào radio button bằng JavaScript.")

        print("Chọn chi nhánh.")
        time.sleep(2)

        name_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "tennguoinhan"))
        )
        name_input.send_keys("Nguyễn Văn A")
        print("Điền tên người nhận.")

        phone_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "sdtnhan"))
        )
        phone_input.send_keys("0901234567")
        print("Điền số điện thoại.")
        time.sleep(2)

        checkout_section = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".checkout-col-right")))
        order_total_element = driver.find_element(By.CSS_SELECTOR, "#checkout-cart-total")
        order_total = order_total_element.text.strip()
        order_total = float(order_total.replace(".", "").replace("₫", "").strip())

        if order_total == calculated_total_price:
            print(f"Tiền hàng trong phần thanh toán đúng với tiền hàng giỏ hàng: {order_total} ₫")
        else:
            print(
                f"Tiền hàng trong phần thanh toán không đúng. Tiền hàng giỏ hàng: {calculated_total_price} ₫, Tiền hàng thanh toán: {order_total} ₫")

        # Kiểm tra tổng tiền cuối cùng
        final_total_element = driver.find_element(By.CSS_SELECTOR, "#checkout-cart-price-final")
        final_total = final_total_element.text.strip()
        final_total = float(final_total.replace(".", "").replace("₫", "").strip())

        if final_total == order_total:
            print(f"Tổng tiền trong thanh toán đúng với tiền hàng: {final_total} ₫")
        else:
            print(
                f"Tổng tiền trong thanh toán không đúng. Tiền hàng: {order_total} ₫, Tổng tiền hiển thị: {final_total} ₫")

        # Lấy tên món ăn và số lượng từ thanh toán
        food_name_element = driver.find_element(By.CSS_SELECTOR, ".food-total .name-food")
        food_name = food_name_element.text.strip()
        food_quantity_element = driver.find_element(By.CSS_SELECTOR, ".food-total .count")
        food_quantity = food_quantity_element.text.strip()

        print(f"Thông tin đơn hàng: Tên món ăn: {food_name}, Số lượng: {food_quantity}, Tiền hàng: {order_total} ₫, Tổng tiền: {final_total} ₫")

        complete_checkout_button = driver.find_element(By.CSS_SELECTOR, ".complete-checkout-btn")
        complete_checkout_button.click()
        print("Hoàn tất thanh toán.")
        time.sleep(2)

        click_element(driver, By.CLASS_NAME, "text-dndk")

        click_element(driver, By.XPATH, '//a[@onclick="orderHistory()"]')
        print("Xem thông tin đơn hàng đã mua.")
        time.sleep(2)

        order_history_elements = driver.find_elements(By.CLASS_NAME, "order-history-group")
        assert order_history_elements, "Không có đơn hàng nào được tìm thấy."

        newest_order = order_history_elements[0]
        product_name_from_history = newest_order.find_element(By.CLASS_NAME, "order-history-info").find_element(By.TAG_NAME, "h4").text.strip()
        quantity_from_history = newest_order.find_element(By.CLASS_NAME, "order-history-quantity").text.strip()
        price_from_history = newest_order.find_element(By.CLASS_NAME, "order-history-current-price").text.strip()
        order_total_history = newest_order.find_element(By.CLASS_NAME, "order-history-toltal-price").text.strip()

        product_name_from_history = product_name_from_history.replace("!", "").strip()
        quantity_from_history = re.sub(r'^(x)(\d+)', r'\2x', quantity_from_history)
        quantity_from_history = re.sub(r'(\d+)(x)$', r'\1x', quantity_from_history)

        print(f"Thông tin đơn hàng mới nhất: Tên món ăn: {product_name_from_history}, Số lượng: {quantity_from_history}, Tiền hàng: {price_from_history}, Tổng tiền: {order_total_history}")

        assert food_name == product_name_from_history, f"Sản phẩm không đúng. Tìm thấy: {product_name_from_history}, nhưng sản phẩm thanh toán: {food_name}"
        assert food_quantity == quantity_from_history, f"Số lượng không đúng. Tìm thấy: {quantity_from_history}, nhưng số lượng thanh toán: {food_quantity}"
        assert order_total == float(price_from_history.replace(".", "").replace("₫",
                                                                                "").strip()), f"Tiền hàng không đúng. Tìm thấy: {price_from_history}, nhưng tiền hàng thanh toán: {order_total} ₫"
        print("Thông tin đơn hàng thanh toán và đơn hàng đã mua khớp.")

