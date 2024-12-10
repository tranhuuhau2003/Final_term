// Mock localStorage for testing
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

// Mock global functions and DOM elements
global.scrollTo = jest.fn();
global.localStorage = new LocalStorageMock();
global.kiemtradangnhap = jest.fn();
global.toast = jest.fn();
global.emailIsValid = jest.fn();

document.body.innerHTML = `
    <div id="trangchu"></div>
    <div id="order-history"></div>
    <div id="account-user"></div>
    <input id="infoname" value="John Doe" />
    <input id="infoemail" value="" />
    <input id="infoaddress" value="123 Street" />
    <div class="inforemail-error"></div>
`;

// Functions under test
function myAccount() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
    document.getElementById('trangchu')?.classList.add('hide');
    document.getElementById('order-history')?.classList.remove('open');
    document.getElementById('account-user')?.classList.add('open');
    userInfo?.();
}

function changeInformation() {
    const accounts = JSON.parse(localStorage.getItem('accounts') || '[]');
    const user = JSON.parse(localStorage.getItem('currentuser') || '{}');

    const infoname = document.getElementById('infoname');
    const infoemail = document.getElementById('infoemail');
    const infoaddress = document.getElementById('infoaddress');

    if (infoname && infoname.value) {
        user.fullname = infoname.value;
    }

    if (infoemail && infoemail.value) {
        if (!emailIsValid(infoemail.value)) {
            document.querySelector('.inforemail-error').innerHTML = 'Vui lòng nhập lại email!';
            infoemail.value = '';
        } else {
            user.email = infoemail.value;
        }
    }

    if (infoaddress && infoaddress.value) {
        user.address = infoaddress.value;
    }

    const index = accounts.findIndex(item => item.phone === user.phone);
    if (index !== -1) {
        Object.assign(accounts[index], user);
    }

    localStorage.setItem('currentuser', JSON.stringify(user));
    localStorage.setItem('accounts', JSON.stringify(accounts));
    kiemtradangnhap();
    toast({ title: 'Success', message: 'Cập nhật thông tin thành công !', type: 'success', duration: 3000 });
}

// Test cases
describe('myAccount()', () => {
    test('Should update the DOM elements and call userInfo', () => {
        global.userInfo = jest.fn();
        myAccount();
        expect(document.getElementById('trangchu').classList.contains('hide')).toBe(true);
        expect(document.getElementById('order-history').classList.contains('open')).toBe(false);
        expect(document.getElementById('account-user').classList.contains('open')).toBe(true);
        expect(global.userInfo).toHaveBeenCalled();
    });
});

describe('changeInformation()', () => {
    afterEach(() => {
        localStorage.clear();
        jest.clearAllMocks();
    });

    test('Should update user information successfully', () => {
        localStorage.setItem('accounts', JSON.stringify([{ phone: '1234567890', fullname: 'Old Name', email: 'old@example.com', address: 'Old Address' }]));
        localStorage.setItem('currentuser', JSON.stringify({ phone: '1234567890', fullname: 'Old Name', email: 'old@example.com', address: 'Old Address' }));

        document.getElementById('infoname').value = 'New Name';
        document.getElementById('infoemail').value = 'new@example.com';
        document.getElementById('infoaddress').value = 'New Address';
        global.emailIsValid.mockReturnValue(true);

        changeInformation();

        const updatedAccounts = JSON.parse(localStorage.getItem('accounts'));
        const updatedUser = JSON.parse(localStorage.getItem('currentuser'));

        expect(updatedAccounts[0].fullname).toBe('New Name');
        expect(updatedAccounts[0].email).toBe('new@example.com');
        expect(updatedAccounts[0].address).toBe('New Address');
        expect(updatedUser.fullname).toBe('New Name');
        expect(updatedUser.email).toBe('new@example.com');
        expect(updatedUser.address).toBe('New Address');
        expect(toast).toHaveBeenCalledWith({ title: 'Success', message: 'Cập nhật thông tin thành công !', type: 'success', duration: 3000 });
    });

    test('Should show email validation error', () => {
        document.getElementById('infoemail').value = 'invalid-email';
        global.emailIsValid.mockReturnValue(false);

        changeInformation();

        expect(document.querySelector('.inforemail-error').innerHTML).toBe('Vui lòng nhập lại email!');
        expect(document.getElementById('infoemail').value).toBe('');
    });

    test('Should not update address if input is empty', () => {
        localStorage.setItem('accounts', JSON.stringify([{ phone: '1234567890', address: 'Old Address' }]));
        localStorage.setItem('currentuser', JSON.stringify({ phone: '1234567890', address: 'Old Address' }));

        document.getElementById('infoaddress').value = '';

        changeInformation();

        const updatedAccounts = JSON.parse(localStorage.getItem('accounts'));
        expect(updatedAccounts[0].address).toBe('Old Address');
    });

    test('Should only update name if other inputs are empty', () => {
        localStorage.setItem('accounts', JSON.stringify([{ phone: '1234567890', fullname: 'Old Name', email: 'old@example.com', address: 'Old Address' }]));
        localStorage.setItem('currentuser', JSON.stringify({ phone: '1234567890', fullname: 'Old Name', email: 'old@example.com', address: 'Old Address' }));

        document.getElementById('infoname').value = 'Updated Name';
        document.getElementById('infoemail').value = '';
        document.getElementById('infoaddress').value = '';

        changeInformation();

        const updatedAccounts = JSON.parse(localStorage.getItem('accounts'));
        const updatedUser = JSON.parse(localStorage.getItem('currentuser'));

        expect(updatedAccounts[0].fullname).toBe('Updated Name');
        expect(updatedAccounts[0].email).toBe('old@example.com');
        expect(updatedAccounts[0].address).toBe('Old Address');
        expect(updatedUser.fullname).toBe('Updated Name');
    });
});
test('Should allow login with updated information', () => {
    // Giả lập dữ liệu ban đầu
    localStorage.setItem('accounts', JSON.stringify([{ phone: '1234567890', password: 'oldpassword', fullname: 'Old Name', email: 'old@example.com', address: 'Old Address' }]));
    localStorage.setItem('currentuser', JSON.stringify({ phone: '1234567890', fullname: 'Old Name', email: 'old@example.com', address: 'Old Address' }));

    // Cập nhật thông tin người dùng
    document.getElementById('infoname').value = 'New Name';
    document.getElementById('infoemail').value = 'new@example.com';
    document.getElementById('infoaddress').value = 'New Address';
    global.emailIsValid.mockReturnValue(true);
    changeInformation();

    // Giả lập đăng nhập bằng thông tin mới
    const updatedAccounts = JSON.parse(localStorage.getItem('accounts'));
    const updatedUser = JSON.parse(localStorage.getItem('currentuser'));

    const phone = updatedUser.phone; // Giữ nguyên số điện thoại
    const password = 'oldpassword'; // Giữ nguyên mật khẩu

    const account = updatedAccounts.find(acc => acc.phone === phone && acc.password === password);

    // Kiểm tra thông tin đăng nhập
    expect(account).not.toBeUndefined();
    expect(account.fullname).toBe('New Name');
    expect(account.email).toBe('new@example.com');
    expect(account.address).toBe('New Address');
});
