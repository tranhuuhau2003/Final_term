/**
 * @jest-environment jsdom
 */

// Giả lập các chức năng localStorage, toast, showUser, và signUpFormReset
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
global.toast = jest.fn();
global.showUser = jest.fn();
global.signUpFormReset = jest.fn();

// Định nghĩa các chức năng
function openCreateAccount() {
    document.querySelector(".signup").classList.add("open");
    document.querySelectorAll(".edit-account-e").forEach(item => {
        item.style.display = "none";
    });
    document.querySelectorAll(".add-account-e").forEach(item => {
        item.style.display = "block";
    });
}

document.body.innerHTML = `
    <div class="signup"></div>
    <div class="edit-account-e"></div>
    <div class="edit-account-e"></div>
    <div class="add-account-e"></div>
    <div class="add-account-e"></div>
    <form id="add-account">
        <input type="text" id="fullname" />
        <div class="form-message-name"></div>
        <input type="text" id="phone" />
        <div class="form-message-phone"></div>
        <input type="password" id="password" />
        <div class="form-message-password"></div>
        <button id="addAccount">Thêm Tài Khoản</button>
    </form>
`;

addAccount.addEventListener("click", (e) => {
    e.preventDefault();
    let fullNameUser = document.getElementById('fullname').value;
    let phoneUser = document.getElementById('phone').value;
    let passwordUser = document.getElementById('password').value;

    let fullNameIP = document.getElementById('fullname');
    let formMessageName = document.querySelector('.form-message-name');
    let formMessagePhone = document.querySelector('.form-message-phone');
    let formMessagePassword = document.querySelector('.form-message-password');

    if (fullNameUser.length == 0) {
        formMessageName.innerHTML = 'Vui lòng nhập họ và tên';
        fullNameIP.focus();
    } else if (fullNameUser.length < 3) {
        fullNameIP.value = '';
        formMessageName.innerHTML = 'Vui lòng nhập họ và tên lớn hơn 3 kí tự';
    }
    
    if (phoneUser.length == 0) {
        formMessagePhone.innerHTML = 'Vui lòng nhập vào số điện thoại';
    } else if (phoneUser.length != 10) {
        formMessagePhone.innerHTML = 'Vui lòng nhập vào số điện thoại 10 số';
        document.getElementById('phone').value = '';
    }
    
    if (passwordUser.length == 0) {
        formMessagePassword.innerHTML = 'Vui lòng nhập mật khẩu';
    } else if (passwordUser.length < 6) {
        formMessagePassword.innerHTML = 'Vui lòng nhập mật khẩu lớn hơn 6 kí tự';
        document.getElementById('password').value = '';
    }

    if (fullNameUser && phoneUser && passwordUser) {
        let user = {
            fullname: fullNameUser,
            phone: phoneUser,
            password: passwordUser,
            address: '',
            email: '',
            status: 1,
            join: new Date(),
            cart: [],
            userType: 0
        };
        let accounts = localStorage.getItem('accounts') ? JSON.parse(localStorage.getItem('accounts')) : [];
        let checkloop = accounts.some(account => {
            return account.phone == user.phone;
        });
        if (!checkloop) {
            accounts.push(user);
            localStorage.setItem('accounts', JSON.stringify(accounts));
            toast({ title: 'Thành công', message: 'Tạo thành công tài khoản !', type: 'success', duration: 3000 });
            document.querySelector(".signup").classList.remove("open");
            showUser();
            signUpFormReset();
        } else {
            toast({ title: 'Cảnh báo !', message: 'Tài khoản đã tồn tại !', type: 'error', duration: 3000 });
        }
    }
});

// Các test case
describe('Hàm openCreateAccount', () => {

    beforeEach(() => {
        // Reset các phần tử DOM trước mỗi bài kiểm tra
        document.querySelector(".signup").classList.remove("open");
        document.querySelectorAll(".edit-account-e").forEach(item => {
            item.style.display = "block";
        });
        document.querySelectorAll(".add-account-e").forEach(item => {
            item.style.display = "none";
        });
    });

    test('nên mở form tạo tài khoản', () => {
        openCreateAccount();

        // Kiểm tra nếu .signup có class 'open'
        expect(document.querySelector('.signup').classList.contains('open')).toBe(true);
    });

    test('nên hiển thị các phần tử thêm tài khoản', () => {
        openCreateAccount();

        // Kiểm tra nếu tất cả phần tử .add-account-e được hiển thị
        document.querySelectorAll('.add-account-e').forEach(item => {
            expect(item.style.display).toBe('block');
        });
    });
});

describe('Sự kiện lắng nghe addAccount', () => {

    beforeEach(() => {
        localStorage.clear();
        jest.clearAllMocks();
    });

    test('nên xác thực các trường nhập liệu', () => {
        document.getElementById('fullname').value = '';
        document.getElementById('phone').value = '';
        document.getElementById('password').value = '';

        addAccount.click();

        expect(document.querySelector('.form-message-phone').innerHTML).toBe('Vui lòng nhập vào số điện thoại');
        expect(document.querySelector('.form-message-password').innerHTML).toBe('Vui lòng nhập mật khẩu');
    });

    test('nên hiển thị thông báo lỗi cho các giá trị nhập không hợp lệ', () => {
        document.getElementById('fullname').value = 'Jo';
        document.getElementById('phone').value = '12345';
        document.getElementById('password').value = '123';

        addAccount.click();

        expect(document.querySelector('.form-message-name').innerHTML).toBe('Vui lòng nhập họ và tên lớn hơn 3 kí tự');
        expect(document.querySelector('.form-message-phone').innerHTML).toBe('Vui lòng nhập vào số điện thoại 10 số');
        expect(document.querySelector('.form-message-password').innerHTML).toBe('Vui lòng nhập mật khẩu lớn hơn 6 kí tự');
    });

    test('nên thêm một tài khoản mới nếu tất cả các trường nhập hợp lệ', () => {
        document.getElementById('fullname').value = 'John Doe';
        document.getElementById('phone').value = '1234567890';
        document.getElementById('password').value = 'password123';

        addAccount.click();

        const accounts = JSON.parse(localStorage.getItem('accounts'));
        expect(accounts.length).toBe(1);
        expect(accounts[0].fullname).toBe('John Doe');
        expect(accounts[0].phone).toBe('1234567890');
        expect(accounts[0].password).toBe('password123');
        expect(toast).toHaveBeenCalledWith({ title: 'Thành công', message: 'Tạo thành công tài khoản !', type: 'success', duration: 3000 });
        expect(showUser).toHaveBeenCalled();
        expect(signUpFormReset).toHaveBeenCalled();
    });

    test('nên không thêm tài khoản trùng lặp', () => {
        const existingAccounts = [
            { fullname: 'Jane Smith', phone: '0987654321', password: 'password123', userType: 0 }
        ];
        localStorage.setItem('accounts', JSON.stringify(existingAccounts));

        document.getElementById('fullname').value = 'Jane Smith';
        document.getElementById('phone').value = '0987654321';
        document.getElementById('password').value = 'password123';

        addAccount.click();

        const accounts = JSON.parse(localStorage.getItem('accounts'));
        expect(accounts.length).toBe(1);  // Vẫn chỉ có một tài khoản
        expect(accounts[0].phone).toBe('0987654321');
        expect(toast).toHaveBeenCalledWith({ title: 'Cảnh báo !', message: 'Tài khoản đã tồn tại !', type: 'error', duration: 3000 });
        expect(showUser).not.toHaveBeenCalled();
        expect(signUpFormReset).not.toHaveBeenCalled();
    });
});
