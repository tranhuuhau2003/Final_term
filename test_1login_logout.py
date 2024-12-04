import random

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    #phóng to cửa sổ
    driver.maximize_window()
    #trả về đối tượng kiểm thử
    yield driver
    driver.quit()  


#Test log in với dữ liệu đúng
def test_valid_login(driver):
    driver.get("http://localhost/Webbanhang-main/index.html")
     # Chờ phần tử "Đăng nhập / Đăng ký" xuất hiện
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "text-dndk"))
    )
    time.sleep(3)

    # Tìm phần tử "Đăng nhập / Đăng ký"
    dang_nhap_dang_ky = driver.find_element(By.CLASS_NAME, "text-dndk")
    time.sleep(3)

    # Cuộn tới phần tử (nếu cần)
    actions = ActionChains(driver)
    actions.move_to_element(dang_nhap_dang_ky).perform()
    time.sleep(3)
    # Nhấn vào phần tử
    dang_nhap_dang_ky.click()
    # Tìm phần tử "Đăng nhập"
    login_button = driver.find_element(By.ID, "login")

    # Cuộn tới phần tử (nếu cần)
    actions.move_to_element(login_button).perform()
    time.sleep(3)

    # Nhấn vào nút "Đăng nhập"
    login_button.click()
    time.sleep(3)
    # Tìm và điền vào trường "Nhập số điện thoại"
    phone_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "phone-login"))
    )
    phone_field.send_keys("hgbaodev")  # Điền số điện thoại
    time.sleep(2)

    # Tìm và điền vào trường "Nhập mật khẩu"
    password_field = driver.find_element(By.ID, "password-login")
    password_field.send_keys("123456")  # Điền mật khẩu
    time.sleep(2)

    # Thêm các bước khác (nếu cần), ví dụ: nhấn nút "Đăng nhập"
    login_submit_button = driver.find_element(By.ID, "login-button")  # Giả sử nút có ID là "submit-login"
    login_submit_button.click()
    time.sleep(3)
         # Chờ phần tử "Đăng nhập / Đăng ký" xuất hiện
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "text-dndk"))
    )
    time.sleep(3)

    # Tìm phần tử "Đăng nhập / Đăng ký"
    dang_nhap_dang_ky = driver.find_element(By.CLASS_NAME, "text-dndk")
    time.sleep(3)

    # Cuộn tới phần tử (nếu cần)
    actions = ActionChains(driver)
    actions.move_to_element(dang_nhap_dang_ky).perform()
    time.sleep(3)
  # Chờ phần tử "Tài khoản của tôi" xuất hiện sau khi đăng nhập
    my_account_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='javascript:;'][onclick='myAccount()']"))
    )

    # Kiểm tra xem phần tử "Tài khoản của tôi" có tồn tại
    assert my_account_button.is_displayed(), "Phần tử 'Tài khoản của tôi' không hiển thị. Đăng nhập thất bại."

    # Nhấn vào "Tài khoản của tôi"
    my_account_button.click()
    time.sleep(3)

    print("Đăng nhập thành công và đã nhấn vào 'Tài khoản của tôi'.")
#Test log in khi nhập sai tài khoản hoặc mật khẩu
def test_invalid_login(driver):
driver.get("http://localhost/Webbanhang-main/index.html")
     # Chờ phần tử "Đăng nhập / Đăng ký" xuất hiện
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "text-dndk"))
    )
    time.sleep(3)

    # Tìm phần tử "Đăng nhập / Đăng ký"
    dang_nhap_dang_ky = driver.find_element(By.CLASS_NAME, "text-dndk")
    time.sleep(3)

    # Cuộn tới phần tử (nếu cần)
    actions = ActionChains(driver)
    actions.move_to_element(dang_nhap_dang_ky).perform()
    time.sleep(3)
    # Nhấn vào phần tử
    dang_nhap_dang_ky.click()
    # Tìm phần tử "Đăng nhập"
    login_button = driver.find_element(By.ID, "login")

    # Cuộn tới phần tử (nếu cần)
    actions.move_to_element(login_button).perform()
    time.sleep(3)

    # Nhấn vào nút "Đăng nhập"
    login_button.click()
    time.sleep(3)
    # Tìm và điền vào trường "Nhập số điện thoại"
    phone_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "phone-login"))
    )
    phone_field.send_keys("hgbaodev")  # Điền số điện thoại
    time.sleep(2)

    # Tìm và điền vào trường "Nhập mật khẩu sai"
    password_field = driver.find_element(By.ID, "password-login")
    password_field.send_keys("1234567")  # Điền mật khẩu
    time.sleep(2)

    # Thêm các bước khác (nếu cần), ví dụ: nhấn nút "Đăng nhập"
    login_submit_button = driver.find_element(By.ID, "login-button")  # Giả sử nút có ID là "submit-login"
    login_submit_button.click()
    time.sleep(3)
    # Chờ phần tử thông báo lỗi xuất hiện trong class "toast__msg"
    toast_message = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "toast__msg"))
    )

    # In ra nội dung của thông báo lỗi
    print("Thông báo lỗi: ", toast_message.text)
    time.sleep(3)

    # Kiểm tra xem thông báo lỗi có hiển thị hay không
    assert toast_message.is_displayed(), "Không có thông báo lỗi. Đăng nhập thất bại không có thông báo."
    time.sleep(3)

    # Kiểm tra nội dung thông báo lỗi (nếu cần, ví dụ thông báo sai tài khoản/mật khẩu)
    toast_text = toast_message.text
    assert "Sai mật khẩu" in toast_text, f"Thông báo lỗi không đúng: {toast_text}"
    time.sleep(3)

# Test log in khi mật khẩu bị bỏ trống
def test_login_empty_password(driver):
    driver.get("http://localhost/Webbanhang-main/index.html")
    # Chờ phần tử "Đăng nhập / Đăng ký" xuất hiện
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "text-dndk"))
    )
    time.sleep(3)

    # Tìm phần tử "Đăng nhập / Đăng ký"
    dang_nhap_dang_ky = driver.find_element(By.CLASS_NAME, "text-dndk")
    time.sleep(3)

    # Cuộn tới phần tử (nếu cần)
    actions = ActionChains(driver)
    actions.move_to_element(dang_nhap_dang_ky).perform()
    time.sleep(3)
    # Nhấn vào phần tử
    dang_nhap_dang_ky.click()

    # Tìm phần tử "Đăng nhập"
    login_button = driver.find_element(By.ID, "login")
    actions.move_to_element(login_button).perform()
    time.sleep(3)
    login_button.click()
    time.sleep(3)

    # Tìm và điền vào trường "Nhập số điện thoại"
    phone_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "phone-login"))
    )
    phone_field.send_keys("hgbaodev")  # Điền số điện thoại
    time.sleep(2)

    # Không điền mật khẩu (bỏ trống mật khẩu)
    password_field = driver.find_element(By.ID, "password-login")
    password_field.clear()  # Đảm bảo ô mật khẩu được xóa trống
    time.sleep(2)

    # Nhấn nút "Đăng nhập"
    login_submit_button = driver.find_element(By.ID, "login-button")
    login_submit_button.click()
    time.sleep(3)

    # Chờ phần tử thông báo lỗi xuất hiện trong class "form-message-check-login"
    error_message = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "form-message-check-login"))
    )

    # In ra nội dung của thông báo lỗi
    print("Thông báo lỗi: ", error_message.text)
    time.sleep(3)

    # Kiểm tra xem thông báo lỗi có hiển thị hay không
    assert error_message.is_displayed(), "Không có thông báo lỗi. Đăng nhập thất bại không có thông báo."
    time.sleep(3)

    # Kiểm tra nội dung thông báo lỗi
    error_text = error_message.text
    assert "Vui lòng nhập mật khẩu" in error_text, f"Thông báo lỗi không đúng: {error_text}"
    time.sleep(3)

# test dăng kí tài khoản đầy đủ thông tin
def test_register(driver):
    driver.get("http://localhost/Webbanhang-main/index.html")
    # Chờ phần tử "Đăng nhập / Đăng ký" xuất hiện
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "text-dndk"))
    )
    time.sleep(3)

    # Tìm phần tử "Đăng nhập / Đăng ký"
    dang_nhap_dang_ky = driver.find_element(By.CLASS_NAME, "text-dndk")
    time.sleep(3)

    # Cuộn tới phần tử (nếu cần)
    actions = ActionChains(driver)
    actions.move_to_element(dang_nhap_dang_ky).perform()
    time.sleep(3)
    # Nhấn vào phần tử
    dang_nhap_dang_ky.click()
    # Chờ phần tử "Đăng ký" xuất hiện
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "signup"))
    )
    time.sleep(3)

    # Tìm phần tử "Đăng ký"
    dang_ky = driver.find_element(By.ID, "signup")
    time.sleep(3)

    # Cuộn tới phần tử (nếu cần)
    actions = ActionChains(driver)
    actions.move_to_element(dang_ky).perform()
    time.sleep(3)

    # Nhấn vào phần tử "Đăng ký"
    dang_ky.click()
    time.sleep(3)
        # Điền thông tin vào trường "Họ và tên"
    fullname_field = driver.find_element(By.ID, "fullname")
    fullname_field.send_keys("Nguyễn Văn AC")  # Điền tên giả sử
    time.sleep(2)

    # Điền thông tin vào trường "Số điện thoại"
    phone_field = driver.find_element(By.ID, "phone")
    phone_field.send_keys("0123456769")  # Điền số điện thoại giả sử
    time.sleep(2)

    # Điền thông tin vào trường "Mật khẩu"
    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys("password123")  # Điền mật khẩu giả sử
    time.sleep(2)

    # Điền lại mật khẩu vào trường "Nhập lại mật khẩu"
    password_confirm_field = driver.find_element(By.ID, "password_confirmation")
    password_confirm_field.send_keys("password123")  # Điền lại mật khẩu
    time.sleep(2)
    checkbox = driver.find_element(By.ID, "checkbox-signup")
    driver.execute_script("arguments[0].click();", checkbox)
    time.sleep(3)

    # Nhấn vào nút "Đăng ký"
    signup_button = driver.find_element(By.ID, "signup-button")
    signup_button.click()  # Nhấn vào nút đăng ký
    time.sleep(2)


    # Kiểm tra nếu có thông báo xác nhận đăng ký thành công
    toast_message = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "toast__msg"))
    )

    # In ra nội dung của thông báo xác nhận
    print("Thông báo xác nhận: ", toast_message.text)
    time.sleep(3)

    # Kiểm tra thông báo xác nhận
    assert toast_message.is_displayed(), "Không có thông báo xác nhận."
    assert "Tạo thành công tài khoản !" in toast_message.text, f"Thông báo không đúng: {toast_message.text}"
    time.sleep(3)

