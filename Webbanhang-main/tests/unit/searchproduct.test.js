// Mock global functions and DOM elements
global.detailProduct = jest.fn();
global.vnd = jest.fn(price => `${price}₫`);
document.body.innerHTML = `
    <div id="home-title" style="display: block;"></div>
    <div id="home-products"></div>
`;

// Function under test
function renderProducts(showProduct) {
    let productHtml = '';
    if (showProduct.length == 0) {
        document.getElementById("home-title").style.display = "none";
        productHtml = `<div class="no-result"><div class="no-result-h">Tìm kiếm không có kết quả</div><div class="no-result-p">Xin lỗi, chúng tôi không thể tìm được kết quả hợp với tìm kiếm của bạn</div><div class="no-result-i"><i class="fa-light fa-face-sad-cry"></i></div></div>`;
    } else {
        document.getElementById("home-title").style.display = "block";
        showProduct.forEach((product) => {
            productHtml += `<div class="col-product">
            <article class="card-product">
                <div class="card-header">
                    <a href="#" class="card-image-link" onclick="detailProduct(${product.id})">
                    <img class="card-image" src="${product.img}" alt="${product.title}">
                    </a>
                </div>
                <div class="food-info">
                    <div class="card-content">
                        <div class="card-title">
                            <a href="#" class="card-title-link" onclick="detailProduct(${product.id})">${product.title}</a>
                        </div>
                    </div>
                    <div class="card-footer">
                        <div class="product-price">
                            <span class="current-price">${vnd(product.price)}</span>
                        </div>
                    <div class="product-buy">
                        <button onclick="detailProduct(${product.id})" class="card-button order-item"><i class="fa-regular fa-cart-shopping-fast"></i> Đặt món</button>
                    </div> 
                </div>
                </div>
            </article>
        </div>`;
        });
    }
    document.getElementById('home-products').innerHTML = productHtml;
}

// Test Cases
describe('renderProducts', () => {
    afterEach(() => {
        jest.clearAllMocks();
        document.getElementById('home-products').innerHTML = '';
        document.getElementById('home-title').style.display = 'block';
    });

    test('Should display no result message when product list is empty', () => {
        renderProducts([]);

        expect(document.getElementById('home-title').style.display).toBe('none');
        expect(document.getElementById('home-products').innerHTML).toContain('Tìm kiếm không có kết quả');
        expect(document.getElementById('home-products').innerHTML).toContain('Xin lỗi, chúng tôi không thể tìm được kết quả hợp với tìm kiếm của bạn');
    });

    test('Should display product list when product list is not empty', () => {
        const sampleProducts = [
            { id: 1, img: 'img1.jpg', title: 'Product 1', price: 10000 },
            { id: 2, img: 'img2.jpg', title: 'Product 2', price: 20000 }
        ];

        renderProducts(sampleProducts);

        expect(document.getElementById('home-title').style.display).toBe('block');
        expect(document.getElementById('home-products').innerHTML).toContain('Product 1');
        expect(document.getElementById('home-products').innerHTML).toContain('Product 2');
        expect(document.getElementById('home-products').innerHTML).toContain('10000₫');
        expect(document.getElementById('home-products').innerHTML).toContain('20000₫');
    });

    });


