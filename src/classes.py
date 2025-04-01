import json


class Product:
    name: str
    description: str
    __price: float
    quantity: int
    product_list = []

    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

        Product.product_list.append(self)

    @classmethod
    def new_product(cls, product_data):
        """Создает новый продукт или обновляет существующий."""
        name = product_data["name"]
        description = product_data["description"]
        price = product_data["price"]
        quantity = product_data["quantity"]

        for product in cls.product_list:
            if product.name == name:
                # Если товар уже есть, обновляем количество и цену
                product.quantity += quantity
                product.price = max(product.price, price)
                return product

        # Если товара нет, создаем новый объект и добавляем в список
        new_product = cls(name, description, price, quantity)
        cls.product_list.append(new_product)
        return new_product

    @property
    def price(self):
        """Геттер для цены"""
        return self.__price

    @price.setter
    def price(self, new_price):
        """Сеттер для цены с проверкой"""
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return

        if new_price < self.__price:
            confirm = input(f"Вы уверены, что хотите понизить цену с {self.__price} до {new_price}? (y/n): ")
            if confirm.lower() != "y":
                print("Изменение цены отменено")
                return

        self.__price = new_price


class Category:
    name: str
    description: str
    __products: list[Product]
    category_count = 0
    product_count = 0

    def __init__(self, name, description, products=None):
        self.name = name
        self.description = description
        self.__products = []

        # Проверяем каждый продукт перед добавлением
        if products:
            for product in products:
                self.add_product(product)

        Category.category_count += 1

    def add_product(self, product: Product):
        """Добавляет продукт в категорию с проверкой типа"""
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только объекты класса Product или его наследников")
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self):
        """Возвращает список товаров в виде строк"""
        if not self.__products:
            return "В категории нет товаров."
        return "\n".join(
            f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт."
            for product in self.__products
        )


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