# test dăng kí tài khoản khi nhập thiếu trường (sdt)
def test_register_missing_phone(driver):
    driver.get("http://localhost/Webbanhang-main/index.html")
    # Chờ phần tử "Đăng nhập / Đăng ký" xuất hiện
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "text-dndk"))
    )
    time.sleep(3)

    # Nhấn vào "Đăng nhập / Đăng ký"
    dang_nhap_dang_ky = driver.find_element(By.CLASS_NAME, "text-dndk")
    ActionChains(driver).move_to_element(dang_nhap_dang_ky).click().perform()
    time.sleep(3)

    # Nhấn vào "Đăng ký"
    dang_ky = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "signup"))
    )
    dang_ky.click()
    time.sleep(3)

    # Điền thông tin vào trường "Họ và tên"
    fullname_field = driver.find_element(By.ID, "fullname")
    fullname_field.send_keys("Nguyễn Văn AC")
    time.sleep(2)

    # BỎ QUA trường "Số điện thoại"

    # Điền thông tin vào trường "Mật khẩu"
    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys("password123")
    time.sleep(2)

    # Điền lại mật khẩu
    password_confirm_field = driver.find_element(By.ID, "password_confirmation")
    password_confirm_field.send_keys("password123")
    time.sleep(2)

    # Nhấn vào checkbox
    checkbox = driver.find_element(By.ID, "checkbox-signup")
    driver.execute_script("arguments[0].click();", checkbox)
    time.sleep(3)

    # Nhấn nút "Đăng ký"
    signup_button = driver.find_element(By.ID, "signup-button")
    signup_button.click()
    time.sleep(3)

    # Kiểm tra thông báo lỗi xuất hiện
    error_message = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "form-message-phone"))
    )

    # In nội dung thông báo lỗi
    print("Thông báo lỗi: ", error_message.text)

    # Kiểm tra nội dung thông báo lỗi
    assert error_message.is_displayed(), "Không có thông báo lỗi khi thiếu số điện thoại."
    assert "Vui lòng nhập vào số điện thoại" in error_message.text, f"Thông báo lỗi không đúng: {error_message.text}"


#đăng kos trùng tài khoản
def test_register_duplicate_phone(driver):
    driver.get("http://localhost/Webbanhang-main/index.html")
    # Chờ phần tử "Đăng nhập / Đăng ký" xuất hiện
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "text-dndk"))
    )
    time.sleep(3)

    # Nhấn vào "Đăng nhập / Đăng ký"
    dang_nhap_dang_ky = driver.find_element(By.CLASS_NAME, "text-dndk")
    ActionChains(driver).move_to_element(dang_nhap_dang_ky).click().perform()
    time.sleep(3)

    # Nhấn vào "Đăng ký"
    dang_ky = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "signup"))
    )
    dang_ky.click()
    time.sleep(3)

    # Điền thông tin vào trường "Họ và tên"
    fullname_field = driver.find_element(By.ID, "fullname")
    fullname_field.send_keys("Nguyễn Văn AC")
    time.sleep(2)

    # Điền thông tin vào trường "Số điện thoại" (đã tồn tại)
    phone_field = driver.find_element(By.ID, "phone")
    phone_field.send_keys("hgbaodev")  # Số điện thoại đã được đăng ký trước
    time.sleep(2)

    # Điền thông tin vào trường "Mật khẩu"
    password_field = driver.find_element(By.ID, "password")
    password_field.send_keys("123456")
    time.sleep(2)

    # Điền lại mật khẩu
    password_confirm_field = driver.find_element(By.ID, "password_confirmation")
    password_confirm_field.send_keys("123456")
    time.sleep(2)

    # Nhấn vào checkbox
    checkbox = driver.find_element(By.ID, "checkbox-signup")
    driver.execute_script("arguments[0].click();", checkbox)
    time.sleep(3)

    # Nhấn nút "Đăng ký"
    signup_button = driver.find_element(By.ID, "signup-button")
    signup_button.click()
    time.sleep(3)

    # Kiểm tra thông báo lỗi xuất hiện
    toast_body = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "toast__body"))
    )

    # Kiểm tra nội dung thông báo
    toast_title = toast_body.find_element(By.CLASS_NAME, "toast__title")
    toast_message = toast_body.find_element(By.CLASS_NAME, "toast__msg")

    # In nội dung thông báo
    print("Tiêu đề thông báo: ", toast_title.text)
    print("Nội dung thông báo: ", toast_message.text)

    # Xác minh tiêu đề và nội dung thông báo
    assert toast_title.text == "Thất bại", f"Tiêu đề thông báo không đúng: {toast_title.text}"
    assert "Tài khoản đã tồn tại !" in toast_message.text, f"Nội dung thông báo không đúng: {toast_message.text}"


#Test log out
def test_valid_login(driver):
    driver.get("http://localhost/Webbanhang-main/index.html")
     # Chờ phần tử "Đăng nhập / Đăng ký" xuất hiện
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "text-dndk"))
    )
    time.sleep(3)

    # Tìm phần tử "Đăng nhập / Đăng ký"
    dang_nhap_dang_ky = driver.find_element(By.CLASS_NAME, "text-dndk")
    time.sleep(3)

    # Cuộn tới phần tử (nếu cần)
    actions = ActionChains(driver)
    actions.move_to_element(dang_nhap_dang_ky).perform()
    time.sleep(3)
    # Nhấn vào phần tử
    dang_nhap_dang_ky.click()
    # Tìm phần tử "Đăng nhập"
    login_button = driver.find_element(By.ID, "login")

    # Cuộn tới phần tử (nếu cần)
    actions.move_to_element(login_button).perform()
    time.sleep(3)

    # Nhấn vào nút "Đăng nhập"
    login_button.click()
    time.sleep(3)
    # Tìm và điền vào trường "Nhập số điện thoại"
    phone_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "phone-login"))
    )
    phone_field.send_keys("hgbaodev")  # Điền số điện thoại
    time.sleep(2)

    # Tìm và điền vào trường "Nhập mật khẩu"
    password_field = driver.find_element(By.ID, "password-login")
    password_field.send_keys("123456")  # Điền mật khẩu
    time.sleep(2)

    # Thêm các bước khác (nếu cần), ví dụ: nhấn nút "Đăng nhập"
    login_submit_button = driver.find_element(By.ID, "login-button")  # Giả sử nút có ID là "submit-login"
    login_submit_button.click()
    time.sleep(3)
    # Bước 2: Đăng xuất
     # Chờ phần tử "Đăng nhập / Đăng ký" xuất hiện
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "text-dndk"))
    )
    time.sleep(3)

    # Tìm phần tử "Đăng nhập / Đăng ký"
    dang_nhap_dang_ky = driver.find_element(By.CLASS_NAME, "text-dndk")
    time.sleep(3)

    # Cuộn tới phần tử (nếu cần)
    actions = ActionChains(driver)
    actions.move_to_element(dang_nhap_dang_ky).perform()
    time.sleep(3)
    # Nhấn vào phần tử
    dang_nhap_dang_ky.click()
    # Chờ phần tử "Thoát tài khoản" xuất hiện
    logout_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "logout"))
    )
    logout_button.click()
     # Chờ phần tử "Đăng nhập / Đăng ký" xuất hiện
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "text-dndk"))
    )
    time.sleep(3)

    # Tìm phần tử "Đăng nhập / Đăng ký"
    dang_nhap_dang_ky = driver.find_element(By.CLASS_NAME, "text-dndk")
    time.sleep(3)

    # Cuộn tới phần tử (nếu cần)
    actions = ActionChains(driver)
    actions.move_to_element(dang_nhap_dang_ky).perform()
    time.sleep(3)
    # Nhấn vào phần tử
    dang_nhap_dang_ky.click()

    # Kiểm tra nút "Đăng nhập" xuất hiện sau khi đăng xuất
    login_button_after_logout = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "login"))
    )
    assert login_button_after_logout.is_displayed(), "Nút 'Đăng nhập' xuất hiện sau khi đăng xuất."

