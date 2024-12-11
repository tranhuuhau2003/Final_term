/**
 * @jest-environment jsdom
 */

// Định nghĩa các hàm
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

// Thiết lập các phần tử DOM cho việc kiểm thử
document.body.innerHTML = `
    <div class="quantity-control">
        <input class="input-qty" type="number" value="1" min="1" max="100" />
        <button class="increase">+</button>
        <button class="decrease">-</button>
    </div>
`;

// Các trường hợp kiểm thử
describe('Hàm increasingNumber', () => {

    beforeEach(() => {
        document.querySelector('.input-qty').value = '1';
    });

    test('nên tăng số lượng lên 1', () => {
        const button = document.querySelector('.increase');
        increasingNumber(button);

        const qty = document.querySelector('.input-qty').value;
        expect(qty).toBe('2');
    });

    test('không nên tăng số lượng vượt quá giá trị tối đa', () => {
        const button = document.querySelector('.increase');
        const qtyInput = document.querySelector('.input-qty');
        qtyInput.value = '100';
        
        increasingNumber(button);

        const qty = document.querySelector('.input-qty').value;
        expect(qty).toBe('100');
    });
});

describe('Hàm decreasingNumber', () => {

    beforeEach(() => {
        document.querySelector('.input-qty').value = '5';
    });

    test('nên giảm số lượng xuống 1', () => {
        const button = document.querySelector('.decrease');
        decreasingNumber(button);

        const qty = document.querySelector('.input-qty').value;
        expect(qty).toBe('4');
    });

    test('không nên giảm số lượng dưới giá trị tối thiểu', () => {
        const button = document.querySelector('.decrease');
        const qtyInput = document.querySelector('.input-qty');
        qtyInput.value = '1';
        
        decreasingNumber(button);

        const qty = document.querySelector('.input-qty').value;
        expect(qty).toBe('1');
    });
});
