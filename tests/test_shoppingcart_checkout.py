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

from Final_term.utils.helper import click_element, fill_input, check_toast_message, check_error_message, login, add_customer, logout, logout_admin, add_to_cart, add_multiple_to_cart, update_product_quantity_in_cart, check_cart_quantity, scroll_to_element


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

    # anh đang sửa
    def test_payment_on_delivery(self, driver):
        try:
            # Mở trang chính và đăng nhập
            driver.get("http://localhost/Webbanhang-main/index.html")
            time.sleep(2)
            login(driver, "hgbaodev", "123456")
            time.sleep(4)

            # # Thêm sản phẩm vào giỏ hàng
            added_product_name, added_product_quantity = add_to_cart(driver)

            # Mở giỏ hàng và tính tổng tiền
            click_element(driver, By.CSS_SELECTOR, "i.fa-light.fa-basket-shopping")
            time.sleep(2)
            cart_items = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".cart-item"))
            )

            calculated_total_price = sum(
                float(item.find_element(By.CSS_SELECTOR, ".cart-item-price").get_attribute("data-price")) *
                int(item.find_element(By.CSS_SELECTOR, ".input-qty").get_attribute("value"))
                for item in cart_items
            )

            # Kiểm tra tổng tiền hiển thị trên giao diện
            total_price_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".cart-total-price .text-price"))
            )
            total_price = float(total_price_element.text.strip().replace(".", "").replace("₫", ""))

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

            # Kiểm tra tiền hàng và phí vận chuyển
            order_total = float(
                driver.find_element(By.CSS_SELECTOR, "#checkout-cart-total").text.strip().replace(".", "").replace("₫",
                                                                                                                   ""))
            shipping_fee = float(
                driver.find_element(By.CSS_SELECTOR, ".chk-ship .price-detail span").text.strip().replace(".",
                                                                                                          "").replace(
                    "₫", ""))
            final_total = float(
                driver.find_element(By.CSS_SELECTOR, "#checkout-cart-price-final").text.strip().replace(".",
                                                                                                        "").replace("₫",
                                                                                                                    ""))

            expected_final_total = order_total + shipping_fee
            assert final_total == expected_final_total, f"Tổng tiền không đúng. Tính: {expected_final_total}, Hiển thị: {final_total}"

            # Hoàn tất thanh toán
            click_element(driver, By.CSS_SELECTOR, ".complete-checkout-btn")

            time.sleep(2)

            # Kiểm tra đơn hàng đã mua
            click_element(driver, By.CLASS_NAME, "text-dndk")
            time.sleep(2)
            click_element(driver, By.XPATH, '//a[@onclick="orderHistory()"]')
            time.sleep(2)

            order_history_elements = driver.find_elements(By.CLASS_NAME, "order-history-group")
            assert order_history_elements, "Không có đơn hàng nào."

            newest_order = order_history_elements[0]
            product_name_from_history = newest_order.find_element(By.CLASS_NAME, "order-history-info").find_element(
                By.TAG_NAME, "h4").text.strip()
            quantity_from_history = newest_order.find_element(By.CLASS_NAME, "order-history-quantity").text.strip()
            price_from_history = newest_order.find_element(By.CLASS_NAME, "order-history-current-price").text.strip()
            order_total_history = newest_order.find_element(By.CLASS_NAME, "order-history-toltal-price").text.strip()

            assert added_product_name == product_name_from_history, f"Sản phẩm không đúng. Tìm thấy: {product_name_from_history}"
            assert added_product_quantity == quantity_from_history, f"Số lượng không đúng. Tìm thấy: {quantity_from_history}"
            assert order_total == float(price_from_history.replace(".", "").replace("₫",
                                                                                    "")), f"Tiền hàng không đúng. Tính: {order_total}, Hiển thị: {price_from_history}"

            print("Thông tin đơn hàng thanh toán và đơn hàng đã mua khớp.")

        except Exception as e:
            print(f"Đã xảy ra lỗi trong quá trình test: {e}")
            raise
        finally:
            logout(driver)
    # anh đang sửa
    def test_payment_on_delivery2(self, driver):
        try:
            # Mở trang chính và đăng nhập
            driver.get("http://localhost/Webbanhang-main/index.html")
            time.sleep(2)
            login(driver, "hgbaodev", "123456")
            time.sleep(4)

            # Thêm sản phẩm vào giỏ hàng
            added_product_name, added_product_quantity = add_to_cart(driver)

            # Mở giỏ hàng và tính tổng tiền
            click_element(driver, By.CSS_SELECTOR, "i.fa-light.fa-basket-shopping")
            time.sleep(2)
            cart_items = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".cart-item"))
            )

            calculated_total_price = sum(
                float(item.find_element(By.CSS_SELECTOR, ".cart-item-price").get_attribute("data-price")) *
                int(item.find_element(By.CSS_SELECTOR, ".input-qty").get_attribute("value"))
                for item in cart_items
            )

            # Kiểm tra tổng tiền hiển thị trên giao diện
            total_price_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".cart-total-price .text-price"))
            )
            total_price = float(total_price_element.text.strip().replace(".", "").replace("₫", ""))

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

            # Kiểm tra tiền hàng và phí vận chuyển
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

            expected_final_total = order_total + shipping_fee
            assert final_total == expected_final_total, f"Tổng tiền không đúng. Tính: {expected_final_total}, Hiển thị: {final_total}"



            # Kiểm tra tiền hàng, phí vận chuyển và tổng tiền trong phần thanh toán
            checkout_section = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".checkout-col-right"))
            )

            # Lấy tiền hàng từ phần thanh toán
            order_total_text = driver.find_element(By.CSS_SELECTOR, "#checkout-cart-total").text.strip()
            order_total = float(order_total_text.replace(".", "").replace("₫", "").strip())

            # So sánh tiền hàng trong phần thanh toán với tổng tiền hàng trong giỏ hàng
            if order_total == calculated_total_price:
                print(f"Tiền hàng trong phần thanh toán đúng với tiền hàng giỏ hàng: {order_total} ₫")
            else:
                print(
                    f"Tiền hàng trong phần thanh toán không đúng. Tiền hàng giỏ hàng: {calculated_total_price} ₫, Tiền hàng thanh toán: {order_total} ₫")

            # Lấy phí vận chuyển
            shipping_fee_text = driver.find_element(By.CSS_SELECTOR, ".chk-ship .price-detail span").text.strip()
            shipping_fee = float(shipping_fee_text.replace(".", "").replace("₫", "").strip())

            # Lấy tổng tiền cuối cùng (bao gồm phí vận chuyển)
            final_total_text = driver.find_element(By.CSS_SELECTOR, "#checkout-cart-price-final").text.strip()
            final_total = float(final_total_text.replace(".", "").replace("₫", "").strip())

            # Tính toán tổng tiền từ tiền hàng và phí vận chuyển
            expected_final_total = order_total + shipping_fee

            # Kiểm tra tổng tiền cuối cùng có đúng không
            if final_total == expected_final_total:
                print(f"Tổng tiền sau khi cộng phí vận chuyển là chính xác: {final_total} ₫")
            else:
                print(
                    f"Tổng tiền sau khi cộng phí vận chuyển không đúng. Tổng tiền tính toán: {expected_final_total} ₫, Tổng tiền hiển thị: {final_total} ₫")






            # Lấy tất cả các sản phẩm trong phần thanh toán
            food_items = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#list-order-checkout .food-total"))
            )
            # In ra thông tin cho mỗi món ăn
            print(f"Thông tin đơn hàng:")
            for food_item in food_items:
                # Lấy tên món ăn
                food_name = food_item.find_element(By.CSS_SELECTOR, ".name-food").text.strip()
                # Lấy số lượng món ăn
                food_quantity = food_item.find_element(By.CSS_SELECTOR, ".count").text.strip()

                # In ra thông tin món ăn
                print(f"Tên món ăn: {food_name}")
                print(f"Số lượng: {food_quantity}")

            # In ra thông tin tiền hàng, phí vận chuyển và tổng tiền
            print(f"Tiền hàng: {order_total} ₫")
            print(f"Phí vận chuyển: {shipping_fee} ₫")
            print(f"Tổng tiền: {final_total} ₫")

            # Hoàn tất thanh toán
            complete_checkout_button = driver.find_element(By.CSS_SELECTOR, ".complete-checkout-btn")
            complete_checkout_button.click()
            time.sleep(2)





            print(f"Thông tin sản phẩm trong đơn hàng mới nhất:")
            # Kiểm tra đơn hàng đã mua
            click_element(driver, By.CLASS_NAME, "text-dndk")
            time.sleep(2)
            click_element(driver, By.XPATH, '//a[@onclick="orderHistory()"]')
            time.sleep(2)

            # Lấy tất cả các đơn hàng trong lịch sử
            order_history_elements = driver.find_elements(By.CLASS_NAME, "order-history-group")
            assert order_history_elements, "Không có đơn hàng nào được tìm thấy."

            # Chọn đơn hàng mới nhất (ở vị trí đầu tiên trong danh sách)
            newest_order = order_history_elements[0]

            # Lấy thông tin sản phẩm trong đơn hàng mới nhất
            order_items = newest_order.find_elements(By.CLASS_NAME,
                                                     "order-history")  # Lấy tất cả các sản phẩm trong đơn hàng




            # Duyệt qua tất cả các sản phẩm trong đơn hàng và in ra thông tin
            for order_item in order_items:
                product_name_from_history = order_item.find_element(By.CLASS_NAME, "order-history-info").find_element(
                    By.TAG_NAME, "h4").text.strip()
                quantity_from_history = order_item.find_element(By.CLASS_NAME, "order-history-quantity").text.strip()
                price_from_history = order_item.find_element(By.CLASS_NAME, "order-history-current-price").text.strip()

                # Loại bỏ dấu chấm than và ký tự không mong muốn trong tên sản phẩm
                product_name_from_history = product_name_from_history.replace("!", "").strip()

                # In ra thông tin sản phẩm
                print(f"Thông tin sản phẩm trong đơn hàng mới nhất:")
                print(f"Tên món ăn: {product_name_from_history}")
                print(f"Số lượng: {quantity_from_history}")
                print(f"Tiền hàng: {price_from_history}")

            # Lấy tổng tiền của đơn hàng mới nhất
            order_total_history = newest_order.find_element(By.CLASS_NAME, "order-history-toltal-price").text.strip()

            # In ra tổng tiền đơn hàng
            print(f"Tổng tiền đơn hàng: {order_total_history}")

            # Kiểm tra thông tin thanh toán với thông tin đơn hàng mới nhất
            for i, food_item in enumerate(food_items):
                # Lấy tên món ăn và số lượng trong phần thanh toán
                food_name = food_item.find_element(By.CSS_SELECTOR, ".name-food").text.strip()
                food_quantity = food_item.find_element(By.CSS_SELECTOR, ".count").text.strip()

                # Lấy tên món ăn và số lượng trong lịch sử đơn hàng
                product_name_from_history = order_items[i].find_element(By.CLASS_NAME,
                                                                        "order-history-info").find_element(By.TAG_NAME,
                                                                                                           "h4").text.strip()
                quantity_from_history = order_items[i].find_element(By.CLASS_NAME,
                                                                    "order-history-quantity").text.strip()
                price_from_history = order_items[i].find_element(By.CLASS_NAME,
                                                                 "order-history-current-price").text.strip()

                # Loại bỏ dấu chấm than và ký tự không mong muốn trong tên sản phẩm
                product_name_from_history = product_name_from_history.replace("!", "").strip()

                # So sánh tên món ăn
                assert food_name == product_name_from_history, f"Sản phẩm không đúng. Tìm thấy: {product_name_from_history}, nhưng sản phẩm thanh toán: {food_name}"

                # So sánh số lượng món ăn
                assert food_quantity == quantity_from_history, f"Số lượng không đúng. Tìm thấy: {quantity_from_history}, nhưng số lượng thanh toán: {food_quantity}"

                # So sánh tiền hàng
                assert order_total == float(price_from_history.replace(".", "").replace("₫",
                                                                                        "").strip()), f"Tiền hàng không đúng. Tìm thấy: {price_from_history}, nhưng tiền hàng thanh toán: {order_total} ₫"

            print("Thông tin đơn hàng thanh toán và đơn hàng đã mua khớp.")

        except Exception as e:
            print(f"Đã xảy ra lỗi trong quá trình test: {e}")
            raise
        finally:
            logout(driver)

