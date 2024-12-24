import datetime
import time

from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
import pytest
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from Final_term.utils.helper import click_element, fill_input, check_toast_message, check_error_message, login, \
    add_customer, logout, logout_admin, add_to_cart, add_multiple_to_cart, update_product_quantity_in_cart, \
    check_cart_quantity, scroll_to_element, navigate_to_product_statistics, navigate_to_product_dashboard, \
    go_to_next_page, calculate_orders_revenue
from Final_term.utils.driver_helper import init_driver, close_driver  # Import từ driver_helper
from selenium.webdriver.common.by import By
from datetime import datetime


@pytest.fixture
def driver():
    driver = init_driver()
    yield driver
    close_driver(driver)



class TestDashBoard:


    def test_dashboard(self, driver):
        try:
            navigate_to_product_dashboard(driver, "hgbaodev", "123456")

            amount_user = int(driver.find_element(By.ID, "amount-user").text.strip())
            amount_product = int(driver.find_element(By.ID, "amount-product").text.strip())
            doanh_thu = driver.find_element(By.ID, "doanh-thu").text.strip()
            print(f"Dashboard: Users: {amount_user}, Products: {amount_product}, Revenue: {doanh_thu}")

            click_element(driver, By.XPATH, "//div[@class='hidden-sidebar' and text()='Sản phẩm']")
            time.sleep(1)
            total_products_counted = 0
            while True:
                total_products_counted += len(driver.find_elements(By.CLASS_NAME, "list"))
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                if not go_to_next_page(driver):
                    break
            print(f"Tổng số sản phẩm đếm được: {total_products_counted}")
            assert total_products_counted == amount_product, f"Không khớp: {amount_product} vs {total_products_counted}"

            click_element(driver, By.XPATH, "//div[@class='hidden-sidebar' and text()='Khách hàng']")
            time.sleep(3)
            total_customers_counted = len(driver.find_elements(By.XPATH, "//tbody[@id='show-user']/tr[td]"))
            print(f"Tổng số khách hàng đếm được: {total_customers_counted}")
            assert total_customers_counted == amount_user, f"Không khớp: {amount_user} vs {total_customers_counted}"

            click_element(driver, By.XPATH, "//li[contains(@class, 'sidebar-list-item') and .//div[@class='hidden-sidebar'][contains(text(), 'Đơn hàng')]]")
            time.sleep(4)
            total_orders_revenue = calculate_orders_revenue(driver)
            print(f"Tổng doanh thu từ các đơn hàng: {total_orders_revenue}₫")
            dashboard_revenue = int(doanh_thu.replace(".", "").replace("₫", "").strip())
            assert total_orders_revenue == dashboard_revenue, f"Không khớp: {total_orders_revenue}₫ vs {dashboard_revenue}₫"

        finally:
            logout_admin(driver)