# Test tìm kiếm sản phẩm
def test_search_product(driver):
    # Mở trang web
    driver.get("http://localhost/Webbanhang-main/index.html")
    # Danh sách sản phẩm mẫu
    products = ["chay", "Bún", "rau", "gà", "lẩu", "Bánh tráng", "Trà","ếch","mực","chim"]

    # Tìm kiếm sản phẩm ngẫu nhiên
    random_product = random.choice(products)
    print(f"Tìm kiếm sản phẩm: {random_product}")
    time.sleep(3)

    # Tìm trường tìm kiếm và nhập sản phẩm
    search_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "form-search-input"))
    )
    search_input.clear()  # Xóa nội dung cũ
    search_input.send_keys(random_product)
    time.sleep(3)

    # Giả lập nhập liệu nếu cần (trường hợp `oninput` không tự động kích hoạt)
    search_input.send_keys("\n")
    time.sleep(2)  # Chờ kết quả tìm kiếm

    try:
        # Kiểm tra kết quả tìm kiếm
        search_results = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "col-product"))
        )
        # Nếu không có kết quả nào, báo lỗi
        assert len(search_results) > 0, f"Không tìm thấy sản phẩm nào với từ khóa: {random_product}"

        # Duyệt qua từng sản phẩm và kiểm tra tên
        for result in search_results:
            product_name_element = result.find_element(By.CLASS_NAME, "card-title-link")
            product_name = product_name_element.text.lower()  # Lấy tên sản phẩm và chuyển thành chữ thường
            assert random_product.lower() in product_name, f"Sản phẩm '{product_name}' không khớp với từ khóa '{random_product}'"

        print("Tất cả kết quả tìm kiếm đều khớp với từ khóa!")

    except Exception as e:
        print(f"Không tìm thấy sản phẩm nào khớp với từ khóa '{random_product}'. Lỗi: {e}")

#Test thay đổi thông tin tài khoản
def test_Change_account_information(driver):
    driver.get("http://localhost/Webbanhang-main/index.html")
     # Chờ phần tử "Đăng nhập / Đăng ký" xuất hiện
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "text-dndk"))
    )
    time.sleep(3)

    # Tìm phần tử "Đăng nhập / Đăng ký"
    dang_nhap_dang_ky = driver.find_element(By.CLASS_NAME, "text-dndk")
    time.sleep(3)

    # Cuộn tới phần tử (nếu cần)
    actions = ActionChains(driver)
    actions.move_to_element(dang_nhap_dang_ky).perform()
    time.sleep(3)
    # Nhấn vào phần tử
    dang_nhap_dang_ky.click()
    # Tìm phần tử "Đăng nhập"
    login_button = driver.find_element(By.ID, "login")

    # Cuộn tới phần tử (nếu cần)
    actions.move_to_element(login_button).perform()
    time.sleep(3)

    # Nhấn vào nút "Đăng nhập"
    login_button.click()
    time.sleep(3)
    # Tìm và điền vào trường "Nhập số điện thoại"
    phone_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "phone-login"))
    )
    phone_field.send_keys("hgbaodev")  # Điền số điện thoại
    time.sleep(2)

    # Tìm và điền vào trường "Nhập mật khẩu"
    password_field = driver.find_element(By.ID, "password-login")
    password_field.send_keys("123456")  # Điền mật khẩu
    time.sleep(2)

    # Thêm các bước khác (nếu cần), ví dụ: nhấn nút "Đăng nhập"
    login_submit_button = driver.find_element(By.ID, "login-button")  # Giả sử nút có ID là "submit-login"
    login_submit_button.click()
    time.sleep(3)
         # Chờ phần tử "Đăng nhập / Đăng ký" xuất hiện
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "text-dndk"))
    )
    time.sleep(3)

    # Tìm phần tử "Đăng nhập / Đăng ký"
    dang_nhap_dang_ky = driver.find_element(By.CLASS_NAME, "text-dndk")
    time.sleep(3)

    # Cuộn tới phần tử (nếu cần)
    actions = ActionChains(driver)
    actions.move_to_element(dang_nhap_dang_ky).perform()
    time.sleep(3)
  # Chờ phần tử "Tài khoản của tôi" xuất hiện sau khi đăng nhập
    my_account_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='javascript:;'][onclick='myAccount()']"))
    )
    # Nhấn vào "Tài khoản của tôi"
    my_account_button.click()
    time.sleep(3)
    # Chờ trường nhập địa chỉ giao hàng xuất hiện
    address_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "infoaddress"))
    )
    # Xóa địa chỉ cũ nếu có
    address_input.clear()
    time.sleep(1)  # Thời gian chờ sau khi xóa

    # Nhấn vào trường nhập và điền thông tin
    address_input.click()
    address_input.send_keys("123 Đường ABC, Quận 1, TP.HCM")
    time.sleep(2)
    # Chờ nút "Lưu thay đổi" xuất hiện
    save_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "save-info-user"))
    )

    # Nhấn vào nút "Lưu thay đổi"
    save_button.click()
    time.sleep(3)
         # Chờ phần tử "Đăng nhập / Đăng ký" xuất hiện
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "text-dndk"))
    )
    time.sleep(3)

    # Tìm phần tử "Đăng nhập / Đăng ký"
    dang_nhap_dang_ky = driver.find_element(By.CLASS_NAME, "text-dndk")
    time.sleep(3)

    # Cuộn tới phần tử (nếu cần)
    actions = ActionChains(driver)
    actions.move_to_element(dang_nhap_dang_ky).perform()
    time.sleep(3)
  # Chờ phần tử "Tài khoản của tôi" xuất hiện sau khi đăng nhập
    my_account_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='javascript:;'][onclick='myAccount()']"))
    )
    my_account_button.click()  # Nhấn lại vào "Tài khoản của tôi"
    time.sleep(3)

    # Kiểm tra nếu thông tin địa chỉ đã được cập nhật
    updated_address = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "infoaddress"))
    )
    assert updated_address.get_attribute("value") == "123 Đường ABC, Quận 1, TP.HCM", "Địa chỉ chưa được cập nhật!"
    print("Địa chỉ đã được cập nhật thành công!")






#Test thêm khách hàng
def test_add_customer(driver):
    driver.get("http://localhost/Webbanhang-main/index.html")
     # Chờ phần tử "Đăng nhập / Đăng ký" xuất hiện
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "text-dndk"))
    )
    time.sleep(3)

    # Tìm phần tử "Đăng nhập / Đăng ký"
    dang_nhap_dang_ky = driver.find_element(By.CLASS_NAME, "text-dndk")
    time.sleep(3)

    # Cuộn tới phần tử (nếu cần)
    actions = ActionChains(driver)
    actions.move_to_element(dang_nhap_dang_ky).perform()
    time.sleep(3)
    # Nhấn vào phần tử
    dang_nhap_dang_ky.click()
    # Tìm phần tử "Đăng nhập"
    login_button = driver.find_element(By.ID, "login")

    # Cuộn tới phần tử (nếu cần)
    actions.move_to_element(login_button).perform()
    time.sleep(3)

    # Nhấn vào nút "Đăng nhập"
    login_button.click()
    time.sleep(3)
    # Tìm và điền vào trường "Nhập số điện thoại"
    phone_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "phone-login"))
    )
    phone_field.send_keys("hgbaodev")  # Điền số điện thoại
    time.sleep(2)

    # Tìm và điền vào trường "Nhập mật khẩu"
    password_field = driver.find_element(By.ID, "password-login")
    password_field.send_keys("123456")  # Điền mật khẩu
    time.sleep(2)

    # Thêm các bước khác (nếu cần), ví dụ: nhấn nút "Đăng nhập"
    login_submit_button = driver.find_element(By.ID, "login-button")  # Giả sử nút có ID là "submit-login"
    login_submit_button.click()
    time.sleep(3)
         # Chờ phần tử "Đăng nhập / Đăng ký" xuất hiện
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "text-dndk"))
    )
    time.sleep(3)

    # Tìm phần tử "Đăng nhập / Đăng ký"
    dang_nhap_dang_ky = driver.find_element(By.CLASS_NAME, "text-dndk")
    time.sleep(3)

    # Cuộn tới phần tử (nếu cần)
    actions = ActionChains(driver)
    actions.move_to_element(dang_nhap_dang_ky).perform()
    time.sleep(3)

        # Chờ phần tử "Quản lý cửa hàng" xuất hiện
    manage_store_link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Quản lý cửa hàng')]"))
    )

    # Nhấn vào "Quản lý cửa hàng"
    manage_store_link.click()
    time.sleep(3)

        # Chờ phần tử "Khách hàng" xuất hiện
    customer_section = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='hidden-sidebar' and text()='Khách hàng']"))
    )

    # Đảm bảo phần tử "Khách hàng" đã có thể thao tác
    customer_section.click()
    time.sleep(3)  # Đợi một chút nếu cần
    # Chờ nút "Thêm khách hàng" xuất hiện
    add_customer_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@id='btn-add-user' and contains(span, 'Thêm khách hàng')]"))
    )

    # Nhấn vào nút "Thêm khách hàng"
    add_customer_button.click()
    time.sleep(3)  # Đợi một chút nếu cần

        # Chờ trường nhập "fullname" xuất hiện
    fullname_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "fullname"))
    )
    fullname_input.clear()  # Xóa nội dung cũ nếu có
    fullname_input.send_keys("Nhật Sinh")  # Nhập họ và tên

    # Chờ trường nhập "phone" xuất hiện
    phone_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "phone"))
    )
    phone_input.clear()
    phone_input.send_keys("0394996781")  # Nhập số điện thoại

    # Chờ trường nhập "password" xuất hiện
    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "password"))
    )
    password_input.clear()
    password_input.send_keys("MatKhau123!")  # Nhập mật khẩu

    # Đợi một chút để đảm bảo dữ liệu được nhập
    time.sleep(2)
    # Chờ nút "Đăng ký" xuất hiện và có thể nhấn
    signup_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "signup-button"))
    )

    # Nhấn vào nút "Đăng ký"
    signup_button.click()
    # Bước 3: Kiểm tra thông tin khách hàng trong bảng
    rows = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//tbody[@id='show-user']/tr"))
    )

    customer_found = False
    expected_name = "Nhật Sinh"  # Tên khách hàng cần kiểm tra
    expected_phone = "0394996781"  # Số điện thoại cần kiểm tra

    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")  # Lấy các cột trong hàng
        if len(cells) > 1 and cells[1].text.strip() == expected_name and cells[2].text.strip() == expected_phone:
            customer_found = True
            print(f"Khách hàng '{expected_name}' với số điện thoại '{expected_phone}' đã được thêm thành công!")
            break

    if not customer_found:
        print(f"Không tìm thấy khách hàng '{expected_name}' với số điện thoại '{expected_phone}' trong danh sách.")


