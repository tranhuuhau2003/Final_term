/**
 * @jest-environment jsdom
 */

// Mock the localStorage
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
global.formatDate = jest.fn(date => new Date(date).toLocaleDateString());
global.editAccount = jest.fn();
global.deleteAcount = jest.fn();
global.alert = jest.fn();

// Define the functions
function showUserArr(arr) {
    let accountHtml = '';
    if (arr.length == 0) {
        accountHtml = `<td colspan="5">Không có dữ liệu</td>`
    } else {
        arr.forEach((account, index) => {
            let tinhtrang = account.status == 0 ? `<span class="status-no-complete">Bị khóa</span>` : `<span class="status-complete">Hoạt động</span>`;
            accountHtml += ` <tr>
            <td>${index + 1}</td>
            <td>${account.fullname}</td>
            <td>${account.phone}</td>
            <td>${formatDate(account.join)}</td>
            <td>${tinhtrang}</td>
            <td class="control control-table">
            <button class="btn-edit" id="edit-account" onclick='editAccount(${account.phone})' ><i class="fa-light fa-pen-to-square"></i></button>
            <button class="btn-delete" id="delete-account" onclick="deleteAcount(${index})"><i class="fa-regular fa-trash"></i></button>
            </td>
        </tr>`
        })
    }
    document.getElementById('show-user').innerHTML = accountHtml;
}

function showUser() {
    let tinhTrang = parseInt(document.getElementById("tinh-trang-user").value);
    let ct = document.getElementById("form-search-user").value;
    let timeStart = document.getElementById("time-start-user").value;
    let timeEnd = document.getElementById("time-end-user").value;

    if (timeEnd < timeStart && timeEnd != "" && timeStart != "") {
        alert("Lựa chọn thời gian sai !");
        return;
    }

    let accounts = localStorage.getItem("accounts") ? JSON.parse(localStorage.getItem("accounts")).filter(item => item.userType == 0) : [];
    let result = tinhTrang == 2 ? accounts : accounts.filter(item => item.status == tinhTrang);

    result = ct == "" ? result : result.filter((item) => {
        return (item.fullname.toLowerCase().includes(ct.toLowerCase()) || item.phone.toString().toLowerCase().includes(ct.toLowerCase()));
    });

    if (timeStart != "" && timeEnd == "") {
        result = result.filter((item) => {
            return new Date(item.join) >= new Date(timeStart).setHours(0, 0, 0);
        });
    } else if (timeStart == "" && timeEnd != "") {
        result = result.filter((item) => {
            return new Date(item.join) <= new Date(timeEnd).setHours(23, 59, 59);
        });
    } else if (timeStart != "" && timeEnd != "") {
        result = result.filter((item) => {
            return (new Date(item.join) >= new Date(timeStart).setHours(0, 0, 0) && new Date(item.join) <= new Date(timeEnd).setHours(23, 59, 59)
            );
        });
    }
    showUserArr(result);
}

// Set up DOM elements
document.body.innerHTML = `
    <select id="tinh-trang-user">
        <option value="2">Tất cả</option>
        <option value="0">Bị khóa</option>
        <option value="1">Hoạt động</option>
    </select>
    <input type="text" id="form-search-user" />
    <input type="date" id="time-start-user" />
    <input type="date" id="time-end-user" />
    <table id="show-user"></table>
`;

// Test cases
describe('showUserArr Function', () => {

    afterEach(() => {
        document.getElementById('show-user').innerHTML = '';
    });

    test('should display "Không có dữ liệu" when array is empty', () => {
        showUserArr([]);

        expect(document.getElementById('show-user').innerHTML).toContain('Không có dữ liệu');
    });

    test('should display users data when array is not empty', () => {
        const accounts = [
            { fullname: 'John Doe', phone: '1234567890', join: '2023-01-01', status: 1 },
            { fullname: 'Jane Smith', phone: '0987654321', join: '2022-12-01', status: 0 }
        ];

        showUserArr(accounts);

        expect(document.getElementById('show-user').innerHTML).toContain('John Doe');
        expect(document.getElementById('show-user').innerHTML).toContain('1234567890');
        expect(document.getElementById('show-user').innerHTML).toContain('Hoạt động');
        expect(document.getElementById('show-user').innerHTML).toContain('Jane Smith');
        expect(document.getElementById('show-user').innerHTML).toContain('0987654321');
        expect(document.getElementById('show-user').innerHTML).toContain('Bị khóa');
    });
});

