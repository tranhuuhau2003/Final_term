/**
 * @jest-environment jsdom
 */

// Mô phỏng các phương thức localStorage, updateAmount, closeModal và các hàm cần thiết khác
class LocalStorageMock {
    constructor() {
        this.store = {}; // Khởi tạo đối tượng lưu trữ
    }

    clear() {
        this.store = {}; // Xóa tất cả dữ liệu trong localStorage
    }

    getItem(key) {
        return this.store[key] || null; // Lấy dữ liệu theo khóa, nếu không có thì trả về null
    }

    setItem(key, value) {
        this.store[key] = value; // Lưu dữ liệu vào localStorage
    }

    removeItem(key) {
        delete this.store[key]; // Xóa một mục dữ liệu theo khóa
    }
}

global.localStorage = new LocalStorageMock(); // Gán mô phỏng localStorage vào đối tượng global
global.updateAmount = jest.fn(); // Mô phỏng hàm updateAmount
global.closeModal = jest.fn(); // Mô phỏng hàm closeModal
global.toast = jest.fn(); // Mô phỏng hàm toast

// Định nghĩa hàm addCart
function addCart(index) {
    let currentuser = localStorage.getItem('currentuser') ? JSON.parse(localStorage.getItem('currentuser')) : { cart: [] }; // Lấy thông tin người dùng từ localStorage
    let soluong = document.querySelector('.input-qty').value; // Lấy số lượng sản phẩm
    let popupDetailNote = document.querySelector('#popup-detail-note').value; // Lấy ghi chú sản phẩm
    let note = popupDetailNote == "" ? "Không có ghi chú" : popupDetailNote; // Nếu không có ghi chú thì mặc định là "Không có ghi chú"
    let productcart = {
        id: index, // ID sản phẩm
        soluong: parseInt(soluong), // Số lượng sản phẩm
        note: note // Ghi chú sản phẩm
    }
    let vitri = currentuser.cart.findIndex(item => item.id == productcart.id); // Tìm vị trí sản phẩm trong giỏ hàng
    if (vitri == -1) {
        currentuser.cart.push(productcart); // Nếu chưa có sản phẩm trong giỏ hàng thì thêm sản phẩm mới
    } else {
        currentuser.cart[vitri].soluong = parseInt(currentuser.cart[vitri].soluong) + parseInt(productcart.soluong); // Cập nhật số lượng sản phẩm nếu sản phẩm đã có trong giỏ hàng
    }
    localStorage.setItem('currentuser', JSON.stringify(currentuser)); // Lưu giỏ hàng vào localStorage
    updateAmount(); // Cập nhật số lượng giỏ hàng
    closeModal(); // Đóng cửa sổ pop-up
}

// Thiết lập các phần tử DOM cho việc kiểm thử
document.body.innerHTML = `
    <input class="input-qty" type="number" value="1" />
    <textarea id="popup-detail-note"></textarea>
    <button class="button-dat"></button>
`;

let infoProduct = { id: 1 }; // Thông tin sản phẩm

let productbtn = document.querySelector('.button-dat');
productbtn.addEventListener('click', (e) => {
    if (localStorage.getItem('currentuser')) {
        addCart(infoProduct.id); // Gọi hàm addCart nếu người dùng đã đăng nhập
    } else {
        toast({ title: 'Warning', message: 'Chưa đăng nhập tài khoản !', type: 'warning', duration: 3000 }); // Hiển thị thông báo cảnh báo nếu người dùng chưa đăng nhập
    }
});