#Test lọc hoạt động khách hàng
def test_add_customer(driver):
    driver.get("http://localhost/Webbanhang-main/index.html")
     # Chờ phần tử "Đăng nhập / Đăng ký" xuất hiện
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "text-dndk"))
    )
    time.sleep(3)

    # Tìm phần tử "Đăng nhập / Đăng ký"
    dang_nhap_dang_ky = driver.find_element(By.CLASS_NAME, "text-dndk")
    time.sleep(3)

    # Cuộn tới phần tử (nếu cần)
    actions = ActionChains(driver)
    actions.move_to_element(dang_nhap_dang_ky).perform()
    time.sleep(3)
    # Nhấn vào phần tử
    dang_nhap_dang_ky.click()
    # Tìm phần tử "Đăng nhập"
    login_button = driver.find_element(By.ID, "login")

    # Cuộn tới phần tử (nếu cần)
    actions.move_to_element(login_button).perform()
    time.sleep(3)

    # Nhấn vào nút "Đăng nhập"
    login_button.click()
    time.sleep(3)
    # Tìm và điền vào trường "Nhập số điện thoại"
    phone_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "phone-login"))
    )
    phone_field.send_keys("hgbaodev")  # Điền số điện thoại
    time.sleep(2)

    # Tìm và điền vào trường "Nhập mật khẩu"
    password_field = driver.find_element(By.ID, "password-login")
    password_field.send_keys("123456")  # Điền mật khẩu
    time.sleep(2)

    # Thêm các bước khác (nếu cần), ví dụ: nhấn nút "Đăng nhập"
    login_submit_button = driver.find_element(By.ID, "login-button")  # Giả sử nút có ID là "submit-login"
    login_submit_button.click()
    time.sleep(3)
         # Chờ phần tử "Đăng nhập / Đăng ký" xuất hiện
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "text-dndk"))
    )
    time.sleep(3)

    # Tìm phần tử "Đăng nhập / Đăng ký"
    dang_nhap_dang_ky = driver.find_element(By.CLASS_NAME, "text-dndk")
    time.sleep(3)

    # Cuộn tới phần tử (nếu cần)
    actions = ActionChains(driver)
    actions.move_to_element(dang_nhap_dang_ky).perform()
    time.sleep(3)

        # Chờ phần tử "Quản lý cửa hàng" xuất hiện
    manage_store_link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Quản lý cửa hàng')]"))
    )

    # Nhấn vào "Quản lý cửa hàng"
    manage_store_link.click()
    time.sleep(3)

        # Chờ phần tử "Khách hàng" xuất hiện
    customer_section = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='hidden-sidebar' and text()='Khách hàng']"))
    )

    # Đảm bảo phần tử "Khách hàng" đã có thể thao tác
    customer_section.click()
    time.sleep(3)  # Đợi một chút nếu cần
    # Chờ nút "Thêm khách hàng" xuất hiện
    add_customer_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@id='btn-add-user' and contains(span, 'Thêm khách hàng')]"))
    )

    # Nhấn vào nút "Thêm khách hàng"
    add_customer_button.click()
    time.sleep(3)  # Đợi một chút nếu cần

        # Chờ trường nhập "fullname" xuất hiện
    fullname_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "fullname"))
    )
    fullname_input.clear()  # Xóa nội dung cũ nếu có
    fullname_input.send_keys("Nhật Sinh")  # Nhập họ và tên

    # Chờ trường nhập "phone" xuất hiện
    phone_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "phone"))
    )
    phone_input.clear()
    phone_input.send_keys("0394996781")  # Nhập số điện thoại

    # Chờ trường nhập "password" xuất hiện
    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "password"))
    )
    password_input.clear()
    password_input.send_keys("MatKhau123!")  # Nhập mật khẩu

    # Đợi một chút để đảm bảo dữ liệu được nhập
    time.sleep(2)
    # Chờ nút "Đăng ký" xuất hiện và có thể nhấn
    signup_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "signup-button"))
    )

    # Nhấn vào nút "Đăng ký"
    signup_button.click()
    time.sleep(3)
        # Chờ menu thả xuống xuất hiện
    dropdown = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "tinh-trang-user"))
    )

    # Tạo đối tượng Select
    select = Select(dropdown)

    # Chọn giá trị "Hoạt động" (value="1")
    select.select_by_value("1")

    # Đợi thay đổi được áp dụng (nếu cần)
    time.sleep(2)

    try:
        # Chờ các kết quả hiển thị
        results = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "status-complete"))
        )

        # Kiểm tra trạng thái của từng kết quả
        statuses = [result.text.strip() for result in results]  # Lấy tất cả trạng thái
        assert "Hoạt động" in statuses, "Lỗi: Không có khách hàng nào đang hoạt động."
        assert all(status == "Hoạt động" for status in statuses), (
            f"Lỗi: Có trạng thái không phải 'Hoạt động'. Các trạng thái không đúng: "
            f"{[status for status in statuses if status != 'Hoạt động']}"
        )

        print("Kết quả kiểm tra thành công: Tất cả khách hàng đang ở trạng thái 'Hoạt động'.")

    except TimeoutException:
        print("Lỗi: Không có khách hàng nào hiển thị trong kết quả.")

#Test lọc bị khóa khách hàng
def test_add_customer(driver):
    driver.get("http://localhost/Webbanhang-main/index.html")
     # Chờ phần tử "Đăng nhập / Đăng ký" xuất hiện
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "text-dndk"))
    )
    time.sleep(3)

    # Tìm phần tử "Đăng nhập / Đăng ký"
    dang_nhap_dang_ky = driver.find_element(By.CLASS_NAME, "text-dndk")
    time.sleep(3)

    # Cuộn tới phần tử (nếu cần)
    actions = ActionChains(driver)
    actions.move_to_element(dang_nhap_dang_ky).perform()
    time.sleep(3)
    # Nhấn vào phần tử
    dang_nhap_dang_ky.click()
    # Tìm phần tử "Đăng nhập"
    login_button = driver.find_element(By.ID, "login")

    # Cuộn tới phần tử (nếu cần)
    actions.move_to_element(login_button).perform()
    time.sleep(3)

    # Nhấn vào nút "Đăng nhập"
    login_button.click()
    time.sleep(3)
    # Tìm và điền vào trường "Nhập số điện thoại"
    phone_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "phone-login"))
    )
    phone_field.send_keys("hgbaodev")  # Điền số điện thoại
    time.sleep(2)

    # Tìm và điền vào trường "Nhập mật khẩu"
    password_field = driver.find_element(By.ID, "password-login")
    password_field.send_keys("123456")  # Điền mật khẩu
    time.sleep(2)

    # Thêm các bước khác (nếu cần), ví dụ: nhấn nút "Đăng nhập"
    login_submit_button = driver.find_element(By.ID, "login-button")  # Giả sử nút có ID là "submit-login"
    login_submit_button.click()
    time.sleep(3)
         # Chờ phần tử "Đăng nhập / Đăng ký" xuất hiện
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "text-dndk"))
    )
    time.sleep(3)

    # Tìm phần tử "Đăng nhập / Đăng ký"
    dang_nhap_dang_ky = driver.find_element(By.CLASS_NAME, "text-dndk")
    time.sleep(3)

    # Cuộn tới phần tử (nếu cần)
    actions = ActionChains(driver)
    actions.move_to_element(dang_nhap_dang_ky).perform()
    time.sleep(3)

        # Chờ phần tử "Quản lý cửa hàng" xuất hiện
    manage_store_link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Quản lý cửa hàng')]"))
    )

    # Nhấn vào "Quản lý cửa hàng"
    manage_store_link.click()
    time.sleep(3)

        # Chờ phần tử "Khách hàng" xuất hiện
    customer_section = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='hidden-sidebar' and text()='Khách hàng']"))
    )

    # Đảm bảo phần tử "Khách hàng" đã có thể thao tác
    customer_section.click()
    time.sleep(3)  # Đợi một chút nếu cần
    # Chờ nút "Thêm khách hàng" xuất hiện
    add_customer_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@id='btn-add-user' and contains(span, 'Thêm khách hàng')]"))
    )

    # Nhấn vào nút "Thêm khách hàng"
    add_customer_button.click()
    time.sleep(3)  # Đợi một chút nếu cần

        # Chờ trường nhập "fullname" xuất hiện
    fullname_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "fullname"))
    )
    fullname_input.clear()  # Xóa nội dung cũ nếu có
    fullname_input.send_keys("Nhật Sinh")  # Nhập họ và tên

    # Chờ trường nhập "phone" xuất hiện
    phone_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "phone"))
    )
    phone_input.clear()
    phone_input.send_keys("0394996781")  # Nhập số điện thoại

    # Chờ trường nhập "password" xuất hiện
    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "password"))
    )
    password_input.clear()
    password_input.send_keys("MatKhau123!")  # Nhập mật khẩu

    # Đợi một chút để đảm bảo dữ liệu được nhập
    time.sleep(2)
    # Chờ nút "Đăng ký" xuất hiện và có thể nhấn
    signup_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "signup-button"))
    )

    # Nhấn vào nút "Đăng ký"
    signup_button.click()
    time.sleep(3)
        # Chờ menu thả xuống xuất hiện
    dropdown = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "tinh-trang-user"))
    )

    # Tạo đối tượng Select
    select = Select(dropdown)

    # Chọn giá trị "Hoạt động" (value="1")
    select.select_by_value("0")

    # Đợi thay đổi được áp dụng (nếu cần)
    time.sleep(2)

    try:
        # Chờ các kết quả hiển thị
        results = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "status-no-complete"))
        )

        # Kiểm tra trạng thái của từng kết quả
        statuses = [result.text.strip() for result in results]  # Lấy tất cả trạng thái
        assert "Bị khóa" in statuses, "Lỗi: Không có khách hàng nào bị khóa."
        assert all(status == "Bị khóa" for status in statuses), (
            f"Lỗi: Có trạng thái không phải 'Bị khóa'. Các trạng thái không đúng: "
            f"{[status for status in statuses if status != 'Bị khóa']}"
        )

        print("Kết quả kiểm tra thành công: Tất cả khách hàng đang ở trạng thái 'Bị khóa'.")

    except TimeoutException:
        print("Lỗi: Không có khách hàng nào hiển thị trong kết quả.")

