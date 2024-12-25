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
global.closeModal = jest.fn();
global.kiemtradangnhap = jest.fn();
global.updateAmount = jest.fn();

const event = {
    preventDefault: jest.fn()
};

document.body.innerHTML = `
    <input id="fullname" type="text" value="" />
    <input id="phone" type="text" value="" />
    <input id="password" type="password" value="" />
    <input id="password_confirmation" type="password" value="" />
    <input id="checkbox-signup" type="checkbox" />
    <div class="form-message-name"></div>
    <div class="form-message-phone"></div>
    <div class="form-message-password"></div>
    <div class="form-message-password-confi"></div>
    <div class="form-message-checkbox"></div>
`;

const signupButton = {
    click: jest.fn(() => {
        const fullname = document.getElementById('fullname').value.trim();
        const phone = document.getElementById('phone').value.trim();
        const password = document.getElementById('password').value;
        const passwordConfirmation = document.getElementById('password_confirmation').value;
        const checkbox = document.getElementById('checkbox-signup').checked;

        const nameMessage = document.querySelector('.form-message-name');
        const phoneMessage = document.querySelector('.form-message-phone');
        const passwordMessage = document.querySelector('.form-message-password');
        const passwordConfiMessage = document.querySelector('.form-message-password-confi');
        const checkboxMessage = document.querySelector('.form-message-checkbox');

        nameMessage.innerHTML = '';
        phoneMessage.innerHTML = '';
        passwordMessage.innerHTML = '';
        passwordConfiMessage.innerHTML = '';
        checkboxMessage.innerHTML = '';

        if (!fullname) {
            nameMessage.innerHTML = 'Vui lòng nhập họ và tên';
            return;
        }

        if (fullname.length < 3) {
            nameMessage.innerHTML = 'Vui lòng nhập họ và tên lớn hơn 3 kí tự';
            return;
        }

        if (!phone) {
            phoneMessage.innerHTML = 'Vui lòng nhập vào số điện thoại';
            return;
        }

        if (phone.length !== 10 || !/^\d{10}$/.test(phone)) {
            phoneMessage.innerHTML = 'Vui lòng nhập vào số điện thoại 10 số';
            return;
        }

        if (!password) {
            passwordMessage.innerHTML = 'Vui lòng nhập mật khẩu';
            return;
        }

        if (password !== passwordConfirmation) {
            passwordConfiMessage.innerHTML = 'Mật khẩu không khớp';
            return;
        }

        if (!checkbox) {
            checkboxMessage.innerHTML = 'Vui lòng check đăng ký';
            return;
        }

        const accounts = JSON.parse(localStorage.getItem('accounts') || '[]');
        if (accounts.some(account => account.phone === phone)) {
            toast({
                title: 'Thất bại',
                message: 'Tài khoản đã tồn tại !',
                type: 'error',
                duration: 30000
            });
            return;
        }

        accounts.push({ fullname, phone, password });
        localStorage.setItem('accounts', JSON.stringify(accounts));
        toast({
            title: 'Thành công',
            message: 'Tạo thành công tài khoản !',
            type: 'success',
            duration: 30000
        });
    })
};
describe('Chức năng đăng ký', () => {
    afterEach(() => {
        localStorage.clear();
        jest.clearAllMocks();
        document.getElementById('fullname').value = '';
        document.getElementById('phone').value = '';
        document.getElementById('password').value = '';
        document.getElementById('password_confirmation').value = '';
        document.getElementById('checkbox-signup').checked = false;
    });

    test('Số điện thoại trống', () => {
        const testName = 'Số điện thoại trống';
        console.log(`Test: ${testName}`);
        document.getElementById('fullname').value = 'John Doe';
        signupButton.click();

        console.log('Đang kiểm tra: Thông báo lỗi cho số điện thoại trống');
        expect(document.querySelector('.form-message-phone').innerHTML).toBe('Vui lòng nhập vào số điện thoại');
    });

    test('Mật khẩu trống', () => {
        const testName = 'Mật khẩu trống';
        console.log(`Test: ${testName}`);
        document.getElementById('fullname').value = 'John Doe';
        document.getElementById('phone').value = '1234567890';
        signupButton.click();

        console.log('Đang kiểm tra: Thông báo lỗi cho mật khẩu trống');
        expect(document.querySelector('.form-message-password').innerHTML).toBe('Vui lòng nhập mật khẩu');
    });

    test('Mật khẩu không khớp với xác nhận mật khẩu', () => {
        const testName = 'Mật khẩu không khớp với xác nhận mật khẩu';
        console.log(`Test: ${testName}`);
        document.getElementById('fullname').value = 'John Doe';
        document.getElementById('phone').value = '1234567890';
        document.getElementById('password').value = 'password123';
        document.getElementById('password_confirmation').value = 'wrongpassword';
        signupButton.click();

        console.log('Đang kiểm tra: Thông báo lỗi cho mật khẩu không khớp');
        expect(document.querySelector('.form-message-password-confi').innerHTML).toBe('Mật khẩu không khớp');
    });

    test('Tài khoản đã tồn tại', () => {
        const testName = 'Tài khoản đã tồn tại';
        console.log(`Test: ${testName}`);
        localStorage.setItem('accounts', JSON.stringify([{ fullname: 'John Doe', phone: '1234567890', password: 'password123' }]));
        document.getElementById('fullname').value = 'Jane Smith';
        document.getElementById('phone').value = '1234567890';
        document.getElementById('password').value = 'password456';
        document.getElementById('password_confirmation').value = 'password456';
        document.getElementById('checkbox-signup').checked = true;
        signupButton.click();

        console.log('Đang kiểm tra: Thông báo lỗi khi tài khoản đã tồn tại');
        expect(toast).toHaveBeenCalledWith({ title: 'Thất bại', message: 'Tài khoản đã tồn tại !', type: 'error', duration: 30000 });
    });

    test('Đăng ký thành công', () => {
        const testName = 'Đăng ký thành công';
        console.log(`Test: ${testName}`);
        document.getElementById('fullname').value = 'John Doe';
        document.getElementById('phone').value = '1234567890';
        document.getElementById('password').value = 'password123';
        document.getElementById('password_confirmation').value = 'password123';
        document.getElementById('checkbox-signup').checked = true;

        signupButton.click();

        console.log('Đang kiểm tra: Dữ liệu tài khoản đã được lưu vào localStorage');
        const accounts = JSON.parse(localStorage.getItem('accounts'));
        expect(accounts).not.toBeNull();

        console.log('Đang kiểm tra: Tài khoản mới đã được thêm vào danh sách');
        expect(accounts).toEqual(
            expect.arrayContaining([
                expect.objectContaining({ phone: '1234567890' })
            ])
        );

        console.log('Đang kiểm tra: Thông báo thành công hiển thị đúng');
        expect(toast).toHaveBeenCalledWith({ title: 'Thành công', message: 'Tạo thành công tài khoản !', type: 'success', duration: 30000 });
    });
});
