// Mock localStorage for testing purposes
import { logOut } from '../js/logout.js';  // Update the path to match your project's structure
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

// Mock functions used in the logout process
const assignMock = jest.fn();
delete window.location;  // Xóa thuộc tính location hiện tại
window.location = { assign: assignMock };  // Thiết lập mock cho window.location.assign

// Define the logOut function here
function logOut() {
    let accounts = JSON.parse(localStorage.getItem('accounts'));
    let user = JSON.parse(localStorage.getItem('currentuser'));
    let vitri = accounts.findIndex(item => item.phone == user.phone);
    accounts[vitri].cart.length = 0;
    for (let i = 0; i < user.cart.length; i++) {
        accounts[vitri].cart[i] = user.cart[i];
    }
    localStorage.setItem('accounts', JSON.stringify(accounts));
    localStorage.removeItem('currentuser');
    window.location.assign("/");
}

// Test cases
describe('LogOut Function', () => {
    beforeEach(() => {
        jest.clearAllMocks();
        localStorage.clear();
    });

    test('It should redirect to home page', () => {
        const accounts = [{ phone: '1234567890', cart: ['item1', 'item2'] }];
        const currentUser = { phone: '1234567890', cart: ['item3', 'item4'] };

        localStorage.setItem('accounts', JSON.stringify(accounts));
        localStorage.setItem('currentuser', JSON.stringify(currentUser));

        logOut();

        expect(window.location.assign).toHaveBeenCalledWith("/");
    });
});