// Các trường hợp kiểm thử
describe('Hàm addCart', () => {

    beforeEach(() => {
        localStorage.clear(); // Xóa dữ liệu trong localStorage trước mỗi kiểm thử
        jest.clearAllMocks(); // Xóa các lời gọi giả lập
        document.querySelector('.input-qty').value = '1'; // Đặt lại giá trị số lượng
        document.getElementById('popup-detail-note').value = ''; // Đặt lại giá trị ghi chú
    });

    test('nên thêm sản phẩm mới vào giỏ hàng', () => {
        addCart(1); // Gọi hàm addCart để thêm sản phẩm

        const currentUser = JSON.parse(localStorage.getItem('currentuser')); // Lấy dữ liệu giỏ hàng từ localStorage
        expect(currentUser.cart.length).toBe(1); // Kiểm tra xem giỏ hàng có một sản phẩm không
        expect(currentUser.cart[0].id).toBe(1); // Kiểm tra ID của sản phẩm trong giỏ hàng
        expect(currentUser.cart[0].soluong).toBe(1); // Kiểm tra số lượng sản phẩm
        expect(currentUser.cart[0].note).toBe("Không có ghi chú"); // Kiểm tra ghi chú của sản phẩm
        expect(updateAmount).toHaveBeenCalled(); // Kiểm tra xem hàm updateAmount có được gọi không
        expect(closeModal).toHaveBeenCalled(); // Kiểm tra xem hàm closeModal có được gọi không
    });

    test('nên cập nhật số lượng nếu sản phẩm đã có trong giỏ hàng', () => {
        localStorage.setItem('currentuser', JSON.stringify({
            cart: [{ id: 1, soluong: 1, note: "Không có ghi chú" }]
        }));

        document.querySelector('.input-qty').value = '2'; // Đặt lại số lượng
        addCart(1); // Gọi hàm addCart

        const currentUser = JSON.parse(localStorage.getItem('currentuser')); // Lấy dữ liệu giỏ hàng
        expect(currentUser.cart.length).toBe(1); // Kiểm tra số lượng sản phẩm trong giỏ hàng
        expect(currentUser.cart[0].id).toBe(1); // Kiểm tra ID của sản phẩm
        expect(currentUser.cart[0].soluong).toBe(3); // Kiểm tra số lượng sản phẩm sau khi cập nhật
        expect(currentUser.cart[0].note).toBe("Không có ghi chú"); // Kiểm tra ghi chú
        expect(updateAmount).toHaveBeenCalled(); // Kiểm tra xem hàm updateAmount có được gọi không
        expect(closeModal).toHaveBeenCalled(); // Kiểm tra xem hàm closeModal có được gọi không
    });

    test('nên thêm sản phẩm mới với ghi chú vào giỏ hàng', () => {
        document.querySelector('.input-qty').value = '1'; // Đặt lại số lượng
        document.getElementById('popup-detail-note').value = 'This is a note'; // Đặt ghi chú
        addCart(2); // Gọi hàm addCart

        const currentUser = JSON.parse(localStorage.getItem('currentuser')); // Lấy dữ liệu giỏ hàng
        expect(currentUser.cart.length).toBe(1); // Kiểm tra số lượng sản phẩm
        expect(currentUser.cart[0].id).toBe(2); // Kiểm tra ID sản phẩm
        expect(currentUser.cart[0].soluong).toBe(1); // Kiểm tra số lượng sản phẩm
        expect(currentUser.cart[0].note).toBe("This is a note"); // Kiểm tra ghi chú
        expect(updateAmount).toHaveBeenCalled(); // Kiểm tra xem hàm updateAmount có được gọi không
        expect(closeModal).toHaveBeenCalled(); // Kiểm tra xem hàm closeModal có được gọi không
    });

    test('nên gọi addCart khi nhấn nút và người dùng đã đăng nhập', () => {
        localStorage.setItem('currentuser', JSON.stringify({ cart: [] }));

        // Mô phỏng việc nhấn nút
        productbtn.click();

        // Lấy giỏ hàng sau khi nhấn nút
        const currentUser = JSON.parse(localStorage.getItem('currentuser'));
        expect(currentUser.cart.length).toBe(1); // Kiểm tra số lượng sản phẩm trong giỏ hàng
        expect(currentUser.cart[0].id).toBe(1); // Kiểm tra ID sản phẩm
        expect(updateAmount).toHaveBeenCalled(); // Kiểm tra xem hàm updateAmount có được gọi không
        expect(closeModal).toHaveBeenCalled(); // Kiểm tra xem hàm closeModal có được gọi không
    });

    test('nên hiển thị thông báo cảnh báo khi nhấn nút và người dùng chưa đăng nhập', () => {
        localStorage.removeItem('currentuser'); // Xóa người dùng khỏi localStorage
        productbtn.click(); // Mô phỏng việc nhấn nút

        expect(toast).toHaveBeenCalledWith({ title: 'Warning', message: 'Chưa đăng nhập tài khoản !', type: 'warning', duration: 3000 }); // Kiểm tra xem thông báo cảnh báo có được hiển thị không
    });
});
