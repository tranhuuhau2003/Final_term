/**
 * @jest-environment jsdom
 */

// Define the functions
function increasingNumber(e) {
    let qty = e.parentNode.querySelector('.input-qty');
    if (parseInt(qty.value) < qty.max) {
        qty.value = parseInt(qty.value) + 1;
    } else {
        qty.value = qty.max;
    }
}

function decreasingNumber(e) {
    let qty = e.parentNode.querySelector('.input-qty');
    if (parseInt(qty.value) > qty.min) {
        qty.value = parseInt(qty.value) - 1;
    } else {
        qty.value = qty.min;
    }
}

// Set up DOM elements for testing
document.body.innerHTML = `
    <div class="quantity-control">
        <input class="input-qty" type="number" value="1" min="1" max="100" />
        <button class="increase">+</button>
        <button class="decrease">-</button>
    </div>
`;

// Test cases
describe('increasingNumber Function', () => {

    beforeEach(() => {
        document.querySelector('.input-qty').value = '1';
    });

    test('should increase the quantity by 1', () => {
        const button = document.querySelector('.increase');
        increasingNumber(button);

        const qty = document.querySelector('.input-qty').value;
        expect(qty).toBe('2');
    });

    test('should not increase the quantity beyond the maximum value', () => {
        const button = document.querySelector('.increase');
        const qtyInput = document.querySelector('.input-qty');
        qtyInput.value = '100';
        
        increasingNumber(button);

        const qty = document.querySelector('.input-qty').value;
        expect(qty).toBe('100');
    });
});

describe('decreasingNumber Function', () => {

    beforeEach(() => {
        document.querySelector('.input-qty').value = '5';
    });

    test('should decrease the quantity by 1', () => {
        const button = document.querySelector('.decrease');
        decreasingNumber(button);

        const qty = document.querySelector('.input-qty').value;
        expect(qty).toBe('4');
    });

    test('should not decrease the quantity below the minimum value', () => {
        const button = document.querySelector('.decrease');
        const qtyInput = document.querySelector('.input-qty');
        qtyInput.value = '1';
        
        decreasingNumber(button);

        const qty = document.querySelector('.input-qty').value;
        expect(qty).toBe('1');
    });
});
