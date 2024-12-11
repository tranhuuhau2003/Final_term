import random
import re
import time

from selenium.common import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import pytest
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from Final_term.utils.driver_helper import init_driver, close_driver  # Import từ driver_helper
from Final_term.utils.helper import click_element, fill_input, check_toast_message, check_error_message, login, add_customer, logout, logout_admin, add_to_cart, add_multiple_to_cart, update_product_quantity_in_cart, check_cart_quantity, scroll_to_element



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
            # Mở trang chính
            driver.get("http://localhost/Webbanhang-main/index.html")
            time.sleep(2)  # Chờ trang tải đầy đủ

            # Đăng nhập
            login(driver, "hgbaodev", "123456")
            time.sleep(4)  # Chờ đăng nhập hoàn tất


            # Thêm sản phẩm vào giỏ hàng và lấy tên sản phẩm và số lượng đã thêm
            added_product_name, added_product_quantity = add_to_cart(driver)

            # Kiểm tra không cần thiết nữa vì add_to_cart đã kiểm tra trước đó
            print(f"Sản phẩm '{added_product_name}' đã được thêm vào giỏ hàng với số lượng {added_product_quantity}.")

        except Exception as e:
            print(f"Lỗi khi kiểm thử thêm sản phẩm: {e}")
        finally:
            # Đảm bảo đăng xuất sau khi kiểm thử
            logout(driver)

    def test_increase_quantity(self, driver):
        try:
            # Mở trang chính
            driver.get("http://localhost/Webbanhang-main/index.html")
            time.sleep(2)  # Chờ trang tải đầy đủ

            # Đăng nhập
            login(driver, "hgbaodev", "123456")
            time.sleep(4)  # Chờ đăng nhập hoàn tất

            # Mở giỏ hàng
            click_element(driver, By.CSS_SELECTOR, "i.fa-light.fa-basket-shopping")
            time.sleep(2)  # Chờ giỏ hàng mở

            # Lấy danh sách các sản phẩm trong giỏ hàng
            cart_items = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".cart-item"))
            )

            if not cart_items:
                print("Giỏ hàng không có sản phẩm.")
                return

            # Chọn một sản phẩm ngẫu nhiên từ giỏ hàng để tăng số lượng
            random_item = random.choice(cart_items)
            cart_product_name = random_item.find_element(By.CSS_SELECTOR, ".cart-item-title").text.strip()

            # Cuộn đến sản phẩm để đảm bảo nó nằm trong tầm nhìn trước khi thực hiện thao tác
            scroll_to_element(driver, random_item)
            time.sleep(3)  # Chờ một chút để cuộn hoàn tất

            # Lấy số lượng sản phẩm trước khi tăng
            quantity_input = random_item.find_element(By.CSS_SELECTOR, ".input-qty")
            initial_quantity = int(quantity_input.get_attribute("value"))

            # In ra tên và số lượng sản phẩm trước khi tăng
            print(f"Sản phẩm '{cart_product_name}' có số lượng ban đầu: {initial_quantity}")

            # Random số lần nhấn nút tăng số lượng
            random_increments = random.randint(1, 10)
            print(f"Tăng {random_increments} lần cho '{cart_product_name}'.")

            # Nhấn nút tăng số lượng
            for _ in range(random_increments):
                increase_button = random_item.find_element(By.CSS_SELECTOR, ".plus.is-form")
                increase_button.click()
                time.sleep(1)  # Chờ cập nhật giao diện

            # Lấy số lượng sản phẩm sau khi tăng
            updated_quantity = int(quantity_input.get_attribute("value"))

            # Kiểm tra kết quả tăng
            expected_quantity = initial_quantity + random_increments
            assert updated_quantity == expected_quantity, \
                f"Số lượng không đúng sau khi tăng, mong đợi: {expected_quantity}, nhận được: {updated_quantity}"
            print(f"Sản phẩm '{cart_product_name}' tăng thành công lên: {updated_quantity}")

            # Đóng giỏ hàng
            click_element(driver, By.CSS_SELECTOR, "i.fa-sharp.fa-solid.fa-xmark")
            time.sleep(2)  # Chờ giỏ hàng đóng

        except Exception as e:
            print(f"Đã xảy ra lỗi trong quá trình test: {e}")
            raise

        finally:
            # Đảm bảo luôn logout sau khi kiểm tra xong
            logout(driver)

    def test_decrease_quantity(self, driver):
        try:
            # Mở trang chính
            driver.get("http://localhost/Webbanhang-main/index.html")
            time.sleep(2)  # Chờ trang tải đầy đủ

            # Đăng nhập
            login(driver, "hgbaodev", "123456")
            time.sleep(4)  # Chờ đăng nhập hoàn tất

            # Mở giỏ hàng
            click_element(driver, By.CSS_SELECTOR, "i.fa-light.fa-basket-shopping")
            time.sleep(2)  # Chờ giỏ hàng mở

            # Lấy danh sách các sản phẩm trong giỏ hàng
            cart_items = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".cart-item"))
            )

            if not cart_items:
                print("Giỏ hàng không có sản phẩm.")
                return

            # Chọn một sản phẩm ngẫu nhiên khác để giảm số lượng
            random_item_to_decrease = random.choice(cart_items)
            cart_product_name_to_decrease = random_item_to_decrease.find_element(By.CSS_SELECTOR, ".cart-item-title").text.strip()

            # Cuộn đến sản phẩm giảm số lượng để đảm bảo nó nằm trong tầm nhìn
            scroll_to_element(driver, random_item_to_decrease)
            time.sleep(3)  # Chờ một chút để cuộn hoàn tất

            # Lấy số lượng sản phẩm trước khi giảm
            quantity_input_to_decrease = random_item_to_decrease.find_element(By.CSS_SELECTOR, ".input-qty")
            initial_quantity_to_decrease = int(quantity_input_to_decrease.get_attribute("value"))

            # In ra tên và số lượng sản phẩm trước khi giảm
            print(f"Sản phẩm '{cart_product_name_to_decrease}' có số lượng ban đầu: {initial_quantity_to_decrease}")

            # Random số lần nhấn nút giảm số lượng từ 1 đến 5
            random_decrements = random.randint(1, 5)
            print(f"Giảm {random_decrements} lần cho '{cart_product_name_to_decrease}'.")

            # Tính số lượng mong đợi sau khi giảm
            expected_quantity_after_decrease = initial_quantity_to_decrease - random_decrements

            # Kiểm tra nếu số lượng mong đợi nhỏ hơn 1, đặt lại thành 1
            if expected_quantity_after_decrease < 1:
                expected_quantity_after_decrease = 1

            # Giảm số lượng sản phẩm bằng số lần random
            for _ in range(random_decrements):
                decrease_button = random_item_to_decrease.find_element(By.CSS_SELECTOR, ".minus.is-form")
                decrease_button.click()
                time.sleep(1)  # Chờ cập nhật giao diện

            # Lấy số lượng sản phẩm sau khi giảm
            updated_quantity_after_decrease = int(quantity_input_to_decrease.get_attribute("value"))

            # Kiểm tra kết quả
            assert updated_quantity_after_decrease == expected_quantity_after_decrease, \
                f"Số lượng không đúng sau khi giảm, mong đợi: {expected_quantity_after_decrease}, nhận được: {updated_quantity_after_decrease}"
            print(f"Sản phẩm '{cart_product_name_to_decrease}' giảm thành công xuống: {updated_quantity_after_decrease}")

            # Đóng giỏ hàng
            click_element(driver, By.CSS_SELECTOR, "i.fa-sharp.fa-solid.fa-xmark")
            time.sleep(2)  # Chờ giỏ hàng đóng

        except Exception as e:
            print(f"Đã xảy ra lỗi trong quá trình test: {e}")
            raise

        finally:
            # Đảm bảo luôn logout sau khi kiểm tra xong
            logout(driver)

    def test_delete_product(self, driver):
        try:
            # Mở trang chính
            driver.get("http://localhost/Webbanhang-main/index.html")
            time.sleep(2)  # Chờ trang tải đầy đủ

            # Đăng nhập
            login(driver, "hgbaodev", "123456")
            time.sleep(4)  # Chờ đăng nhập hoàn tất

            # Thêm sản phẩm vào giỏ hàng
            product_name, product_quantity = add_to_cart(driver)

            # Mở giỏ hàng
            click_element(driver, By.CSS_SELECTOR, "i.fa-light.fa-basket-shopping")
            time.sleep(2)  # Chờ giỏ hàng mở

            # Lấy tất cả các sản phẩm trong giỏ hàng
            cart_items = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".cart-item"))
            )

            # Tìm sản phẩm đã thêm vào giỏ hàng và nhấn vào nút xoá
            for item in cart_items:
                cart_product_name = item.find_element(By.CSS_SELECTOR, ".cart-item-title").text.strip()
                if cart_product_name == product_name:
                    # Đợi nút xóa (cart-item-delete) xuất hiện và nhấn vào nó
                    delete_button = WebDriverWait(item, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, ".cart-item-delete"))
                    )
                    delete_button.click()
                    time.sleep(2)  # Chờ sau khi nhấn nút xoá

                    # Kiểm tra xem sản phẩm đã bị xoá khỏi giỏ hàng chưa
                    cart_items_after_delete = WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".cart-item"))
                    )

                    # Assert rằng sản phẩm đã bị xoá khỏi giỏ hàng
                    assert not any(item for item in cart_items_after_delete if product_name in item.text), \
                        f"Sản phẩm '{product_name}' vẫn còn trong giỏ hàng sau khi xoá."

                    print(f"Sản phẩm '{product_name}' đã được xoá thành công khỏi giỏ hàng.")
                    break
            else:
                print(f"Sản phẩm '{product_name}' không có trong giỏ hàng để xoá.")

            # Đóng giỏ hàng
            click_element(driver, By.CSS_SELECTOR, "i.fa-sharp.fa-solid.fa-xmark")
            time.sleep(2)  # Chờ giỏ hàng đóng

        finally:
            # Đảm bảo đăng xuất dù có xảy ra lỗi hay không
            logout(driver)

    def test_payment_on_delivery(self, driver):
        try:
            # Mở trang chính và đăng nhập
            driver.get("http://localhost/Webbanhang-main/index.html")
            time.sleep(2)

            login(driver, "hgbaodev", "123456")
            time.sleep(4)

            # Thêm sản phẩm vào giỏ hàng
            products_in_cart = []
            for _ in range(1):  # Giả sử thêm 1 sản phẩm
                product_name, product_quantity = add_to_cart(driver)
                products_in_cart.append({"name": product_name, "quantity": product_quantity})

            print("Sản phẩm trong giỏ hàng:", products_in_cart)

            # Mở giỏ hàng và kiểm tra tổng tiền
            click_element(driver, By.CSS_SELECTOR, "i.fa-light.fa-basket-shopping")
            time.sleep(2)
            cart_items = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".cart-item"))
            )

            # Tính tổng tiền giỏ hàng
            calculated_total_price = sum(
                float(item.find_element(By.CSS_SELECTOR, ".cart-item-price").get_attribute("data-price")) *
                int(item.find_element(By.CSS_SELECTOR, ".input-qty").get_attribute("value"))
                for item in cart_items
            )

            # In ra tổng tiền giỏ hàng tính toán
            print(f"Tổng tiền giỏ hàng tính toán: {calculated_total_price}₫")

            # Kiểm tra tổng tiền hiển thị trên giao diện
            total_price_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".cart-total-price .text-price"))
            )
            total_price = float(total_price_element.text.strip().replace(".", "").replace("₫", ""))

            # In ra tổng tiền hiển thị
            print(f"Tổng tiền giỏ hàng hiển thị: {total_price}₫")

            assert calculated_total_price == total_price, f"Tổng tiền sai. Tính: {calculated_total_price}, Hiển thị: {total_price}"

            # Tiến hành thanh toán
            click_element(driver, By.CSS_SELECTOR, "button.thanh-toan")
            time.sleep(2)
            click_element(driver, By.ID, "giaotannoi")
            time.sleep(2)

            # Chọn ngày giao hàng
            date_options = WebDriverWait(driver, 10).until(
                EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div.date-order a.pick-date"))
            )
            random.choice(date_options).click()
            time.sleep(2)

            # Điền thông tin người nhận
            fill_input(driver, By.ID, "tennguoinhan", "Nguyễn Văn A")
            fill_input(driver, By.ID, "sdtnhan", "0901234567")
            fill_input(driver, By.ID, "diachinhan", "Số 123, Đường ABC, Quận XYZ, TP.HCM")

            time.sleep(2)

            # Kiểm tra tổng tiền thanh toán
            order_total = float(
                driver.find_element(By.CSS_SELECTOR, "#checkout-cart-total").text.strip().replace(".", "").replace("₫",
                                                                                                                   "")
            )
            shipping_fee = float(
                driver.find_element(By.CSS_SELECTOR, ".chk-ship .price-detail span").text.strip().replace(".",
                                                                                                          "").replace(
                    "₫", "")
            )
            final_total = float(
                driver.find_element(By.CSS_SELECTOR, "#checkout-cart-price-final").text.strip().replace(".",
                                                                                                        "").replace("₫",
                                                                                                                    "")
            )

            # In ra các tổng tiền
            print(f"Tổng tiền hàng: {order_total}₫")
            print(f"Phí vận chuyển: {shipping_fee}₫")
            print(f"Tổng tiền cuối cùng: {final_total}₫")

            expected_final_total = order_total + shipping_fee
            assert final_total == expected_final_total, f"Tổng tiền không đúng. Tính: {expected_final_total}, Hiển thị: {final_total}"

            # Hoàn tất thanh toán
            click_element(driver, By.CSS_SELECTOR, ".complete-checkout-btn")
            time.sleep(2)

            # Kiểm tra lịch sử đơn hàng
            click_element(driver, By.CLASS_NAME, "text-dndk")
            time.sleep(2)
            click_element(driver, By.XPATH, '//a[@onclick="orderHistory()"]')
            time.sleep(2)

            order_history_elements = driver.find_elements(By.CLASS_NAME, "order-history-group")
            assert order_history_elements, "Không có đơn hàng nào."

            # Lấy đơn hàng mới nhất
            latest_order = order_history_elements[0]
            product_name_from_history = latest_order.find_element(By.CLASS_NAME, "order-history-info").find_element(
                By.TAG_NAME, "h4").text.strip()
            quantity_from_history = latest_order.find_element(By.CLASS_NAME, "order-history-quantity").text.strip()

            print(f"Đơn hàng mới nhất: {product_name_from_history} x {quantity_from_history}")

            # Kiểm tra sản phẩm trong lịch sử đơn hàng với giỏ hàng
            product_found = False
            for product in products_in_cart:
                # Bỏ qua dấu chấm than và chữ 'x' trong tên và số lượng
                product_name_from_history_cleaned = product_name_from_history.rstrip('!')
                quantity_from_history_cleaned = quantity_from_history.lstrip('x')

                if product["name"] == product_name_from_history_cleaned and str(
                        product["quantity"]) == quantity_from_history_cleaned:
                    product_found = True
                    break  # Nếu tìm thấy, thoát khỏi vòng lặp

            if not product_found:
                print(f"Sản phẩm không khớp:")
                print(f"- Tên sản phẩm trong giỏ hàng: {products_in_cart[0]['name']}")
                print(f"- Tên sản phẩm trong lịch sử đơn hàng: {product_name_from_history}")
                print(f"- Số lượng trong giỏ hàng: {products_in_cart[0]['quantity']}")
                print(f"- Số lượng trong lịch sử đơn hàng: {quantity_from_history}")

            # Kiểm tra nếu không tìm thấy sản phẩm trong lịch sử đơn hàng
            assert product_found, f"Sản phẩm {products_in_cart[0]['name']} không khớp trong lịch sử đơn hàng."

            print("Thông tin sản phẩm khớp với lịch sử đơn hàng.")

        except Exception as e:
            print(f"Đã xảy ra lỗi trong quá trình test: {e}")
            raise  # Ném lỗi lên để framework test ghi nhận

        finally:
            logout(driver)  # Đăng xuất sau khi kết thúc kiểm thử

    def test_pay_until_pick_up(self, driver):
        driver.get("http://localhost/Webbanhang-main/index.html")

        # Đăng nhập vào hệ thống
        login(driver, "hgbaodev", "123456")
        print("Đăng nhập thành công.")
        time.sleep(4)

        # Thêm sản phẩm vào giỏ hàng
        product_name, product_quantity = add_to_cart(driver)
        print(f"Sản phẩm {product_name} đã được thêm vào giỏ hàng.")

        basket_icon = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "i.fa-light.fa-basket-shopping"))  # Chọn biểu tượng giỏ hàng
        )
        basket_icon.click()
        print("Nhấn vào giỏ hàng.")
        time.sleep(2)

        # Lấy danh sách các sản phẩm trong giỏ hàng
        cart_items = driver.find_elements(By.CSS_SELECTOR, ".cart-list .cart-item")

        # Tính tổng tiền dựa trên giá và số lượng
        calculated_total_price = 0
        print("Đang tính tổng tiền...")

        for item in cart_items:
            # Lấy giá sản phẩm (giá ở dạng string có dấu phân cách)
            price_element = item.find_element(By.CSS_SELECTOR, ".cart-item-price")
            price = price_element.get_attribute("data-price")
            price = float(price.strip())  # Chuyển đổi giá thành số, bỏ dấu phân cách nếu có

            # Lấy số lượng sản phẩm
            quantity_element = item.find_element(By.CSS_SELECTOR, ".input-qty")
            quantity = int(quantity_element.get_attribute("value"))

            # Tính tổng tiền cho sản phẩm này
            calculated_total_price += price * quantity

        # Lấy tổng tiền hiển thị trên giao diện
        total_price_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".cart-total-price .text-price"))
        )
        total_price = total_price_element.text.strip()
        total_price = float(total_price.replace(".", "").replace("₫", "").strip())  # Chuyển đổi giá trị thành số

        # Kiểm tra xem tổng tiền tính toán có trùng với tổng tiền hiển thị trên giao diện không
        if calculated_total_price == total_price:
            print(f"Tổng tiền tính đúng: {calculated_total_price} ₫")
        else:
            print(
                f"Tổng tiền không đúng. Tổng tiền tính toán: {calculated_total_price} ₫, Tổng tiền hiển thị: {total_price} ₫")

        # Nhấn nút "Thanh toán"
        checkout_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.thanh-toan"))
        )
        checkout_button.click()
        print("Nhấn vào nút thanh toán.")
        time.sleep(2)

        # Chờ đến khi nút "Tự đến lấy" có thể được nhấn
        pickup_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "tudenlay"))
        )
        pickup_button.click()
        print("Nhấn vào nút tự đến lấy.")
        time.sleep(2)

        # Chọn ngày giao hàng
        date_options = WebDriverWait(driver, 10).until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "div.date-order a.pick-date"))
        )
        random_date = random.choice(date_options)
        random_date.click()
        print("Chọn ngày giao hàng.")
        time.sleep(3)


        print("Cuộn đến phần thông tin người nhận.")


        # Chờ đến khi phần tử radio button có id là "chinhanh-1" hoặc "chinhanh-2" xuất hiện
        radio_buttons = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input[type='radio'][name='chinhanh']"))
        )

        # Chọn ngẫu nhiên một radio button
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

        # Kiểm tra tiền hàng trong phần thanh toán
        checkout_section = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".checkout-col-right"))
        )
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

        print(
            f"Thông tin đơn hàng: Tên món ăn: {food_name}, Số lượng: {food_quantity}, Tiền hàng: {order_total} ₫, Tổng tiền: {final_total} ₫")

        # Hoàn tất thanh toán
        complete_checkout_button = driver.find_element(By.CSS_SELECTOR, ".complete-checkout-btn")
        complete_checkout_button.click()
        print("Hoàn tất thanh toán.")
        time.sleep(2)

        # Kiểm tra đơn hàng đã mua
        click_element(driver, By.CLASS_NAME, "text-dndk")

        click_element(driver, By.XPATH, '//a[@onclick="orderHistory()"]')
        print("Xem thông tin đơn hàng đã mua.")
        time.sleep(2)

        order_history_elements = driver.find_elements(By.CLASS_NAME, "order-history-group")
        assert order_history_elements, "Không có đơn hàng nào được tìm thấy."

        newest_order = order_history_elements[0]
        product_name_from_history = newest_order.find_element(By.CLASS_NAME, "order-history-info").find_element(
            By.TAG_NAME, "h4").text.strip()
        quantity_from_history = newest_order.find_element(By.CLASS_NAME, "order-history-quantity").text.strip()
        price_from_history = newest_order.find_element(By.CLASS_NAME, "order-history-current-price").text.strip()
        order_total_history = newest_order.find_element(By.CLASS_NAME, "order-history-toltal-price").text.strip()

        product_name_from_history = product_name_from_history.replace("!", "").strip()
        quantity_from_history = re.sub(r'^(x)(\d+)', r'\2x', quantity_from_history)
        quantity_from_history = re.sub(r'(\d+)(x)$', r'\1x', quantity_from_history)

        print(
            f"Thông tin đơn hàng mới nhất: Tên món ăn: {product_name_from_history}, Số lượng: {quantity_from_history}, Tiền hàng: {price_from_history}, Tổng tiền: {order_total_history}")

        # So sánh thông tin đơn hàng
        assert food_name == product_name_from_history, f"Sản phẩm không đúng. Tìm thấy: {product_name_from_history}, nhưng sản phẩm thanh toán: {food_name}"
        assert food_quantity == quantity_from_history, f"Số lượng không đúng. Tìm thấy: {quantity_from_history}, nhưng số lượng thanh toán: {food_quantity}"
        assert order_total == float(price_from_history.replace(".", "").replace("₫",
                                                                                "").strip()), f"Tiền hàng không đúng. Tìm thấy: {price_from_history}, nhưng tiền hàng thanh toán: {order_total} ₫"

        print("Thông tin đơn hàng thanh toán và đơn hàng đã mua khớp.")

