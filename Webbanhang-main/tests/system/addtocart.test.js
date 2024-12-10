/**
 * @jest-environment jsdom
 */

// Mock the localStorage, updateAmount, closeModal, and other necessary functions
class LocalStorageMock {
    constructor() {
        this.store = {};
    }

    clear() {
        this.store = {};
    }

    getItem(key) {
        return this.store[key] || null;
    }

    setItem(key, value) {
        this.store[key] = value;
    }

    removeItem(key) {
        delete this.store[key];
    }
}

global.localStorage = new LocalStorageMock();
global.updateAmount = jest.fn();
global.closeModal = jest.fn();
global.toast = jest.fn();

// Define the function
function addCart(index) {
    let currentuser = localStorage.getItem('currentuser') ? JSON.parse(localStorage.getItem('currentuser')) : { cart: [] };
    let soluong = document.querySelector('.input-qty').value;
    let popupDetailNote = document.querySelector('#popup-detail-note').value;
    let note = popupDetailNote == "" ? "Không có ghi chú" : popupDetailNote;
    let productcart = {
        id: index,
        soluong: parseInt(soluong),
        note: note
    }
    let vitri = currentuser.cart.findIndex(item => item.id == productcart.id);
    if (vitri == -1) {
        currentuser.cart.push(productcart);
    } else {
        currentuser.cart[vitri].soluong = parseInt(currentuser.cart[vitri].soluong) + parseInt(productcart.soluong);
    }
    localStorage.setItem('currentuser', JSON.stringify(currentuser));
    updateAmount();
    closeModal();
}

// Set up DOM elements for testing
document.body.innerHTML = `
    <input class="input-qty" type="number" value="1" />
    <textarea id="popup-detail-note"></textarea>
    <button class="button-dat"></button>
`;

let infoProduct = { id: 1 };

let productbtn = document.querySelector('.button-dat');
productbtn.addEventListener('click', (e) => {
    if (localStorage.getItem('currentuser')) {
        addCart(infoProduct.id);
    } else {
        toast({ title: 'Warning', message: 'Chưa đăng nhập tài khoản !', type: 'warning', duration: 3000 });
    }
});

// Test cases
describe('addCart Function', () => {

    beforeEach(() => {
        localStorage.clear();
        jest.clearAllMocks();
        document.querySelector('.input-qty').value = '1';
        document.getElementById('popup-detail-note').value = '';
    });

    test('should add a new product to the cart', () => {
        addCart(1);

        const currentUser = JSON.parse(localStorage.getItem('currentuser'));
        expect(currentUser.cart.length).toBe(1);
        expect(currentUser.cart[0].id).toBe(1);
        expect(currentUser.cart[0].soluong).toBe(1);
        expect(currentUser.cart[0].note).toBe("Không có ghi chú");
        expect(updateAmount).toHaveBeenCalled();
        expect(closeModal).toHaveBeenCalled();
    });

    test('should update the quantity if the product is already in the cart', () => {
        localStorage.setItem('currentuser', JSON.stringify({
            cart: [{ id: 1, soluong: 1, note: "Không có ghi chú" }]
        }));

        document.querySelector('.input-qty').value = '2';
        addCart(1);

        const currentUser = JSON.parse(localStorage.getItem('currentuser'));
        expect(currentUser.cart.length).toBe(1);
        expect(currentUser.cart[0].id).toBe(1);
        expect(currentUser.cart[0].soluong).toBe(3);
        expect(currentUser.cart[0].note).toBe("Không có ghi chú");
        expect(updateAmount).toHaveBeenCalled();
        expect(closeModal).toHaveBeenCalled();
    });

    test('should add a new product with a note to the cart', () => {
        document.querySelector('.input-qty').value = '1';
        document.getElementById('popup-detail-note').value = 'This is a note';
        addCart(2);

        const currentUser = JSON.parse(localStorage.getItem('currentuser'));
        expect(currentUser.cart.length).toBe(1);
        expect(currentUser.cart[0].id).toBe(2);
        expect(currentUser.cart[0].soluong).toBe(1);
        expect(currentUser.cart[0].note).toBe("This is a note");
        expect(updateAmount).toHaveBeenCalled();
        expect(closeModal).toHaveBeenCalled();
    });

    test('should call addCart when button is clicked and user is logged in', () => {
        localStorage.setItem('currentuser', JSON.stringify({ cart: [] }));

        // Simulate button click
        productbtn.click();

        // Retrieve the current user's cart after button click
        const currentUser = JSON.parse(localStorage.getItem('currentuser'));
        expect(currentUser.cart.length).toBe(1);
        expect(currentUser.cart[0].id).toBe(1);
        expect(updateAmount).toHaveBeenCalled();
        expect(closeModal).toHaveBeenCalled();
    });

    test('should show warning toast when button is clicked and user is not logged in', () => {
        localStorage.removeItem('currentuser');
        productbtn.click();

        expect(toast).toHaveBeenCalledWith({ title: 'Warning', message: 'Chưa đăng nhập tài khoản !', type: 'warning', duration: 3000 });
    });
});
