// Mock localStorage for testing purposes
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

// Replace global localStorage with the mock
global.localStorage = new LocalStorageMock();

// Mock functions used in the login process
global.toast = jest.fn();
global.closeModal = jest.fn();
global.kiemtradangnhap = jest.fn();
global.checkAdmin = jest.fn();
global.updateAmount = jest.fn();

// Define the loginButton event listener function here
function loginEventListener(event) {
    event.preventDefault();
    let phonelog = document.getElementById('phone-login').value;
    let passlog = document.getElementById('password-login').value;
// danh sách tài khoản được lấy từ local
    let accounts = JSON.parse(localStorage.getItem('accounts'));

    if (phonelog.length == 0) {
        document.querySelector('.form-message.phonelog').innerHTML = 'Vui lòng nhập vào số điện thoại';
    } else if (phonelog.length != 10) {
        document.querySelector('.form-message.phonelog').innerHTML = 'Vui lòng nhập vào số điện thoại 10 số';
        document.getElementById('phone-login').value = '';
    } else {
        document.querySelector('.form-message.phonelog').innerHTML = '';
    }

    if (passlog.length == 0) {
        document.querySelector('.form-message-check-login').innerHTML = 'Vui lòng nhập mật khẩu';
    } else if (passlog.length < 6) {
        document.querySelector('.form-message-check-login').innerHTML = 'Vui lòng nhập mật khẩu lớn hơn 6 kí tự';
        document.getElementById('password-login').value = '';
    } else {
        document.querySelector('.form-message-check-login').innerHTML = '';
    }

    if (phonelog && passlog) {
        let vitri = accounts.findIndex(item => item.phone == phonelog);
        if (vitri == -1) {
            toast({ title: 'Error', message: 'Tài khoản của bạn không tồn tại', type: 'error', duration: 3000 });
        } else if (accounts[vitri].password == passlog) {
            if (accounts[vitri].status == 0) {
                toast({ title: 'Warning', message: 'Tài khoản của bạn đã bị khóa', type: 'warning', duration: 3000 });
            } else {
                localStorage.setItem('currentuser', JSON.stringify(accounts[vitri]));
                toast({ title: 'Success', message: 'Đăng nhập thành công', type: 'success', duration: 3000 });
                closeModal();
                kiemtradangnhap();
                checkAdmin();
                updateAmount();
            }
        } else {
            toast({ title: 'Warning', message: 'Sai mật khẩu', type: 'warning', duration: 3000 });
        }
    }
}

// Mock event
const event = {
    preventDefault: jest.fn()
};

// Set up DOM elements mock
document.body.innerHTML = `
    <input id="phone-login" type="text" value="" />
    <input id="password-login" type="password" value="" />
    <div class="form-message phonelog"></div>
    <div class="form-message-check-login"></div>
`;

// Test cases
describe('Login Event Listener Function', () => {

    afterEach(() => {
        localStorage.clear();
        document.getElementById('phone-login').value = '';
        document.getElementById('password-login').value = '';
        document.querySelector('.form-message.phonelog').innerHTML = '';
        document.querySelector('.form-message-check-login').innerHTML = '';
        jest.clearAllMocks();
    });

    test('Phone number field is empty', () => {
        document.getElementById('phone-login').value = '';
        document.getElementById('password-login').value = '123456';
        // lưu trữ dữ liệu dưới dạng khóa key accounts
        localStorage.setItem('accounts', JSON.stringify([{ phone: '1234567890', password: '123456', status: 1 }]));
        
        loginEventListener(event);
        expect(document.querySelector('.form-message.phonelog').innerHTML).toBe('Vui lòng nhập vào số điện thoại');
    });

    test('Account does not exist', () => {
        document.getElementById('phone-login').value = '1234567890';
        document.getElementById('password-login').value = '123456';
        localStorage.setItem('accounts', JSON.stringify([{ phone: '0987654321', password: '123456', status: 1 }]));
        
        loginEventListener(event);

        expect(toast).toHaveBeenCalledWith({ title: 'Error', message: 'Tài khoản của bạn không tồn tại', type: 'error', duration: 3000 });
    });

    test('Account is locked', () => {
        document.getElementById('phone-login').value = '1234567890';
        document.getElementById('password-login').value = '123456';
        localStorage.setItem('accounts', JSON.stringify([{ phone: '1234567890', password: '123456', status: 0 }]));
        
        loginEventListener(event);

        expect(toast).toHaveBeenCalledWith({ title: 'Warning', message: 'Tài khoản của bạn đã bị khóa', type: 'warning', duration: 3000 });
    });

    test('Successful login', () => {
        document.getElementById('phone-login').value = '1234567890';
        document.getElementById('password-login').value = '123456';
        localStorage.setItem('accounts', JSON.stringify([{ phone: '1234567890', password: '123456', status: 1 }]));
        
        loginEventListener(event);

        expect(localStorage.getItem('currentuser')).toEqual(JSON.stringify({ phone: '1234567890', password: '123456', status: 1 }));
        expect(toast).toHaveBeenCalledWith({ title: 'Success', message: 'Đăng nhập thành công', type: 'success', duration: 3000 });
    });

    test('Incorrect password', () => {
        document.getElementById('phone-login').value = '1234567890';
        document.getElementById('password-login').value = 'wrongpassword';
        localStorage.setItem('accounts', JSON.stringify([{ phone: '1234567890', password: '123456', status: 1 }]));
        
        loginEventListener(event);

        expect(toast).toHaveBeenCalledWith({ title: 'Warning', message: 'Sai mật khẩu', type: 'warning', duration: 3000 });
    });
});
