/**
 * @jest-environment jsdom
 */

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

describe('Hàm addCart', () => {

    beforeEach(() => {
        localStorage.clear();
        jest.clearAllMocks();
        document.querySelector('.input-qty').value = '1';
        document.getElementById('popup-detail-note').value = '';
    });

    test('thêm sản phẩm mới vào giỏ hàng', () => {
        console.log('------ Bắt đầu test: Thêm sản phẩm mới vào giỏ hàng ------');

        addCart(1);

        const currentUser = JSON.parse(localStorage.getItem('currentuser'));
        console.log('Giỏ hàng sau khi thêm sản phẩm mới:', currentUser.cart);

        expect(currentUser.cart.length).toBe(1);
        expect(currentUser.cart[0].id).toBe(1);
        expect(currentUser.cart[0].soluong).toBe(1);
        expect(currentUser.cart[0].note).toBe("Không có ghi chú");

        console.log('Kiểm tra hàm updateAmount đã được gọi:', updateAmount.mock.calls.length);
        expect(updateAmount).toHaveBeenCalled();
        expect(closeModal).toHaveBeenCalled();

        console.log('------ Kết thúc test: Thêm sản phẩm mới vào giỏ hàng ------\n');
    });

    test('cập nhật số lượng nếu sản phẩm đã có trong giỏ hàng', () => {
        console.log('------ Bắt đầu test: Cập nhật số lượng sản phẩm trong giỏ hàng ------');

        localStorage.setItem('currentuser', JSON.stringify({
            cart: [{ id: 1, soluong: 1, note: "Không có ghi chú" }]
        }));

        document.querySelector('.input-qty').value = '2';
        addCart(1);

        const currentUser = JSON.parse(localStorage.getItem('currentuser'));
        console.log('Giỏ hàng sau khi cập nhật số lượng:', currentUser.cart);

        expect(currentUser.cart.length).toBe(1);
        expect(currentUser.cart[0].id).toBe(1);
        expect(currentUser.cart[0].soluong).toBe(3);
        expect(currentUser.cart[0].note).toBe("Không có ghi chú");
        expect(updateAmount).toHaveBeenCalled();
        expect(closeModal).toHaveBeenCalled();

        console.log('------ Kết thúc test: Cập nhật số lượng sản phẩm trong giỏ hàng ------\n');
    });

    test('hiển thị thông báo cảnh báo khi nhấn nút và người dùng chưa đăng nhập', () => {
        console.log('------ Bắt đầu test: Hiển thị thông báo cảnh báo khi người dùng chưa đăng nhập ------');

        localStorage.removeItem('currentuser');
        productbtn.click();

        console.log('Kiểm tra thông báo toast:', toast.mock.calls);
        expect(toast).toHaveBeenCalledWith({ title: 'Warning', message: 'Chưa đăng nhập tài khoản !', type: 'warning', duration: 3000 });

        console.log('------ Kết thúc test: Hiển thị thông báo cảnh báo khi người dùng chưa đăng nhập ------\n');
    });

});
