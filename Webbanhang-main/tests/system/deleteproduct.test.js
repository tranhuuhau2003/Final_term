/**
 * @jest-environment jsdom
 */

// Mock the necessary DOM methods and localStorage
const initialHTML = `
    <ul class="cart-list"></ul>
    <div class="gio-hang-trong" style="display: none;"></div>
    <button class="thanh-toan disabled"></button>
    <span class="text-price"></span>
`;

document.body.innerHTML = initialHTML;

const localStorageMock = (() => {
    let store = {};
    return {
        getItem: jest.fn((key) => store[key] || null),
        setItem: jest.fn((key, value) => store[key] = value.toString()),
        clear: jest.fn(() => store = {}),
        removeItem: jest.fn((key) => delete store[key])
    };
})();

Object.defineProperty(window, 'localStorage', { value: localStorageMock });

// Mocking the updateCartTotal function and price formatting function
global.updateCartTotal = jest.fn();
global.vnd = jest.fn((price) => `${price}₫`);

// Mock the getProduct and getCartTotal functions as they are used in showCart
global.getProduct = jest.fn((item) => ({
    id: item.id,
    title: `Product ${item.id}`,
    price: item.price,
    note: item.note,
    soluong: item.soluong,
}));

global.getCartTotal = jest.fn(() => 1000);

// Define the function to test (copy the code for deleteCartItem)
function deleteCartItem(id, el) {
    let cartParent = el.closest('li'); // Robust way to find the parent list item
    cartParent.remove();
    let currentUser = JSON.parse(localStorage.getItem('currentuser'));
    let vitri = currentUser.cart.findIndex(item => item.id === id);
    currentUser.cart.splice(vitri, 1);

    // If cart is empty, show empty cart message and disable checkout button
    if (currentUser.cart.length === 0) {
        document.querySelector('.gio-hang-trong').style.display = 'flex';
        document.querySelector('button.thanh-toan').classList.add('disabled');
    }
    localStorage.setItem('currentuser', JSON.stringify(currentUser));
    updateCartTotal();
}

// Test Cases
describe('deleteCartItem function', () => {
    beforeEach(() => {
        document.body.innerHTML = initialHTML; // Reset the HTML structure before each test
        jest.clearAllMocks();
        // Mock initial cart data in localStorage
        localStorage.setItem('currentuser', JSON.stringify({
            cart: [
                { id: 1, price: 100, note: 'Note 1', soluong: 1 },
                { id: 2, price: 200, note: 'Note 2', soluong: 2 },
            ]
        }));
    });

    test('should remove the cart item and update localStorage', () => {
        const deleteButton = document.createElement('button');
        deleteButton.onclick = () => deleteCartItem(1, deleteButton);

        // Create a list item for the cart that includes the delete button
        const cartItem = document.createElement('li');
        cartItem.appendChild(deleteButton);
        document.querySelector('.cart-list').appendChild(cartItem);

        // Click the delete button
        deleteButton.click();

        const updatedCart = JSON.parse(localStorage.getItem('currentuser')).cart;
        expect(updatedCart).toEqual([{ id: 2, price: 200, note: 'Note 2', soluong: 2 }]);
        expect(updateCartTotal).toHaveBeenCalled();
    });

    test('should display empty cart message and disable checkout button if cart is empty', () => {
        // Set up an initial cart with only one item
        localStorage.setItem('currentuser', JSON.stringify({ cart: [{ id: 1, price: 100, note: 'Note 1', soluong: 1 }] }));
        
        const deleteButton = document.createElement('button');
        deleteButton.onclick = () => deleteCartItem(1, deleteButton);

        // Create a list item for the cart that includes the delete button
        const cartItem = document.createElement('li');
        cartItem.appendChild(deleteButton);
        document.querySelector('.cart-list').appendChild(cartItem);

        // Click the delete button
        deleteButton.click();

        // Check that the empty cart message is shown and the checkout button is disabled
        expect(document.querySelector('.gio-hang-trong').style.display).toBe('flex');
        expect(document.querySelector('button.thanh-toan').classList.contains('disabled')).toBe(true);
    });
});