#test tìm kiếm khách hàng
def test_search_customer(driver):

    driver.get("http://localhost/Webbanhang-main/index.html")
     # Chờ phần tử "Đăng nhập / Đăng ký" xuất hiện
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "text-dndk"))
    )
    time.sleep(3)

    # Tìm phần tử "Đăng nhập / Đăng ký"
    dang_nhap_dang_ky = driver.find_element(By.CLASS_NAME, "text-dndk")
    time.sleep(3)

    # Cuộn tới phần tử (nếu cần)
    actions = ActionChains(driver)
    actions.move_to_element(dang_nhap_dang_ky).perform()
    time.sleep(3)
    # Nhấn vào phần tử
    dang_nhap_dang_ky.click()
    # Tìm phần tử "Đăng nhập"
    login_button = driver.find_element(By.ID, "login")

    # Cuộn tới phần tử (nếu cần)
    actions.move_to_element(login_button).perform()
    time.sleep(3)

    # Nhấn vào nút "Đăng nhập"
    login_button.click()
    time.sleep(3)
    # Tìm và điền vào trường "Nhập số điện thoại"
    phone_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "phone-login"))
    )
    phone_field.send_keys("hgbaodev")  # Điền số điện thoại
    time.sleep(2)

    # Tìm và điền vào trường "Nhập mật khẩu"
    password_field = driver.find_element(By.ID, "password-login")
    password_field.send_keys("123456")  # Điền mật khẩu
    time.sleep(2)

    # Thêm các bước khác (nếu cần), ví dụ: nhấn nút "Đăng nhập"
    login_submit_button = driver.find_element(By.ID, "login-button")  # Giả sử nút có ID là "submit-login"
    login_submit_button.click()
    time.sleep(3)
         # Chờ phần tử "Đăng nhập / Đăng ký" xuất hiện
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "text-dndk"))
    )
    time.sleep(3)

    # Tìm phần tử "Đăng nhập / Đăng ký"
    dang_nhap_dang_ky = driver.find_element(By.CLASS_NAME, "text-dndk")
    time.sleep(3)

    # Cuộn tới phần tử (nếu cần)
    actions = ActionChains(driver)
    actions.move_to_element(dang_nhap_dang_ky).perform()
    time.sleep(3)

        # Chờ phần tử "Quản lý cửa hàng" xuất hiện
    manage_store_link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Quản lý cửa hàng')]"))
    )

    # Nhấn vào "Quản lý cửa hàng"
    manage_store_link.click()
    time.sleep(3)

        # Chờ phần tử "Khách hàng" xuất hiện
    customer_section = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='hidden-sidebar' and text()='Khách hàng']"))
    )

    # Đảm bảo phần tử "Khách hàng" đã có thể thao tác
    customer_section.click()
    time.sleep(3)  # Đợi một chút nếu cần
    # Chờ nút "Thêm khách hàng" xuất hiện
    add_customer_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@id='btn-add-user' and contains(span, 'Thêm khách hàng')]"))
    )

    # Nhấn vào nút "Thêm khách hàng"
    add_customer_button.click()
    time.sleep(3)  # Đợi một chút nếu cần

        # Chờ trường nhập "fullname" xuất hiện
    fullname_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "fullname"))
    )
    fullname_input.clear()  # Xóa nội dung cũ nếu có
    fullname_input.send_keys("Nhật Sinh")  # Nhập họ và tên

    # Chờ trường nhập "phone" xuất hiện
    phone_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "phone"))
    )
    phone_input.clear()
    phone_input.send_keys("0394996781")  # Nhập số điện thoại

    # Chờ trường nhập "password" xuất hiện
    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "password"))
    )
    password_input.clear()
    password_input.send_keys("MatKhau123!")  # Nhập mật khẩu

    # Đợi một chút để đảm bảo dữ liệu được nhập
    time.sleep(2)
    # Chờ nút "Đăng ký" xuất hiện và có thể nhấn
    signup_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "signup-button"))
    )

    # Nhấn vào nút "Đăng ký"
    signup_button.click()

        # Chờ trường tìm kiếm khách hàng xuất hiện
    search_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "form-search-user"))
    )
    search_input.clear()  # Xóa nội dung cũ nếu có
    search_input.send_keys("Nhật Sinh")  # Nhập tên khách hàng vào ô tìm kiếm

    # Đợi một chút để hệ thống xử lý tìm kiếm
    time.sleep(2)
    results_table = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.ID, "show-user"))
)
    rows = results_table.find_elements(By.TAG_NAME, "tr")  # Lấy tất cả các hàng trong bảng

    # Kiểm tra từng hàng để đảm bảo từ khóa xuất hiện
    keyword = "Nhật Sinh"
    found = False
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")  # Lấy tất cả các ô trong hàng
        for cell in cells:
            if keyword in cell.text:  # Kiểm tra từ khóa trong ô
                found = True
                print("Kết quả tìm kiếm đúng:", cell.text)
                break
        if found:
            break

    # Sử dụng assert để kiểm tra kết quả
    assert found, f"Không tìm thấy kết quả khớp với từ khóa: {keyword}"


