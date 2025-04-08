import pytest
from src.classes import Product, Smartphone, LawnGrass, Category


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
    assert sample_product.price == 1500.0

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


def test_product_str():
    product = Product("Ноутбук", "Игровой ноутбук", 100_000, 5)
    assert str(product) == "Ноутбук, 100000 руб. Остаток: 5 шт."


def test_category_str():
    category = Category("Электроника", "Электроника")
    product1 = Product("Ноутбук", "Игровой ноутбук", 100_000, 5)
    product2 = Product("Смартфон", "Флагманский телефон", 80_000, 3)
    category.add_product(product1)
    category.add_product(product2)

    assert str(category) == "Электроника, количество продуктов: 8 шт."


def test_product_addition():
    product1 = Product("Ноутбук", "Игровой ноутбук", 100_000, 5)
    product2 = Product("Смартфон", "Флагманский телефон", 80_000, 3)

    total_price = product1 + product2
    assert total_price == (100_000 * 5 + 80_000 * 3)

# Тест: успешное сложение товаров одного класса
def test_product_add_same_type():
    phone1 = Smartphone("Phone A", "desc", 100.0, 3, "Snapdragon", "A1", "128GB", "black")
    phone2 = Smartphone("Phone B", "desc", 200.0, 2, "Snapdragon", "B2", "256GB", "blue")

    total = phone1 + phone2
    assert total == (100.0 * 3 + 200.0 * 2)

# Тест: ошибка при сложении разных классов
def test_product_add_different_types():
    phone = Smartphone("Phone", "desc", 100.0, 3, "Snapdragon", "A1", "128GB", "black")
    grass = LawnGrass("Grass", "desc", 50.0, 10, "Germany", "7 days", "green")

    with pytest.raises(TypeError):
        _ = phone + grass

# Тест: добавление только экземпляров Product или наследников
def test_add_valid_product():
    category = Category("Gadgets", 'Гаджеты')
    phone = Smartphone("Phone", "desc", 100.0, 3, "Snapdragon", "A1", "128GB", "black")

    category.add_product(phone)
    assert len(category._Category__products) == 1
    assert category._Category__products[0].name == "Phone"

def test_add_invalid_product():
    category = Category("Gadgets", 'Гаджеты')
    with pytest.raises(TypeError):
        category.add_product("not a product")

# Тест: инициализация LawnGrass
def test_lawngrass_attributes():
    grass = LawnGrass("Grass", "desc", 60.0, 5, "Netherlands", "10 days", "green")
    assert grass.country == "Netherlands"
    assert grass.germination_period == "10 days"
    assert grass.color == "green"

# Тест: инициализация Smartphone
def test_smartphone_attributes():
    phone = Smartphone("Galaxy", "desc", 200.0, 4, "Exynos", "S23", "256GB", "gray")
    assert phone.model == "S23"
    assert phone.memory == "256GB"
