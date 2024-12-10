/**
 * @jest-environment jsdom
 */

// Mock functions for DOM manipulation and localStorage
function updateCartTotal() { /* Mock implementation */ }
function saveAmountCart() { /* Mock implementation */ }
function vnd(value) { return `${value} VND`; }  // Mock currency formatter
function getProduct(item) {
    return { id: item.id, title: "Product", price: 1000, soluong: 1, note: "Product note" };
}

// Set up a mock for localStorage
beforeEach(() => {
    const user = {
        currentuser: {
            cart: [
                { id: 1, title: 'Product 1', price: 1000, soluong: 1, note: 'Note 1' },
                { id: 2, title: 'Product 2', price: 2000, soluong: 1, note: 'Note 2' }
            ]
        }
    };
    localStorage.setItem('currentuser', JSON.stringify(user.currentuser));
    document.body.innerHTML = `
        <div class="gio-hang-trong" style="display: none"></div>
        <button class="thanh-toan"></button>
        <ul class="cart-list">
            <li class="cart-item" data-id="1">
                <div class="cart-item-info">
                    <p class="cart-item-title">Product 1</p>
                    <span class="cart-item-price price" data-price="1000">1000 VND</span>
                </div>
                <p class="product-note"><i class="fa-light fa-pencil"></i><span>Product note</span></p>
                <div class="cart-item-control">
                    <button class="cart-item-delete" onclick="deleteCartItem(1, this)">Xóa</button>
                </div>
            </li>
            <li class="cart-item" data-id="2">
                <div class="cart-item-info">
                    <p class="cart-item-title">Product 2</p>
                    <span class="cart-item-price price" data-price="2000">2000 VND</span>
                </div>
                <p class="product-note"><i class="fa-light fa-pencil"></i><span>Product note</span></p>
                <div class="cart-item-control">
                    <button class="cart-item-delete" onclick="deleteCartItem(2, this)">Xóa</button>
                </div>
            </li>
        </ul>
    `;
});

// Test cases for deleteCartItem function
describe('deleteCartItem Function', () => {
    test('should remove the product from cart and DOM', () => {
        const deleteButton = document.querySelector('.cart-item-delete');
        deleteCartItem(1, deleteButton);  // Simulate delete for product with id 1
        
        // Check that the product is removed from the DOM
        const cartItems = document.querySelectorAll('.cart-item');
        expect(cartItems.length).toBe(1);
        expect(cartItems[0].dataset.id).toBe('2'); // Only product with id 2 should remain

        // Check that localStorage is updated correctly
        const currentUser = JSON.parse(localStorage.getItem('currentuser'));
        expect(currentUser.cart.length).toBe(1);
        expect(currentUser.cart[0].id).toBe(2); // Product with id 2 should be left in the cart
    });

    test('should show empty cart message and disable checkout button when cart is empty', () => {
        const deleteButton = document.querySelectorAll('.cart-item-delete')[0];  // Delete product with id 1
        deleteCartItem(1, deleteButton);

        // Simulate delete for product with id 2
        const deleteButton2 = document.querySelectorAll('.cart-item-delete')[0];
        deleteCartItem(2, deleteButton2);

        // Check that the cart is empty
        const cartItems = document.querySelectorAll('.cart-item');
        expect(cartItems.length).toBe(0);  // No items should remain

        // Check that the empty cart message is shown
        const emptyCartMessage = document.querySelector('.gio-hang-trong');
        expect(emptyCartMessage.style.display).toBe('flex');

        // Check that the checkout button is disabled
        const checkoutButton = document.querySelector('.thanh-toan');
        expect(checkoutButton.classList.contains('disabled')).toBe(true);
    });

    test('should update localStorage correctly after deleting an item', () => {
        const deleteButton = document.querySelector('.cart-item-delete');
        deleteCartItem(1, deleteButton);  // Simulate delete for product with id 1
        
        const currentUser = JSON.parse(localStorage.getItem('currentuser'));
        expect(currentUser.cart.length).toBe(1);
        expect(currentUser.cart[0].id).toBe(2); // Product with id 2 should remain
    });
});
