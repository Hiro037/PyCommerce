from src.classes import Product,Category
import pytest

@pytest.fixture()
def create_product():
    return Product('Apple', 'Tasty fruit', 10.00, 5)


@pytest.fixture()
def create_category():
    yield Category('Fruits', 'Lots of goodies', ['Apple', 'Banana'])
    Category.category_count = 0
    Category.product_count = 0

def test_category_init(create_category):  # Тест на корректность инициализации Category
    assert create_category.name == 'Fruits'
    assert create_category.description == 'Lots of goodies'
    assert create_category.products == ['Apple', 'Banana']

def test_product_init(create_product):  # Тест на корректность инициализации Product
    assert create_product.name == 'Apple'
    assert create_product.description == 'Tasty fruit'
    assert create_product.price == 10.00
    assert create_product.quantity == 5

def test_product_count(create_category):  # Тест на подсчет количества продуктов
    assert Category.product_count == 2

def test_category_count(create_category):  # Тест на подсчет количества категорий
    assert Category.category_count == 1