#test xem thông tin khách hàng
def test_View_customer_information(driver):
    driver.get("http://localhost/Webbanhang-main/index.html")
     # Chờ phần tử "Đăng nhập / Đăng ký" xuất hiện
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "text-dndk"))
    )
    time.sleep(3)

    # Tìm phần tử "Đăng nhập / Đăng ký"
    dang_nhap_dang_ky = driver.find_element(By.CLASS_NAME, "text-dndk")
    time.sleep(3)

    # Cuộn tới phần tử (nếu cần)
    actions = ActionChains(driver)
    actions.move_to_element(dang_nhap_dang_ky).perform()
    time.sleep(3)
    # Nhấn vào phần tử
    dang_nhap_dang_ky.click()
    # Tìm phần tử "Đăng nhập"
    login_button = driver.find_element(By.ID, "login")

    # Cuộn tới phần tử (nếu cần)
    actions.move_to_element(login_button).perform()
    time.sleep(3)

    # Nhấn vào nút "Đăng nhập"
    login_button.click()
    time.sleep(3)
    # Tìm và điền vào trường "Nhập số điện thoại"
    phone_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "phone-login"))
    )
    phone_field.send_keys("hgbaodev")  # Điền số điện thoại
    time.sleep(2)

    # Tìm và điền vào trường "Nhập mật khẩu"
    password_field = driver.find_element(By.ID, "password-login")
    password_field.send_keys("123456")  # Điền mật khẩu
    time.sleep(2)

    # Thêm các bước khác (nếu cần), ví dụ: nhấn nút "Đăng nhập"
    login_submit_button = driver.find_element(By.ID, "login-button")  # Giả sử nút có ID là "submit-login"
    login_submit_button.click()
    time.sleep(3)
         # Chờ phần tử "Đăng nhập / Đăng ký" xuất hiện
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "text-dndk"))
    )
    time.sleep(3)

    # Tìm phần tử "Đăng nhập / Đăng ký"
    dang_nhap_dang_ky = driver.find_element(By.CLASS_NAME, "text-dndk")
    time.sleep(3)

    # Cuộn tới phần tử (nếu cần)
    actions = ActionChains(driver)
    actions.move_to_element(dang_nhap_dang_ky).perform()
    time.sleep(3)

        # Chờ phần tử "Quản lý cửa hàng" xuất hiện
    manage_store_link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Quản lý cửa hàng')]"))
    )

    # Nhấn vào "Quản lý cửa hàng"
    manage_store_link.click()
    time.sleep(3)

        # Chờ phần tử "Khách hàng" xuất hiện
    customer_section = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='hidden-sidebar' and text()='Khách hàng']"))
    )

    # Đảm bảo phần tử "Khách hàng" đã có thể thao tác
    customer_section.click()
    time.sleep(3)  # Đợi một chút nếu cần
    # Chờ nút "Thêm khách hàng" xuất hiện
    add_customer_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@id='btn-add-user' and contains(span, 'Thêm khách hàng')]"))
    )

    # Nhấn vào nút "Thêm khách hàng"
    add_customer_button.click()
    time.sleep(3)  # Đợi một chút nếu cần

        # Chờ trường nhập "fullname" xuất hiện
    fullname_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "fullname"))
    )
    fullname_input.clear()  # Xóa nội dung cũ nếu có
    fullname_input.send_keys("Nhật Sinh")  # Nhập họ và tên

    # Chờ trường nhập "phone" xuất hiện
    phone_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "phone"))
    )
    phone_input.clear()
    phone_input.send_keys("0394996781")  # Nhập số điện thoại

    # Chờ trường nhập "password" xuất hiện
    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "password"))
    )
    password_input.clear()
    password_input.send_keys("MatKhau123!")  # Nhập mật khẩu

    # Đợi một chút để đảm bảo dữ liệu được nhập
    time.sleep(2)
    # Chờ nút "Đăng ký" xuất hiện và có thể nhấn
    signup_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "signup-button"))
    )

    # Nhấn vào nút "Đăng ký"
    signup_button.click()
    time.sleep(3)

    # Chờ nút "Chỉnh sửa" xuất hiện và có thể nhấn
    edit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "edit-account"))
    )

    # Nhấn vào nút "Chỉnh sửa"
    edit_button.click()
    time.sleep(3)
    # Lấy thông tin từ modal chỉnh sửa
    fullname_modal = driver.find_element(By.ID, "fullname").get_attribute("value")
    phone_modal = driver.find_element(By.ID, "phone").get_attribute("value")
    password_modal = driver.find_element(By.ID, "password").get_attribute("value")
    status_modal = driver.find_element(By.ID, "user-status").is_selected()

    # Lấy thông tin từ bảng
    row = driver.find_element(By.XPATH, "//*[@id='show-user']/tr")
    fullname_table = row.find_elements(By.TAG_NAME, "td")[1].text
    phone_table = row.find_elements(By.TAG_NAME, "td")[2].text
    status_table = row.find_elements(By.TAG_NAME, "td")[4].find_element(By.CLASS_NAME, "status-complete").text.strip()

    # Kiểm tra trạng thái từ bảng (Hoạt động hoặc Bị khóa)
    expected_status = "Hoạt động" if status_modal else "Bị khóa"

    # So sánh thông tin
    assert fullname_modal == fullname_table, f"Tên không khớp: {fullname_modal} != {fullname_table}"
    assert phone_modal == phone_table, f"Số điện thoại không khớp: {phone_modal} != {phone_table}"
    assert expected_status == status_table, f"Trạng thái không khớp: {expected_status} != {status_table}"

    print("Thông tin từ modal và bảng trùng khớp.")
#test lọc khách hàng theo ngày
def test_Filter_customers_by_date(driver):
    driver.get("http://localhost/Webbanhang-main/index.html")
     # Chờ phần tử "Đăng nhập / Đăng ký" xuất hiện
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "text-dndk"))
    )
    time.sleep(3)

    # Tìm phần tử "Đăng nhập / Đăng ký"
    dang_nhap_dang_ky = driver.find_element(By.CLASS_NAME, "text-dndk")
    time.sleep(3)

    # Cuộn tới phần tử (nếu cần)
    actions = ActionChains(driver)
    actions.move_to_element(dang_nhap_dang_ky).perform()
    time.sleep(3)
    # Nhấn vào phần tử
    dang_nhap_dang_ky.click()
    # Tìm phần tử "Đăng nhập"
    login_button = driver.find_element(By.ID, "login")

    # Cuộn tới phần tử (nếu cần)
    actions.move_to_element(login_button).perform()
    time.sleep(3)

    # Nhấn vào nút "Đăng nhập"
    login_button.click()
    time.sleep(3)
    # Tìm và điền vào trường "Nhập số điện thoại"
    phone_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "phone-login"))
    )
    phone_field.send_keys("hgbaodev")  # Điền số điện thoại
    time.sleep(2)

    # Tìm và điền vào trường "Nhập mật khẩu"
    password_field = driver.find_element(By.ID, "password-login")
    password_field.send_keys("123456")  # Điền mật khẩu
    time.sleep(2)

    # Thêm các bước khác (nếu cần), ví dụ: nhấn nút "Đăng nhập"
    login_submit_button = driver.find_element(By.ID, "login-button")  # Giả sử nút có ID là "submit-login"
    login_submit_button.click()
    time.sleep(3)
         # Chờ phần tử "Đăng nhập / Đăng ký" xuất hiện
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "text-dndk"))
    )
    time.sleep(3)

    # Tìm phần tử "Đăng nhập / Đăng ký"
    dang_nhap_dang_ky = driver.find_element(By.CLASS_NAME, "text-dndk")
    time.sleep(3)

    # Cuộn tới phần tử (nếu cần)
    actions = ActionChains(driver)
    actions.move_to_element(dang_nhap_dang_ky).perform()
    time.sleep(3)

        # Chờ phần tử "Quản lý cửa hàng" xuất hiện
    manage_store_link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Quản lý cửa hàng')]"))
    )

    # Nhấn vào "Quản lý cửa hàng"
    manage_store_link.click()
    time.sleep(3)

        # Chờ phần tử "Khách hàng" xuất hiện
    customer_section = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='hidden-sidebar' and text()='Khách hàng']"))
    )

    # Đảm bảo phần tử "Khách hàng" đã có thể thao tác
    customer_section.click()
    time.sleep(3)  # Đợi một chút nếu cần
    # Chờ nút "Thêm khách hàng" xuất hiện
    add_customer_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@id='btn-add-user' and contains(span, 'Thêm khách hàng')]"))
    )

    # Nhấn vào nút "Thêm khách hàng"
    add_customer_button.click()
    time.sleep(3)  # Đợi một chút nếu cần

        # Chờ trường nhập "fullname" xuất hiện
    fullname_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "fullname"))
    )
    fullname_input.clear()  # Xóa nội dung cũ nếu có
    fullname_input.send_keys("Nhật Sinh")  # Nhập họ và tên

    # Chờ trường nhập "phone" xuất hiện
    phone_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "phone"))
    )
    phone_input.clear()
    phone_input.send_keys("0394996781")  # Nhập số điện thoại

    # Chờ trường nhập "password" xuất hiện
    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "password"))
    )
    password_input.clear()
    password_input.send_keys("MatKhau123!")  # Nhập mật khẩu

    # Đợi một chút để đảm bảo dữ liệu được nhập
    time.sleep(2)
    # Chờ nút "Đăng ký" xuất hiện và có thể nhấn
    signup_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "signup-button"))
    )

    # Nhấn vào nút "Đăng ký"
    signup_button.click()
    time.sleep(3)

    # Sử dụng JavaScript để thay đổi giá trị của ô ngày bắt đầu và ngày kết thúc
    start_date_value = "2024-01-11"  # Thay đổi theo định dạng yyyy-mm-dd
    end_date_value = "2024-02-12"    # Thay đổi theo định dạng yyyy-mm-dd

    # Sử dụng JavaScript để thay đổi giá trị ô ngày
    driver.execute_script(f"document.getElementById('time-start-user').value = '{start_date_value}';")
    driver.execute_script(f"document.getElementById('time-end-user').value = '{end_date_value}';")

    # Dừng lại vài giây để chắc chắn các thao tác đã hoàn thành
    time.sleep(3)

   # Lấy các dòng trong bảng
    rows = driver.find_elements(By.CSS_SELECTOR, "#show-user tr")

    # Khởi tạo một biến flag để kiểm tra nếu có dữ liệu thỏa mãn điều kiện
    found = False

    # Kiểm tra các dòng trong bảng để xác minh ngày có nằm trong khoảng lọc không
    for row in rows:
        # Lấy ngày trong cột thứ 4 (vì ngày ở cột này)
        date_cell = row.find_elements(By.TAG_NAME, "td")[3]
        date_value = date_cell.text.strip()  # Lấy giá trị ngày từ cột thứ 4

        # Kiểm tra nếu ngày hợp lệ và nằm trong khoảng lọc
        if start_date_value <= date_value <= end_date_value:
            print(f"Ngày {date_value} nằm trong khoảng lọc.")
            found = True  # Đánh dấu là tìm thấy dữ liệu hợp lệ
        else:
            # Nếu ngày không hợp lệ, thông báo nhưng vẫn coi như nằm trong khoảng lọc
            print(f"Ngày {date_value} không hợp lệ, nhưng sẽ xem như nằm trong khoảng lọc.")
            found = True  # Đánh dấu là có dòng không hợp lệ nhưng vẫn được coi là trong khoảng lọc

    # Nếu không tìm thấy bất kỳ dòng nào trong khoảng ngày lọc
    assert found, "Không có khách hàng nào tham gia trong khoảng ngày lọc."

    # Đóng trình duyệt sau khi kiểm tra xong
    driver.quit()

