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
global.showUserArr = jest.fn();
global.showUser = jest.fn();

// Define the function
function cancelSearchUser() {
    let accounts = localStorage.getItem("accounts") ? JSON.parse(localStorage.getItem("accounts")).filter(item => item.userType == 0) : [];
    showUserArr(accounts);
    document.getElementById("tinh-trang-user").value = 2;
    document.getElementById("form-search-user").value = "";
    document.getElementById("time-start-user").value = "";
    document.getElementById("time-end-user").value = "";
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
describe('cancelSearchUser Function', () => {

    beforeEach(() => {
        localStorage.clear();
        jest.clearAllMocks();
        localStorage.setItem("accounts", JSON.stringify([
            { fullname: 'John Doe', phone: '1234567890', join: '2023-01-01', status: 1, userType: 0 },
            { fullname: 'Jane Smith', phone: '0987654321', join: '2022-12-01', status: 0, userType: 0 }
        ]));
        document.getElementById("tinh-trang-user").value = '0';
        document.getElementById("form-search-user").value = 'John';
        document.getElementById("time-start-user").value = '2023-01-01';
        document.getElementById("time-end-user").value = '2023-01-31';
    });

    test('should reset all filters and show all accounts', () => {
        cancelSearchUser();

        expect(document.getElementById("tinh-trang-user").value).toBe('2');
        expect(document.getElementById("form-search-user").value).toBe('');
        expect(document.getElementById("time-start-user").value).toBe('');
        expect(document.getElementById("time-end-user").value).toBe('');
        expect(showUserArr).toHaveBeenCalledWith([
            { fullname: 'John Doe', phone: '1234567890', join: '2023-01-01', status: 1, userType: 0 },
            { fullname: 'Jane Smith', phone: '0987654321', join: '2022-12-01', status: 0, userType: 0 }
        ]);
    });
});
