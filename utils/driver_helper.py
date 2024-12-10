from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def init_driver():
    """
    Khởi tạo WebDriver với profile Chrome được định trước.
    """
    profile_path = "C:\\Users\\user\\AppData\\Local\\Google\\Chrome\\User Data"
    profile_directory = "Default"  # Đây là profile mà bạn muốn sử dụng (ví dụ: "Default", "Profile 1",...)

    options = Options()
    options.add_argument(f"user-data-dir={profile_path}")  # Chỉ định thư mục chứa profile
    options.add_argument(f"profile-directory={profile_directory}")  # Chỉ định tên thư mục profile

    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    return driver

def close_driver(driver):
    """
    Đóng WebDriver sau khi sử dụng.
    """
    driver.quit()
