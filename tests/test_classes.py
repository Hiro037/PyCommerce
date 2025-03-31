import pytest
from src.classes import Product, Category

# Фикстуры для Product
@pytest.fixture
def sample_product():
    return Product("Test Product", "Test Description", 1000.0, 10)

@pytest.fixture
def product_data():
    return {
        "name": "Test Product",
        "description": "Test Description",
        "price": 1000.0,
        "quantity": 10
    }

# Фикстуры для Category
@pytest.fixture
def sample_category():
    products = [
        Product("Phone", "Smartphone", 50000.0, 5),
        Product("Laptop", "Gaming", 150000.0, 3)
    ]
    return Category("Electronics", "Devices", products)

# Тесты для Product
def test_product_initialization(sample_product):
    assert sample_product.name == "Test Product"
    assert sample_product.description == "Test Description"
    assert sample_product.price == 1000.0
    assert sample_product.quantity == 10

def test_price_setter_valid(sample_product):
    sample_product.price = 1500.0
    assert sample_product._price == 1500.0

def test_price_setter_negative(sample_product):
    sample_product.price = -100
    assert sample_product.price == 1000.0  # Цена не должна измениться

def test_price_setter_zero(sample_product):
    sample_product.price = 0
    assert sample_product.price == 1000.0  # Цена не должна измениться

def test_new_product_creation(product_data):
    new_product = Product.new_product({
        "name": "New Product",
        "description": "New Desc",
        "price": 500.0,
        "quantity": 3
    })
    assert isinstance(new_product, Product)
    assert new_product.name == "New Product"

def test_existing_product_update(product_data, sample_product):
    updated_product = Product.new_product(product_data)
    assert updated_product.quantity == 20  # 10 (из фикстуры) + 10 (из данных)

# Тесты для Category
def test_category_initialization(sample_category):
    assert sample_category.name == "Electronics"
    assert "Phone, 50000.0 руб." in sample_category.products
    assert "Laptop, 150000.0 руб." in sample_category.products

def test_add_product(sample_category):
    initial_count = Category.product_count
    new_product = Product("Tablet", "Drawing", 30000.0, 7)
    sample_category.add_product(new_product)
    assert Category.product_count == initial_count + 1
    assert "Tablet, 30000.0 руб." in sample_category.products

def test_empty_category():
    empty_category = Category("Empty", "Test")
    assert empty_category.products == "В категории нет товаров."

def test_category_count():
    initial_count = Category.category_count
    Category("Temp Category", "Test")
    assert Category.category_count == initial_count + 1
