const { thanhtoanpage, showProductCart, showProductBuyNow, xulyDathang } = require('../js/checkout.js');

describe('Checkout Page Tests', () => {

  beforeEach(() => {
    // Set up DOM elements before each test case.
    document.body.innerHTML = `
      <div class="checkout-page">
        <div class="date-order"></div>
        <div class="total-bill-order"></div>
        <div class="priceFlx"></div>
        <div class="pick-date"></div>
        <div class="complete-checkout-btn"></div>
      </div>`;
    // Mock localStorage methods if needed
    global.localStorage = {
      getItem: jest.fn(() => '{"currentuser": {"cart": []}}'),
      setItem: jest.fn()
    };
  });

  test('should show correct product and total price when choosing "payment in cart" option', () => {
    // Arrange
    const mockOption = 1; // Payment in cart
    const mockProduct = { soluong: 2, price: 50000 }; // Mock product data
    const mockGetCartTotal = jest.fn(() => 100000); // Mock getCartTotal function

    // Mock external functions
    global.getCartTotal = mockGetCartTotal;

    // Act
    thanhtoanpage(mockOption, mockProduct); // Call the function
    
    // Assert
    const totalBillOrder = document.querySelector('.total-bill-order');
    expect(totalBillOrder.innerHTML).toContain("Tiền hàng"); // Check if the total bill is displayed
    expect(totalBillOrder.innerHTML).toContain("Phí vận chuyển"); // Ensure shipping fee is displayed
    expect(document.querySelector('#checkout-cart-total').innerText).toBe('100,000 đ'); // Final total price should include PHIVANCHUYEN
  });

  test('should handle date selection properly', () => {
    // Arrange
    const mockOption = 1; // Payment in cart
    const mockProduct = { soluong: 2, price: 50000 };

    // Act
    thanhtoanpage(mockOption, mockProduct); // Set up the page

    // Simulate a click event on the "Ngày mai" date
    const pickDateElements = document.getElementsByClassName('pick-date');
    pickDateElements[1].click(); // Click on "Ngày mai"

    // Assert
    expect(pickDateElements[1].classList.contains('active')).toBe(true); // Ensure the "Ngày mai" is active
    expect(pickDateElements[0].classList.contains('active')).toBe(false); // Previous active class should be removed
  });

  test('should calculate total correctly for "Buy Now" option', () => {
    // Arrange
    const mockOption = 2; // Buy Now
    const mockProduct = { soluong: 3, price: 50000 }; // 3 items at 50,000 each
    const mockGetCartTotal = jest.fn(() => 0); // Ensure cart total is zero for Buy Now case

    // Act
    thanhtoanpage(mockOption, mockProduct); // Set up the page

    // Assert
    const totalBillOrder = document.querySelector('.total-bill-order');
    expect(totalBillOrder.innerHTML).toContain("Tiền hàng");
    expect(totalBillOrder.innerHTML).toContain("Phí vận chuyển");
    expect(document.querySelector('#checkout-cart-total').innerText).toBe('150,000 đ'); // 3 * 50,000 + PHIVANCHUYEN
  });

  test('should handle "Place Order" action', () => {
    // Arrange
    const mockProduct = { soluong: 1, price: 50000 };
    document.querySelector('.complete-checkout-btn').click = jest.fn();

    // Mock external functions
    const mockXulyDathang = jest.fn();
    global.xulyDathang = mockXulyDathang;

    // Act
    xulyDathang(mockProduct); // Trigger the order process

    // Assert
    expect(mockXulyDathang).toHaveBeenCalled(); // Ensure that the place order function was triggered
  });

  test('should handle missing required fields in order processing', () => {
    // Arrange
    const mockProduct = { soluong: 1, price: 50000 };

    // Mock missing user data
    document.querySelector("#tennguoinhan").value = "";
    document.querySelector("#sdtnhan").value = "";
    document.querySelector("#diachinhan").value = "";

    const toastMock = jest.fn();
    global.toast = toastMock;

    // Act
    xulyDathang(mockProduct); // Try to place an order with missing fields

    // Assert
    expect(toastMock).toHaveBeenCalledWith({
      title: 'Chú ý',
      message: 'Vui lòng nhập đầy đủ thông tin !',
      type: 'warning',
      duration: 4000
    }); // Ensure that a toast warning appears for missing data
  });

});