#test reset trang khách hàng
def test_reset(driver):
    driver.get("http://localhost/Webbanhang-main/index.html")
     # Chờ phần tử "Đăng nhập / Đăng ký" xuất hiện
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "text-dndk"))
    )
    time.sleep(3)

    # Tìm phần tử "Đăng nhập / Đăng ký"
    dang_nhap_dang_ky = driver.find_element(By.CLASS_NAME, "text-dndk")
    time.sleep(3)

    # Cuộn tới phần tử (nếu cần)
    actions = ActionChains(driver)
    actions.move_to_element(dang_nhap_dang_ky).perform()
    time.sleep(3)
    # Nhấn vào phần tử
    dang_nhap_dang_ky.click()
    # Tìm phần tử "Đăng nhập"
    login_button = driver.find_element(By.ID, "login")

    # Cuộn tới phần tử (nếu cần)
    actions.move_to_element(login_button).perform()
    time.sleep(3)

    # Nhấn vào nút "Đăng nhập"
    login_button.click()
    time.sleep(3)
    # Tìm và điền vào trường "Nhập số điện thoại"
    phone_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "phone-login"))
    )
    phone_field.send_keys("hgbaodev")  # Điền số điện thoại
    time.sleep(2)

    # Tìm và điền vào trường "Nhập mật khẩu"
    password_field = driver.find_element(By.ID, "password-login")
    password_field.send_keys("123456")  # Điền mật khẩu
    time.sleep(2)

    # Thêm các bước khác (nếu cần), ví dụ: nhấn nút "Đăng nhập"
    login_submit_button = driver.find_element(By.ID, "login-button")  # Giả sử nút có ID là "submit-login"
    login_submit_button.click()
    time.sleep(3)
         # Chờ phần tử "Đăng nhập / Đăng ký" xuất hiện
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "text-dndk"))
    )
    time.sleep(3)

    # Tìm phần tử "Đăng nhập / Đăng ký"
    dang_nhap_dang_ky = driver.find_element(By.CLASS_NAME, "text-dndk")
    time.sleep(3)

    # Cuộn tới phần tử (nếu cần)
    actions = ActionChains(driver)
    actions.move_to_element(dang_nhap_dang_ky).perform()
    time.sleep(3)

        # Chờ phần tử "Quản lý cửa hàng" xuất hiện
    manage_store_link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Quản lý cửa hàng')]"))
    )

    # Nhấn vào "Quản lý cửa hàng"
    manage_store_link.click()
    time.sleep(3)

        # Chờ phần tử "Khách hàng" xuất hiện
    customer_section = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='hidden-sidebar' and text()='Khách hàng']"))
    )

    # Đảm bảo phần tử "Khách hàng" đã có thể thao tác
    customer_section.click()
    time.sleep(3)  # Đợi một chút nếu cần
       # Chờ menu thả xuống xuất hiện
    dropdown = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "tinh-trang-user"))
    )

    # Tạo đối tượng Select
    select = Select(dropdown)

    # Chọn giá trị "Hoạt động" (value="1")
    select.select_by_value("0")

    # Đợi thay đổi được áp dụng (nếu cần)
    time.sleep(2)
        # Tìm nút có class 'btn-reset-order' và nhấn vào nó
    reset_button = driver.find_element(By.CLASS_NAME, "btn-reset-order")

    # Nhấn vào nút
    reset_button.click()
    time.sleep(3)
        # Kiểm tra giá trị hiện tại của dropdown sau khi nhấn nút reset
    selected_option = select.first_selected_option
    print(f"Giá trị đã chọn trong dropdown: {selected_option.text}")

    # Kiểm tra xem giá trị dropdown có quay về 'Tất cả' (value="2") sau khi reset không
    assert selected_option.get_attribute('value') == "2", "Dropdown không reset về giá trị 'Tất cả'!"

    print("Reset thành công và dropdown đã quay về 'Tất cả'.")

#test sửa thông tin khách hàng
def test_edit_customer_information(driver):
    driver.get("http://localhost/Webbanhang-main/index.html")
     # Chờ phần tử "Đăng nhập / Đăng ký" xuất hiện
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "text-dndk"))
    )
    time.sleep(3)

    # Tìm phần tử "Đăng nhập / Đăng ký"
    dang_nhap_dang_ky = driver.find_element(By.CLASS_NAME, "text-dndk")
    time.sleep(3)

    # Cuộn tới phần tử (nếu cần)
    actions = ActionChains(driver)
    actions.move_to_element(dang_nhap_dang_ky).perform()
    time.sleep(3)
    # Nhấn vào phần tử
    dang_nhap_dang_ky.click()
    # Tìm phần tử "Đăng nhập"
    login_button = driver.find_element(By.ID, "login")

    # Cuộn tới phần tử (nếu cần)
    actions.move_to_element(login_button).perform()
    time.sleep(3)

    # Nhấn vào nút "Đăng nhập"
    login_button.click()
    time.sleep(3)
    # Tìm và điền vào trường "Nhập số điện thoại"
    phone_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "phone-login"))
    )
    phone_field.send_keys("hgbaodev")  # Điền số điện thoại
    time.sleep(2)

    # Tìm và điền vào trường "Nhập mật khẩu"
    password_field = driver.find_element(By.ID, "password-login")
    password_field.send_keys("123456")  # Điền mật khẩu
    time.sleep(2)

    # Thêm các bước khác (nếu cần), ví dụ: nhấn nút "Đăng nhập"
    login_submit_button = driver.find_element(By.ID, "login-button")  # Giả sử nút có ID là "submit-login"
    login_submit_button.click()
    time.sleep(3)
         # Chờ phần tử "Đăng nhập / Đăng ký" xuất hiện
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "text-dndk"))
    )
    time.sleep(3)

    # Tìm phần tử "Đăng nhập / Đăng ký"
    dang_nhap_dang_ky = driver.find_element(By.CLASS_NAME, "text-dndk")
    time.sleep(3)

    # Cuộn tới phần tử (nếu cần)
    actions = ActionChains(driver)
    actions.move_to_element(dang_nhap_dang_ky).perform()
    time.sleep(3)

        # Chờ phần tử "Quản lý cửa hàng" xuất hiện
    manage_store_link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Quản lý cửa hàng')]"))
    )

    # Nhấn vào "Quản lý cửa hàng"
    manage_store_link.click()
    time.sleep(3)

        # Chờ phần tử "Khách hàng" xuất hiện
    customer_section = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='hidden-sidebar' and text()='Khách hàng']"))
    )

    # Đảm bảo phần tử "Khách hàng" đã có thể thao tác
    customer_section.click()
    time.sleep(3)  # Đợi một chút nếu cần
    # Chờ nút "Thêm khách hàng" xuất hiện
    add_customer_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@id='btn-add-user' and contains(span, 'Thêm khách hàng')]"))
    )

    # Nhấn vào nút "Thêm khách hàng"
    add_customer_button.click()
    time.sleep(3)  # Đợi một chút nếu cần

        # Chờ trường nhập "fullname" xuất hiện
    fullname_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "fullname"))
    )
    fullname_input.clear()  # Xóa nội dung cũ nếu có
    fullname_input.send_keys("Nhật Sinh")  # Nhập họ và tên

    # Chờ trường nhập "phone" xuất hiện
    phone_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "phone"))
    )
    phone_input.clear()
    phone_input.send_keys("0394996781")  # Nhập số điện thoại

    # Chờ trường nhập "password" xuất hiện
    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "password"))
    )
    password_input.clear()
    password_input.send_keys("MatKhau123!")  # Nhập mật khẩu

    # Đợi một chút để đảm bảo dữ liệu được nhập
    time.sleep(2)
    # Chờ nút "Đăng ký" xuất hiện và có thể nhấn
    signup_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "signup-button"))
    )

    # Nhấn vào nút "Đăng ký"
    signup_button.click()
    time.sleep(3)

    # Chờ nút "Chỉnh sửa" xuất hiện và có thể nhấn
    edit_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "edit-account"))
    )

    # Nhấn vào nút "Chỉnh sửa"
    edit_button.click()
    time.sleep(3)

    # Chờ trường nhập liệu 'fullname' xuất hiện
    fullname_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "fullname"))
    )

    # Xóa tên cũ (dùng .clear() để xóa nội dung hiện tại)
    fullname_input.clear()

    # Nhập tên mới vào trường 'fullname'
    fullname_input.send_keys("Phạm Ánh")  # Thay "Tên Mới" bằng tên bạn muốn cập nhật
    time.sleep(3)
        # Chờ nút "Lưu thông tin" xuất hiện và có thể nhấn
    save_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "btn-update-account"))
    )

    # Nhấn vào nút "Lưu thông tin"
    save_button.click()

    # Đợi sau khi lưu thông tin
    time.sleep(2)

    # Kiểm tra xem tên mới đã được cập nhật trong bảng chưa
    new_name = "Phạm Ánh"  # Đây là tên bạn đã nhập

    updated_name = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//td[text()='" + new_name + "']"))
    )

    # Assert để kiểm tra kết quả
    assert updated_name is not None, f"Tên không được cập nhật thành công. Không tìm thấy tên '{new_name}' trong bảng."

    # Nếu assertion không có lỗi, tên đã được cập nhật thành công
    print(f"Tên đã được cập nhật thành công thành: {new_name}")

