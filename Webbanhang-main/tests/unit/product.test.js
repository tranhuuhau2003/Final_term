// File addCart.test.js

describe('addCart', () => {
  let currentUser;
  let inputQty;
  let popupDetailNote;

  // Thiết lập mock cho các đối tượng và hàm cần thiết trước mỗi lần test
  beforeEach(() => {
    // Tạo HTML cần thiết cho test
    document.body.innerHTML = `
      <input class="input-qty" value="1" />
      <textarea id="popup-detail-note"></textarea>
    `;

    // Mock localStorage với dữ liệu giả cho người dùng
    currentUser = {
      username: 'testUser',
      cart: [
        { id: 1, soluong: 2, note: 'Ghi chú cũ' }  // Giả lập sản phẩm đã có trong giỏ hàng
      ]
    };

    // Lưu dữ liệu giả vào localStorage
    localStorage.setItem('currentuser', JSON.stringify(currentUser));

    // Mock các hàm updateAmount, closeModal và toast (chưa thực sự được gọi trong test)
    global.updateAmount = jest.fn();  // Mô phỏng hàm updateAmount
    global.closeModal = jest.fn();    // Mô phỏng hàm closeModal
    global.toast = jest.fn();         // Mô phỏng hàm toast
  });

  // Hàm addCart mà chúng ta cần test
  function addCart(index) {
    let currentuser = localStorage.getItem('currentuser') ? JSON.parse(localStorage.getItem('currentuser')) : [];
    let soluong = document.querySelector('.input-qty').value;  // Lấy giá trị số lượng sản phẩm
    let popupDetailNote = document.querySelector('#popup-detail-note').value;  // Lấy ghi chú sản phẩm
    let note = popupDetailNote == "" ? "Không có ghi chú" : popupDetailNote;  // Nếu không có ghi chú thì dùng giá trị mặc định

    // Tạo đối tượng sản phẩm sẽ thêm vào giỏ hàng
    let productcart = {
      id: index,
      soluong: parseInt(soluong),  // Chuyển số lượng thành kiểu số nguyên
      note: note
    }

    // Kiểm tra xem sản phẩm đã có trong giỏ hàng chưa
    let vitri = currentuser.cart.findIndex(item => item.id == productcart.id);

    // Nếu sản phẩm chưa có trong giỏ, thêm vào giỏ
    if (vitri == -1) {
      currentuser.cart.push(productcart);
    } else {
      // Nếu sản phẩm đã có trong giỏ, cập nhật số lượng
      currentuser.cart[vitri].soluong = parseInt(currentuser.cart[vitri].soluong) + parseInt(productcart.soluong);
    }

    // Lưu lại giỏ hàng mới vào localStorage
    localStorage.setItem('currentuser', JSON.stringify(currentuser));

    // Gọi các hàm để cập nhật số lượng giỏ và đóng modal
    updateAmount();
    closeModal();
  }

  // Test thêm sản phẩm mới vào giỏ nếu chưa có
  test('should add a new product to the cart if not already in the cart', () => {
    // Giả lập sản phẩm mới chưa có trong giỏ hàng
    const index = 2;  // ID sản phẩm mới
    const soluong = 3;
    const note = 'Ghi chú mới';
    document.querySelector('.input-qty').value = soluong;  // Set số lượng
    document.querySelector('#popup-detail-note').value = note;  // Set ghi chú

    // Gọi hàm addCart
    addCart(index);

    // Kiểm tra lại localStorage sau khi thêm sản phẩm mới
    const updatedUser = JSON.parse(localStorage.getItem('currentuser'));
    expect(updatedUser.cart).toHaveLength(2);  // Giỏ hàng phải có 2 sản phẩm
    expect(updatedUser.cart[1]).toEqual({
      id: 2,
      soluong: soluong,
      note: note
    });

    // Kiểm tra xem updateAmount có được gọi không
    expect(updateAmount).toHaveBeenCalled();
  });

  // Test cập nhật số lượng sản phẩm nếu sản phẩm đã có trong giỏ
  test('should update the quantity of an existing product in the cart', () => {
    // Giả lập sản phẩm đã có trong giỏ hàng
    const index = 1;  // ID sản phẩm đã có
    const soluong = 3;
    document.querySelector('.input-qty').value = soluong;  // Set số lượng
    document.querySelector('#popup-detail-note').value = 'Ghi chú mới';  // Set ghi chú

    // Gọi hàm addCart
    addCart(index);

    // Kiểm tra xem sản phẩm đã có trong giỏ hàng có số lượng đã cập nhật chưa
    const updatedUser = JSON.parse(localStorage.getItem('currentuser'));
    expect(updatedUser.cart[0].soluong).toBe(5);  // Sản phẩm có số lượng là 2 + 3 = 5

    // Kiểm tra xem updateAmount có được gọi không
    expect(updateAmount).toHaveBeenCalled();
  });

  // Test sử dụng ghi chú mặc định khi không nhập ghi chú
  test('should use default note when no note is entered', () => {
    // Giả lập sản phẩm mới và không nhập ghi chú
    const index = 3;
    const soluong = 2;
    document.querySelector('.input-qty').value = soluong;  // Set số lượng
    document.querySelector('#popup-detail-note').value = '';  // Không nhập ghi chú

    // Gọi hàm addCart
    addCart(index);

    // Kiểm tra xem sản phẩm mới được thêm vào giỏ với ghi chú mặc định
    const updatedUser = JSON.parse(localStorage.getItem('currentuser'));
    expect(updatedUser.cart[1].note).toBe('Không có ghi chú');  // Ghi chú mặc định

    // Kiểm tra xem updateAmount có được gọi không
    expect(updateAmount).toHaveBeenCalled();
  });

  // Test xem hàm closeModal có được gọi không
  test('should call closeModal after adding product to cart', () => {
    // Giả lập sản phẩm mới
    const index = 4;
    const soluong = 1;
    document.querySelector('.input-qty').value = soluong;

    // Gọi hàm addCart
    addCart(index);

    // Kiểm tra xem closeModal có được gọi sau khi thêm sản phẩm vào giỏ không
    expect(closeModal).toHaveBeenCalled();
  });

  // Test kiểm tra localStorage sau khi thêm sản phẩm vào giỏ hàng
  test('should update localStorage after adding product to cart', () => {
    const index = 1;
    const soluong = 2;
    document.querySelector('.input-qty').value = soluong;  // Set số lượng
    document.querySelector('#popup-detail-note').value = 'Ghi chú cập nhật';  // Set ghi chú

    // Gọi hàm addCart
    addCart(index);

    // Kiểm tra lại localStorage sau khi cập nhật giỏ hàng
    const updatedUser = JSON.parse(localStorage.getItem('currentuser'));
    expect(updatedUser.cart).toHaveLength(1);  // Vẫn chỉ có 1 sản phẩm trong giỏ hàng
    expect(updatedUser.cart[0].soluong).toBe(4);  // Số lượng phải được cập nhật (2 + 2 = 4)
    expect(updatedUser.cart[0].note).toBe('Ghi chú cập nhật');  // Kiểm tra ghi chú
  });
});

