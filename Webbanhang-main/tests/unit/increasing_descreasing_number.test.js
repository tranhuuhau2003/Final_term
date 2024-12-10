
describe('increasingNumber', () => {
  let inputElement;

  // Functions are directly included in the test file
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
    if (qty.value > qty.min) {
      qty.value = parseInt(qty.value) - 1;
    } else {
      qty.value = qty.min;
    }
  }

  beforeEach(() => {
    // Mocking a DOM element for the input field
    document.body.innerHTML = `<div><input type="number" class="input-qty" value="5" min="1" max="10"></div>`;
    inputElement = document.querySelector('.input-qty');
  });

  test('should increase value when less than max', () => {
    inputElement.value = 5;
    inputElement.max = 10;
    // Gọi hàm increasingNumber để tăng giá trị của inputElement
    increasingNumber({ parentNode: inputElement.parentNode });
    // Kiểm tra giá trị của inputElement đã được tăng lên 6
    expect(inputElement.value).toBe("6");
  });

  test('should not exceed max value', () => {
    inputElement.value = 10;
    inputElement.max = 10;
    // Gọi hàm increasingNumber với giá trị đã bằng max
    increasingNumber({ parentNode: inputElement.parentNode });
    // Kiểm tra xem giá trị của inputElement có vượt quá max không
    expect(inputElement.value).toBe("10");
  });
});



describe('decreasingNumber', () => {
  let inputElement;

  // Functions are directly included in the test file
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
    if (qty.value > qty.min) {
      qty.value = parseInt(qty.value) - 1;
    } else {
      qty.value = qty.min;
    }
  }

  beforeEach(() => {
    // Mocking a DOM element for the input field
    document.body.innerHTML = `<div><input type="number" class="input-qty" value="5" min="1" max="10"></div>`;
    inputElement = document.querySelector('.input-qty');
  });

  test('should decrease value when greater than min', () => {
    inputElement.value = 5;
    inputElement.min = 1;
    // Gọi hàm decreasingNumber để giảm giá trị của inputElement
    decreasingNumber({ parentNode: inputElement.parentNode });
    // Kiểm tra giá trị của inputElement đã giảm xuống 4
    expect(inputElement.value).toBe("4");
  });

  test('should not go below min value', () => {
    inputElement.value = 1;
    inputElement.min = 1;
    // Gọi hàm decreasingNumber với giá trị đã bằng min
    decreasingNumber({ parentNode: inputElement.parentNode });
    // Kiểm tra xem giá trị của inputElement có giảm xuống dưới min không
    expect(inputElement.value).toBe("1");
  });
});


describe('Edge cases', () => {
  let inputElement;

  // Functions are directly included in the test file
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
    if (qty.value > qty.min) {
      qty.value = parseInt(qty.value) - 1;
    } else {
      qty.value = qty.min;
    }
  }

  beforeEach(() => {
    document.body.innerHTML = `<div><input type="number" class="input-qty" value="1" min="1" max="10"></div>`;
    inputElement = document.querySelector('.input-qty');
  });

  test('should not decrease below the min value', () => {
    inputElement.value = 1;
    inputElement.min = 1;
    inputElement.max = 10;
    // Gọi hàm decreasingNumber với giá trị đã bằng min
    decreasingNumber({ parentNode: inputElement.parentNode });
    // Kiểm tra giá trị của inputElement không giảm dưới min
    expect(inputElement.value).toBe("1");
  });

  test('should not increase above the max value', () => {
    inputElement.value = 10;
    inputElement.min = 1;
    inputElement.max = 10;
    // Gọi hàm increasingNumber với giá trị đã bằng max
    increasingNumber({ parentNode: inputElement.parentNode });
    // Kiểm tra giá trị của inputElement không tăng vượt quá max
    expect(inputElement.value).toBe("10");
  });
});



describe('Invalid input', () => {
  let inputElement;

  // Functions are directly included in the test file
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
    if (qty.value > qty.min) {
      qty.value = parseInt(qty.value) - 1;
    } else {
      qty.value = qty.min;
    }
  }

  beforeEach(() => {
    document.body.innerHTML = `<div><input type="number" class="input-qty" value="abc" min="1" max="10"></div>`;
    inputElement = document.querySelector('.input-qty');
  });

  test('should handle non-numeric input gracefully', () => {
    inputElement.value = "abc";
    inputElement.max = 10;
    inputElement.min = 1;
    increasingNumber({ parentNode: inputElement.parentNode });
    expect(inputElement.value).toBe("NaN");
  });
});
