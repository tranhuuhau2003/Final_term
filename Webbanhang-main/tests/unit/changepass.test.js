// Mock các hàm toàn cục và các phần tử DOM
global.toast = jest.fn();
document.body.innerHTML = `
    <input id="password-cur-info" type="password">
    <input id="password-after-info" type="password">
    <input id="password-comfirm-info" type="password">
    <div class="password-cur-info-error"></div>
    <div class="password-after-info-error"></div>
    <div class="password-after-comfirm-error"></div>
`;

function changePassword() {
    let currentUser = JSON.parse(localStorage.getItem("currentuser"));
    let passwordCur = document.getElementById('password-cur-info');
    let passwordAfter = document.getElementById('password-after-info');
    let passwordConfirm = document.getElementById('password-comfirm-info');
    let check = true;
    if (passwordCur.value.length == 0) {
        document.querySelector('.password-cur-info-error').innerHTML = 'Vui lòng nhập mật khẩu hiện tại';
        check = false;
    } else {
        document.querySelector('.password-cur-info-error').innerHTML = '';
    }

    if (passwordAfter.value.length == 0) {
        document.querySelector('.password-after-info-error').innerHTML = 'Vui lòn nhập mật khẩu mới';
        check = false;
    } else {
        document.querySelector('.password-after-info-error').innerHTML = '';
    }

    if (passwordConfirm.value.length == 0) {
        document.querySelector('.password-after-comfirm-error').innerHTML = 'Vui lòng nhập mật khẩu xác nhận';
        check = false;
    } else {
        document.querySelector('.password-after-comfirm-error').innerHTML = '';
    }

    if (check == true) {
        if (passwordCur.value.length > 0) {
            if (passwordCur.value == currentUser.password) {
                document.querySelector('.password-cur-info-error').innerHTML = '';
                if (passwordAfter.value.length > 0) {
                    if (passwordAfter.value.length < 6) {
                        document.querySelector('.password-after-info-error').innerHTML = 'Vui lòng nhập mật khẩu mới có số  kí tự lớn hơn bằng 6';
                    } else {
                        document.querySelector('.password-after-info-error').innerHTML = '';
                        if (passwordConfirm.value.length > 0) {
                            if (passwordConfirm.value == passwordAfter.value) {
                                document.querySelector('.password-after-comfirm-error').innerHTML = '';
                                currentUser.password = passwordAfter.value;
                                localStorage.setItem('currentuser', JSON.stringify(currentUser));
                                let userChange = JSON.parse(localStorage.getItem('currentuser'));
                                let accounts = JSON.parse(localStorage.getItem('accounts'));
                                let accountChange = accounts.find(acc => {
                                    return acc.phone = userChange.phone;
                                })
                                accountChange.password = userChange.password;
                                localStorage.setItem('accounts', JSON.stringify(accounts));
                                toast({ title: 'Thành công', message: 'Đổi mật khẩu thành công !', type: 'success', duration: 3000 });
                            } else {
                                document.querySelector('.password-after-comfirm-error').innerHTML = 'Mật khẩu bạn nhập không trùng khớp';
                            }
                        } else {
                            document.querySelector('.password-after-comfirm-error').innerHTML = 'Vui lòng xác nhận mật khẩu';
                        }
                    }
                } else {
                    document.querySelector('.password-after-info-error').innerHTML = 'Vui lòng nhập mật khẩu mới';
                }
            } else {
                document.querySelector('.password-cur-info-error').innerHTML = 'Bạn đã nhập sai mật khẩu hiện tại';
            }
        }
    }
}

// Các test case
describe('changePassword', () => {
    beforeEach(() => {
        // Mock dữ liệu localStorage
        localStorage.setItem("currentuser", JSON.stringify({ password: 'oldpassword', phone: '1234567890' }));
        localStorage.setItem('accounts', JSON.stringify([{ phone: '1234567890', password: 'oldpassword' }]));
    });

    afterEach(() => {
        jest.clearAllMocks();
        document.querySelector('.password-cur-info-error').innerHTML = '';
        document.querySelector('.password-after-info-error').innerHTML = '';
        document.querySelector('.password-after-comfirm-error').innerHTML = '';
    });

    test('Hiển thị lỗi nếu mật khẩu hiện tại để trống', () => {
        document.getElementById('password-cur-info').value = '';
        document.getElementById('password-after-info').value = 'newpassword';
        document.getElementById('password-comfirm-info').value = 'newpassword';

        changePassword();

        expect(document.querySelector('.password-cur-info-error').innerHTML).toBe('Vui lòng nhập mật khẩu hiện tại');
    });

    test('Hiển thị lỗi nếu mật khẩu mới để trống', () => {
        document.getElementById('password-cur-info').value = 'oldpassword';
        document.getElementById('password-after-info').value = '';
        document.getElementById('password-comfirm-info').value = 'newpassword';

        changePassword();

        expect(document.querySelector('.password-after-info-error').innerHTML).toBe('Vui lòn nhập mật khẩu mới');
    });

    test('Hiển thị lỗi nếu mật khẩu xác nhận để trống', () => {
        document.getElementById('password-cur-info').value = 'oldpassword';
        document.getElementById('password-after-info').value = 'newpassword';
        document.getElementById('password-comfirm-info').value = '';

        changePassword();

        expect(document.querySelector('.password-after-comfirm-error').innerHTML).toBe('Vui lòng nhập mật khẩu xác nhận');
    });

    test('Hiển thị lỗi nếu mật khẩu hiện tại không đúng', () => {
        document.getElementById('password-cur-info').value = 'wrongpassword';
        document.getElementById('password-after-info').value = 'newpassword';
        document.getElementById('password-comfirm-info').value = 'newpassword';

        changePassword();

        expect(document.querySelector('.password-cur-info-error').innerHTML).toBe('Bạn đã nhập sai mật khẩu hiện tại');
    });

    test('Hiển thị lỗi nếu mật khẩu mới có ít hơn 6 ký tự', () => {
        document.getElementById('password-cur-info').value = 'oldpassword';
        document.getElementById('password-after-info').value = 'short';
        document.getElementById('password-comfirm-info').value = 'short';

        changePassword();

        expect(document.querySelector('.password-after-info-error').innerHTML).toBe('Vui lòng nhập mật khẩu mới có số  kí tự lớn hơn bằng 6');
    });

    test('Hiển thị lỗi nếu mật khẩu xác nhận không trùng khớp với mật khẩu mới', () => {
        document.getElementById('password-cur-info').value = 'oldpassword';
        document.getElementById('password-after-info').value = 'newpassword';
        document.getElementById('password-comfirm-info').value = 'mismatchpassword';

        changePassword();

        expect(document.querySelector('.password-after-comfirm-error').innerHTML).toBe('Mật khẩu bạn nhập không trùng khớp');
    });

    test('Đổi mật khẩu thành công khi tất cả điều kiện đúng', () => {
        document.getElementById('password-cur-info').value = 'oldpassword';
        document.getElementById('password-after-info').value = 'newpassword';
        document.getElementById('password-comfirm-info').value = 'newpassword';

        changePassword();

        expect(localStorage.getItem('currentuser')).toBe(JSON.stringify({ password: 'newpassword', phone: '1234567890' }));
        expect(localStorage.getItem('accounts')).toBe(JSON.stringify([{ phone: '1234567890', password: 'newpassword' }]));
        expect(global.toast).toHaveBeenCalledWith({
            title: 'Thành công', 
            message: 'Đổi mật khẩu thành công !', 
            type: 'success', 
            duration: 3000 
        });
    });
});