describe('showUser Function', () => {

    beforeEach(() => {
        localStorage.clear();
        document.getElementById('tinh-trang-user').value = '2';
        document.getElementById('form-search-user').value = '';
        document.getElementById('time-start-user').value = '';
        document.getElementById('time-end-user').value = '';
    });

    test('should display an alert when timeEnd is before timeStart', () => {
        document.getElementById('time-start-user').value = '2023-01-01';
        document.getElementById('time-end-user').value = '2022-12-01';

        showUser();

        expect(alert).toHaveBeenCalledWith('Lựa chọn thời gian sai !');
    });

    test('should display all users when "Tất cả" is selected', () => {
        localStorage.setItem("accounts", JSON.stringify([
            { fullname: 'John Doe', phone: '1234567890', join: '2023-01-01', status: 1, userType: 0 },
            { fullname: 'Jane Smith', phone: '0987654321', join: '2022-12-01', status: 0, userType: 0 }
        ]));

        showUser();

        expect(document.getElementById('show-user').innerHTML).toContain('John Doe');
        expect(document.getElementById('show-user').innerHTML).toContain('Jane Smith');
    });

    test('should filter users by status when a specific status is selected', () => {
        document.getElementById('tinh-trang-user').value = '1';
        localStorage.setItem("accounts", JSON.stringify([
            { fullname: 'John Doe', phone: '1234567890', join: '2023-01-01', status: 1, userType: 0 },
            { fullname: 'Jane Smith', phone: '0987654321', join: '2022-12-01', status: 0, userType: 0 }
        ]));

        showUser();

        expect(document.getElementById('show-user').innerHTML).toContain('John Doe');
        expect(document.getElementById('show-user').innerHTML).not.toContain('Jane Smith');
    });

    test('should filter users by search input', () => {
        document.getElementById('form-search-user').value = 'Jane';
        localStorage.setItem("accounts", JSON.stringify([
            { fullname: 'John Doe', phone: '1234567890', join: '2023-01-01', status: 1, userType: 0 },
            { fullname: 'Jane Smith', phone: '0987654321', join: '2022-12-01', status: 0, userType: 0 }
        ]));

        showUser();

        expect(document.getElementById('show-user').innerHTML).toContain('Jane Smith');
        expect(document.getElementById('show-user').innerHTML).not.toContain('John Doe');
    });
    test('should filter users by join date range', () => {
        document.getElementById('time-start-user').value = '2022-01-01';
        document.getElementById('time-end-user').value = '2022-31-12';
        localStorage.setItem("accounts", JSON.stringify([
            { fullname: 'John Doe', phone: '1234567890', join: '2022-06-15', status: 1, userType: 0 },
            { fullname: 'Jane Smith', phone: '0987654321', join: '2023-01-10', status: 0, userType: 0 }
        ]));

        showUser();

        expect(document.getElementById('show-user').innerHTML).toContain('John Doe');
        expect(document.getElementById('show-user').innerHTML).not.toContain('Jane Smith');
    });

    test('should filter users by join date from a specific start date', () => {
        document.getElementById('time-start-user').value = '2022-01-01';
        document.getElementById('time-end-user').value = '';
        localStorage.setItem("accounts", JSON.stringify([
            { fullname: 'John Doe', phone: '1234567890', join: '2022-06-15', status: 1, userType: 0 },
            { fullname: 'Jane Smith', phone: '0987654321', join: '2021-12-31', status: 0, userType: 0 }
        ]));

        showUser();

        expect(document.getElementById('show-user').innerHTML).toContain('John Doe');
        expect(document.getElementById('show-user').innerHTML).not.toContain('Jane Smith');
    });

    test('should filter users by join date up to a specific end date', () => {
        document.getElementById('time-start-user').value = '';
        document.getElementById('time-end-user').value = '2022-31-12';
        localStorage.setItem("accounts", JSON.stringify([
            { fullname: 'John Doe', phone: '1234567890', join: '2022-06-15', status: 1, userType: 0 },
            { fullname: 'Jane Smith', phone: '0987654321', join: '2023-01-10', status: 0, userType: 0 }
        ]));

        showUser();

        expect(document.getElementById('show-user').innerHTML).toContain('John Doe');
        expect(document.getElementById('show-user').innerHTML).not.toContain('Jane Smith');
    });
test('should filter users by join date range', () => {
    document.getElementById('time-start-user').value = '2022-01-01';
    document.getElementById('time-end-user').value = '2022-12-31';
    localStorage.setItem("accounts", JSON.stringify([
        { fullname: 'John Doe', phone: '1234567890', join: '2022-06-15', status: 1, userType: 0 },
        { fullname: 'Jane Smith', phone: '0987654321', join: '2023-01-10', status: 0, userType: 0 }
    ]));

    showUser();

    expect(document.getElementById('show-user').innerHTML).toContain('John Doe');
    expect(document.getElementById('show-user').innerHTML).not.toContain('Jane Smith');
});


});


