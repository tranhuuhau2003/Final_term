// modal.test.js
describe('closeModal function', () => {
    let modalContainer;
    let body;

    // Hàm closeModal cần kiểm tra
    function closeModal() {
        modalContainer.forEach(item => {
            item.classList.remove('open');
        });
        console.log(modalContainer); // Giả sử cần kiểm tra console.log
        body.style.overflow = "auto";
    }

    beforeEach(() => {
        // Thiết lập DOM giả
        document.body.innerHTML = `
            <div class="modal-container open"></div>
            <div class="modal-container open"></div>
        `;

        // Lấy các phần tử cần kiểm tra
        modalContainer = document.querySelectorAll('.modal-container');
        body = document.body;
    });

    test('should remove "open" class from all modal containers', () => {
        // Gọi hàm closeModal
        closeModal();

        // Kiểm tra xem tất cả các modal containers đã bị loại bỏ class "open"
        modalContainer.forEach(item => {
            expect(item.classList.contains('open')).toBe(false);
        });
    });

    test('should set body overflow to "auto"', () => {
        // Gọi hàm closeModal
        // Hàm closeModal có nhiệm vụ đóng các modal và khôi phục khả năng cuộn trang của body
        closeModal();

        // Kiểm tra thuộc tính overflow của body đã được thay đổi thành "auto"
        // Sau khi modal đóng, thuộc tính overflow của body phải được khôi phục lại thành "auto"
        // Điều này giúp trang có thể cuộn lại bình thường sau khi modal đóng.
        expect(body.style.overflow).toBe('auto');
    });

});