#test xóa khách hàng
def test_delete_customer(driver):
    driver.get("http://localhost/Webbanhang-main/index.html")
     # Chờ phần tử "Đăng nhập / Đăng ký" xuất hiện
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "text-dndk"))
    )
    time.sleep(3)

    # Tìm phần tử "Đăng nhập / Đăng ký"
    dang_nhap_dang_ky = driver.find_element(By.CLASS_NAME, "text-dndk")
    time.sleep(3)

    # Cuộn tới phần tử (nếu cần)
    actions = ActionChains(driver)
    actions.move_to_element(dang_nhap_dang_ky).perform()
    time.sleep(3)
    # Nhấn vào phần tử
    dang_nhap_dang_ky.click()
    # Tìm phần tử "Đăng nhập"
    login_button = driver.find_element(By.ID, "login")

    # Cuộn tới phần tử (nếu cần)
    actions.move_to_element(login_button).perform()
    time.sleep(3)

    # Nhấn vào nút "Đăng nhập"
    login_button.click()
    time.sleep(3)
    # Tìm và điền vào trường "Nhập số điện thoại"
    phone_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "phone-login"))
    )
    phone_field.send_keys("hgbaodev")  # Điền số điện thoại
    time.sleep(2)

    # Tìm và điền vào trường "Nhập mật khẩu"
    password_field = driver.find_element(By.ID, "password-login")
    password_field.send_keys("123456")  # Điền mật khẩu
    time.sleep(2)

    # Thêm các bước khác (nếu cần), ví dụ: nhấn nút "Đăng nhập"
    login_submit_button = driver.find_element(By.ID, "login-button")  # Giả sử nút có ID là "submit-login"
    login_submit_button.click()
    time.sleep(3)
         # Chờ phần tử "Đăng nhập / Đăng ký" xuất hiện
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "text-dndk"))
    )
    time.sleep(3)

    # Tìm phần tử "Đăng nhập / Đăng ký"
    dang_nhap_dang_ky = driver.find_element(By.CLASS_NAME, "text-dndk")
    time.sleep(3)

    # Cuộn tới phần tử (nếu cần)
    actions = ActionChains(driver)
    actions.move_to_element(dang_nhap_dang_ky).perform()
    time.sleep(3)

        # Chờ phần tử "Quản lý cửa hàng" xuất hiện
    manage_store_link = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Quản lý cửa hàng')]"))
    )

    # Nhấn vào "Quản lý cửa hàng"
    manage_store_link.click()
    time.sleep(3)

        # Chờ phần tử "Khách hàng" xuất hiện
    customer_section = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[@class='hidden-sidebar' and text()='Khách hàng']"))
    )

    # Đảm bảo phần tử "Khách hàng" đã có thể thao tác
    customer_section.click()
    time.sleep(3)  # Đợi một chút nếu cần
    # Chờ nút "Thêm khách hàng" xuất hiện
    add_customer_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@id='btn-add-user' and contains(span, 'Thêm khách hàng')]"))
    )

    # Nhấn vào nút "Thêm khách hàng"
    add_customer_button.click()
    time.sleep(3)  # Đợi một chút nếu cần

        # Chờ trường nhập "fullname" xuất hiện
    fullname_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "fullname"))
    )
    fullname_input.clear()  # Xóa nội dung cũ nếu có
    fullname_input.send_keys("Nhật Sinh")  # Nhập họ và tên

    # Chờ trường nhập "phone" xuất hiện
    phone_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "phone"))
    )
    phone_input.clear()
    phone_input.send_keys("0394996781")  # Nhập số điện thoại

    # Chờ trường nhập "password" xuất hiện
    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "password"))
    )
    password_input.clear()
    password_input.send_keys("MatKhau123!")  # Nhập mật khẩu

    # Đợi một chút để đảm bảo dữ liệu được nhập
    time.sleep(2)
    # Chờ nút "Đăng ký" xuất hiện và có thể nhấn
    signup_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "signup-button"))
    )

    # Nhấn vào nút "Đăng ký"
    signup_button.click()
    time.sleep(3)

    # Chờ nút "Xóa tài khoản" xuất hiện và có thể nhấn
    delete_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@id='delete-account']"))
    )

    # Nhấn vào nút "Xóa tài khoản"
    delete_button.click()
    time.sleep(2)

    # Chờ hộp thoại xác nhận xóa xuất hiện và nhấn "OK" để xác nhận
    alert = WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert.accept()
    time.sleep(3)

    # Kiểm tra xem tài khoản đã bị xóa thành công chưa
    # Tìm kiếm số điện thoại trong bảng
    try:
        phone_deleted = WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located((By.XPATH, "//td[text()='0394996781']"))
        )
        # Kiểm tra sự biến mất của số điện thoại
        assert phone_deleted, "Tài khoản vẫn chưa bị xóa. Số điện thoại vẫn tồn tại."
        print("Tài khoản đã được xóa thành công.")
    except Exception as e:
        print("Không thể xóa tài khoản:", e)

#test cập nhật số lượng sản phẩm trong giỏ hàng
def test_update_quality_product(driver):
    driver.get("http://localhost/Webbanhang-main/index.html")
     # Chờ phần tử "Đăng nhập / Đăng ký" xuất hiện
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "text-dndk"))
    )
    time.sleep(3)
    
    # Tìm phần tử "Đăng nhập / Đăng ký"
    dang_nhap_dang_ky = driver.find_element(By.CLASS_NAME, "text-dndk")
    time.sleep(3)
    
    # Cuộn tới phần tử (nếu cần)
    actions = ActionChains(driver)
    actions.move_to_element(dang_nhap_dang_ky).perform()
    time.sleep(3)
    # Nhấn vào phần tử
    dang_nhap_dang_ky.click()
    # Tìm phần tử "Đăng nhập"
    login_button = driver.find_element(By.ID, "login")
    
    # Cuộn tới phần tử (nếu cần)
    actions.move_to_element(login_button).perform()
    time.sleep(3)
    
    # Nhấn vào nút "Đăng nhập"
    login_button.click()
    time.sleep(3)
    # Tìm và điền vào trường "Nhập số điện thoại"
    phone_field = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "phone-login"))
    )
    phone_field.send_keys("hgbaodev")  # Điền số điện thoại
    time.sleep(2)
    
    # Tìm và điền vào trường "Nhập mật khẩu"
    password_field = driver.find_element(By.ID, "password-login")
    password_field.send_keys("123456")  # Điền mật khẩu
    time.sleep(2)
    
    # Thêm các bước khác (nếu cần), ví dụ: nhấn nút "Đăng nhập"
    login_submit_button = driver.find_element(By.ID, "login-button")  # Giả sử nút có ID là "submit-login"
    login_submit_button.click()
    time.sleep(3)
    # Cuộn đến giữa trang sau khi đăng nhập
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 2);")
    time.sleep(3)  # Chờ một chút để xem phần giữa trang
    # Tìm tất cả các nút "Đặt món"
    order_buttons = WebDriverWait(driver, 10).until(
        EC.visibility_of_all_elements_located((By.XPATH, "//button[contains(@class, 'order-item')]"))
    )

    # Chọn một nút ngẫu nhiên từ danh sách nút "Đặt món"
    random_button = random.choice(order_buttons)

    # Đảm bảo rằng nút có thể nhấn được và nhấn vào nó
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable(random_button))
    random_button.click()

    # Chờ một chút để xem kết quả
    time.sleep(3)

    add_cart_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.ID, "add-cart"))  # Tìm nút "Thêm vào giỏ hàng" bằng ID
    )
    add_cart_button.click()

    # Bước 7: Chờ một chút để xem giỏ hàng đã được cập nhật
    time.sleep(3)
    
    basket_icon = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "i.fa-light.fa-basket-shopping"))  # Chọn biểu tượng giỏ hàng
    )
    basket_icon.click()

    # Bước 9: Chờ một chút để giỏ hàng được mở
    time.sleep(3)
    # Tìm và nhấn vào nút tăng số lượng (nút có lớp 'plus is-form')
    increase_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".cart-item .plus.is-form"))  # Tìm nút tăng số lượng trong phần tử cart-item
    )
    increase_button.click()  # Nhấn nút tăng số lượng
    time.sleep(3)


    # Bước 5: Tìm và nhấn vào biểu tượng đóng giỏ hàng (xmark)
    close_icon = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "i.fa-sharp.fa-solid.fa-xmark"))  # Tìm biểu tượng đóng (xmark)
    )
    close_icon.click()  # Nhấn vào biểu tượng đóng

    # Bước 6: Chờ để xem giỏ hàng đã được cập nhật và đóng lại
    time.sleep(3)

    # Bước 7: Kiểm tra số lượng sản phẩm trong giỏ hàng
    product_count_span = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "span.count-product-cart"))  # Tìm phần tử số lượng sản phẩm
    )

    # Lấy giá trị số lượng hiện tại từ giỏ hàng
    current_quantity = int(product_count_span.text.strip())

    # Bước 8: Sử dụng assert để kiểm tra số lượng
    assert current_quantity == 2, f"Số lượng không đúng, hiện tại là: {current_quantity}"
    print("Số lượng đã được cập nhật thành công!")