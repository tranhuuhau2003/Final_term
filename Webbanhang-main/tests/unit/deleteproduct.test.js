/**
 * @jest-environment jsdom
 */

// Giả lập các phương thức DOM cần thiết và localStorage
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
        getItem: jest.fn((key) => store[key] || null), // Lấy giá trị từ localStorage
        setItem: jest.fn((key, value) => store[key] = value.toString()), // Lưu giá trị vào localStorage
        clear: jest.fn(() => store = {}), // Xóa tất cả dữ liệu trong localStorage
        removeItem: jest.fn((key) => delete store[key]) // Xóa một mục khỏi localStorage
    };
})();

Object.defineProperty(window, 'localStorage', { value: localStorageMock });

// Giả lập các hàm updateCartTotal và định dạng giá
global.updateCartTotal = jest.fn();
global.vnd = jest.fn((price) => `${price}₫`);

// Giả lập các hàm getProduct và getCartTotal vì chúng được sử dụng trong showCart
global.getProduct = jest.fn((item) => ({
    id: item.id,
    title: `Product ${item.id}`,
    price: item.price,
    note: item.note,
    soluong: item.soluong,
}));

global.getCartTotal = jest.fn(() => 1000);

// Định nghĩa hàm để kiểm tra (sao chép mã của hàm deleteCartItem)
function deleteCartItem(id, el) {
    let cartParent = el.closest('li'); // Cách tìm phần tử cha của danh sách một cách chắc chắn
    cartParent.remove();
    let currentUser = JSON.parse(localStorage.getItem('currentuser'));
    let vitri = currentUser.cart.findIndex(item => item.id === id);
    currentUser.cart.splice(vitri, 1);

    // Nếu giỏ hàng rỗng, hiển thị thông báo giỏ hàng rỗng và vô hiệu hóa nút thanh toán
    if (currentUser.cart.length === 0) {
        document.querySelector('.gio-hang-trong').style.display = 'flex';
        document.querySelector('button.thanh-toan').classList.add('disabled');
    }
    localStorage.setItem('currentuser', JSON.stringify(currentUser));
    updateCartTotal();
}

// Các bài kiểm thử
describe('deleteCartItem function', () => {
    beforeEach(() => {
        document.body.innerHTML = initialHTML; // Đặt lại cấu trúc HTML trước mỗi bài kiểm thử
        jest.clearAllMocks();
        // Giả lập dữ liệu giỏ hàng ban đầu trong localStorage
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

        // Tạo một phần tử danh sách cho giỏ hàng có nút xóa
        const cartItem = document.createElement('li');
        cartItem.appendChild(deleteButton);
        document.querySelector('.cart-list').appendChild(cartItem);

        // Nhấn nút xóa
        deleteButton.click();

        const updatedCart = JSON.parse(localStorage.getItem('currentuser')).cart;
        expect(updatedCart).toEqual([{ id: 2, price: 200, note: 'Note 2', soluong: 2 }]);
        expect(updateCartTotal).toHaveBeenCalled();
    });

    test('should display empty cart message and disable checkout button if cart is empty', () => {
        // Thiết lập giỏ hàng ban đầu với chỉ một mặt hàng
        localStorage.setItem('currentuser', JSON.stringify({ cart: [{ id: 1, price: 100, note: 'Note 1', soluong: 1 }] }));
        
        const deleteButton = document.createElement('button');
        deleteButton.onclick = () => deleteCartItem(1, deleteButton);

        // Tạo một phần tử danh sách cho giỏ hàng có nút xóa
        const cartItem = document.createElement('li');
        cartItem.appendChild(deleteButton);
        document.querySelector('.cart-list').appendChild(cartItem);

        // Nhấn nút xóa
        deleteButton.click();

        // Kiểm tra rằng thông báo giỏ hàng rỗng được hiển thị và nút thanh toán bị vô hiệu hóa
        expect(document.querySelector('.gio-hang-trong').style.display).toBe('flex');
        expect(document.querySelector('button.thanh-toan').classList.contains('disabled')).toBe(true);
    });
});
