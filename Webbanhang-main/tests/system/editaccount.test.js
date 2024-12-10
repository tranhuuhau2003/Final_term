// Mock global functions and DOM elements
global.toast = jest.fn();
document.body.innerHTML = `
    <div class="signup"></div>
    <div id="home-title" style="display: block;"></div>
    <div id="home-products"></div>
    <input id="fullname" />
    <input id="phone" />
    <input id="password" />
    <input id="user-status" type="checkbox" />
    <button id="updateAccount"></button>
    <div class="add-account-e"></div>
    <div class="edit-account-e"></div>
`;

// Mock localStorage
const localStorageMock = (() => {
    let store = {};
    return {
        getItem: jest.fn((key) => store[key] || null),
        setItem: jest.fn((key, value) => store[key] = value.toString()),
        clear: jest.fn(() => store = {}),
        removeItem: jest.fn((key) => delete store[key])
    };
})();

Object.defineProperty(window, 'localStorage', { value: localStorageMock });

let indexFlag;

// Function under test
function editAccount(phone) {
    document.querySelector(".signup").classList.add("open");
    document.querySelectorAll(".add-account-e").forEach(item => {
        item.style.display = "none";
    });
    document.querySelectorAll(".edit-account-e").forEach(item => {
        item.style.display = "block";
    });
    let accounts = JSON.parse(localStorage.getItem("accounts"));
    let index = accounts.findIndex(item => {
        return item.phone == phone;
    });
    indexFlag = index;
    document.getElementById("fullname").value = accounts[index].fullname;
    document.getElementById("phone").value = accounts[index].phone;
    document.getElementById("password").value = accounts[index].password;
    document.getElementById("user-status").checked = accounts[index].status == 1 ? true : false;
}

document.getElementById("updateAccount").addEventListener("click", (e) => {
    e.preventDefault();
    let accounts = JSON.parse(localStorage.getItem("accounts"));
    let fullname = document.getElementById("fullname").value;
    let phone = document.getElementById("phone").value;
    let password = document.getElementById("password").value;
    if(fullname == "" || phone == "" || password == "") {
        toast({ title: 'Chu y', message: 'Vui long nhap day du thong tin !', type: 'warning', duration: 3000 });
    } else {
        accounts[indexFlag].fullname = fullname;
        accounts[indexFlag].phone = phone;
        accounts[indexFlag].password = password;
        accounts[indexFlag].status = document.getElementById("user-status").checked ? 1 : 0;
        localStorage.setItem("accounts", JSON.stringify(accounts));
        toast({ title: 'Thanh cong', message: 'Thay doi thong tin thanh cong !', type: 'success', duration: 3000 });
        document.querySelector(".signup").classList.remove("open");
        signUpFormReset();
        showUser();
    }
});

// Mock additional functions used within updateAccount event listener
global.signUpFormReset = jest.fn();
global.showUser = jest.fn();

// Test Cases
describe('editAccount', () => {
    beforeEach(() => {
        localStorage.getItem.mockReturnValue(JSON.stringify([
            { fullname: 'User One', phone: '1234567890', password: 'pass1', status: 1 },
            { fullname: 'User Two', phone: '0987654321', password: 'pass2', status: 0 }
        ]));
        document.querySelector(".signup").classList.remove("open");
        document.querySelectorAll(".add-account-e").forEach(item => item.style.display = "block");
        document.querySelectorAll(".edit-account-e").forEach(item => item.style.display = "none");
        document.getElementById("fullname").value = "";
        document.getElementById("phone").value = "";
        document.getElementById("password").value = "";
        document.getElementById("user-status").checked = false;
    });

    afterEach(() => {
        jest.clearAllMocks();
    });

    test('Should open signup modal and populate fields for editing', () => {
        editAccount('1234567890');

        expect(document.querySelector(".signup").classList.contains("open")).toBe(true);
        expect(document.querySelectorAll(".add-account-e")[0].style.display).toBe("none");
        expect(document.querySelectorAll(".edit-account-e")[0].style.display).toBe("block");
        expect(document.getElementById("fullname").value).toBe("User One");
        expect(document.getElementById("phone").value).toBe("1234567890");
        expect(document.getElementById("password").value).toBe("pass1");
        expect(document.getElementById("user-status").checked).toBe(true);
    });
});

describe('updateAccount', () => {
    beforeEach(() => {
        localStorage.getItem.mockReturnValue(JSON.stringify([
            { fullname: 'User One', phone: '1234567890', password: 'pass1', status: 1 },
            { fullname: 'User Two', phone: '0987654321', password: 'pass2', status: 0 }
        ]));
        document.getElementById("updateAccount").click();  // Ensure the event listener is set up
    });

    afterEach(() => {
        jest.clearAllMocks();
        document.getElementById("fullname").value = "";
        document.getElementById("phone").value = "";
        document.getElementById("password").value = "";
        document.getElementById("user-status").checked = false;
    });

    test('Should display warning toast when fields are empty', () => {
        document.getElementById("fullname").value = "";
        document.getElementById("phone").value = "";
        document.getElementById("password").value = "";

        document.getElementById("updateAccount").click();

        expect(toast).toHaveBeenCalledWith({ title: 'Chu y', message: 'Vui long nhap day du thong tin !', type: 'warning', duration: 3000 });
    });

    test('Should update account information and display success toast when fields are valid', () => {
        document.getElementById("fullname").value = "User Updated";
        document.getElementById("phone").value = "1234567890";
        document.getElementById("password").value = "newpass";
        document.getElementById("user-status").checked = true;
        indexFlag = 0; // Ensure indexFlag is set to simulate editAccount function

        document.getElementById("updateAccount").click();

        expect(localStorage.setItem).toHaveBeenCalledWith("accounts", JSON.stringify([
            { fullname: 'User Updated', phone: '1234567890', password: 'newpass', status: 1 },
            { fullname: 'User Two', phone: '0987654321', password: 'pass2', status: 0 }
        ]));
        expect(toast).toHaveBeenCalledWith({ title: 'Thanh cong', message: 'Thay doi thong tin thanh cong !', type: 'success', duration: 3000 });
        expect(document.querySelector(".signup").classList.contains("open")).toBe(false);
        expect(global.signUpFormReset).toHaveBeenCalled();
        expect(global.showUser).toHaveBeenCalled();
    });
});