describe('deleteCartItem', () => {
  // Mock các biến và hàm cần thiết
  let currentUser;

  beforeEach(() => {
    // Tạo HTML cần thiết
    document.body.innerHTML = `
      <div class="cart-item">
        <button class="delete-button" onclick="deleteCartItem(1, this)">X</button>
      </div>
      <div class="gio-hang-trong" style="display: none;"></div>
      <button class="thanh-toan"></button>
    `;

    // Mock dữ liệu người dùng và giỏ hàng
    currentUser = {
      username: 'testUser',
      cart: [
        { id: 1, soluong: 2, note: 'Test note 1' },
        { id: 2, soluong: 1, note: 'Test note 2' },
      ]
    };

    // Lưu dữ liệu vào localStorage
    localStorage.setItem('currentuser', JSON.stringify(currentUser));

    // Mock hàm updateCartTotal
    global.updateCartTotal = jest.fn();
  });

  // Hàm deleteCartItem được kiểm tra
  function deleteCartItem(id, el) {
    let cartParent = el.parentNode.parentNode; // Lấy thẻ cha
    cartParent.remove(); // Xóa sản phẩm khỏi giao diện
    let currentUser = JSON.parse(localStorage.getItem('currentuser')); // Lấy dữ liệu người dùng
    let vitri = currentUser.cart.findIndex(item => item.id == id); // Tìm vị trí của sản phẩm trong giỏ
    currentUser.cart.splice(vitri, 1); // Xóa sản phẩm khỏi giỏ hàng

    // Nếu giỏ hàng trống, hiển thị thông báo
    if (currentUser.cart.length == 0) {
      document.querySelector('.gio-hang-trong').style.display = 'flex'; // Hiển thị thông báo giỏ hàng trống
      document.querySelector('button.thanh-toan').classList.add('disabled'); // Vô hiệu hóa nút thanh toán
    }

    // Cập nhật localStorage và tổng tiền
    localStorage.setItem('currentuser', JSON.stringify(currentUser));
    updateCartTotal();
  }

  test('should remove an item from the cart and update localStorage', () => {
    // Lấy nút xóa sản phẩm
    const deleteButton = document.querySelector('.delete-button');

    // Gọi hàm deleteCartItem để xóa sản phẩm có id = 1
    deleteCartItem(1, deleteButton);

    // Kiểm tra xem sản phẩm đã bị xóa khỏi giao diện chưa
    expect(document.querySelector('.cart-item')).toBeNull();

    // Kiểm tra dữ liệu trong localStorage
    const updatedUser = JSON.parse(localStorage.getItem('currentuser'));
    expect(updatedUser.cart).toHaveLength(1); // Giỏ hàng còn 1 sản phẩm
    expect(updatedUser.cart[0].id).toBe(2); // ID sản phẩm còn lại là 2
  });

  test('should show empty cart message if no items are left', () => {
    // Xóa tất cả sản phẩm để giỏ hàng trống
    currentUser.cart = [{ id: 1, soluong: 2, note: 'Test note 1' }];
    localStorage.setItem('currentuser', JSON.stringify(currentUser));

    // Lấy nút xóa sản phẩm
    const deleteButton = document.querySelector('.delete-button');

    // Gọi hàm deleteCartItem để xóa sản phẩm cuối cùng
    deleteCartItem(1, deleteButton);

    // Kiểm tra hiển thị thông báo giỏ hàng trống
    const emptyCartMessage = document.querySelector('.gio-hang-trong');
    expect(emptyCartMessage.style.display).toBe('flex'); // Thông báo giỏ hàng trống được hiển thị

    // Kiểm tra nút thanh toán bị vô hiệu hóa
    const checkoutButton = document.querySelector('button.thanh-toan');
    expect(checkoutButton.classList.contains('disabled')).toBe(true); // Nút thanh toán bị vô hiệu hóa
  });

  test('should call updateCartTotal after deleting an item', () => {
    // Lấy nút xóa sản phẩm
    const deleteButton = document.querySelector('.delete-button');

    // Gọi hàm deleteCartItem để xóa sản phẩm
    deleteCartItem(1, deleteButton);

    // Kiểm tra xem updateCartTotal có được gọi không
    expect(updateCartTotal).toHaveBeenCalled();
  });
});
