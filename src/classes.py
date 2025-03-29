import json


class Product:
    name: str
    description: str
    price: float
    quantity: int

    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity


class Category:
    name: str
    description: str
    products: list[Product]
    category_count = 0
    product_count = 0

    def __init__(self, name, description, products):
        self.name = name
        self.description = description
        self.products = products

        Category.category_count += 1
        Category.product_count += len(products)


# Функция для подгрузки данных из JSON и создания объектов
def load_data_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)  # Чтение и парсинг JSON файла

    categories = []

    for category_data in data:
        products = [
            Product(p['name'], p['description'], p['price'], p['quantity'])
            for p in category_data['products']
        ]
        category = Category(category_data['name'], category_data['description'], products)
        categories.append(category)

    return categories
