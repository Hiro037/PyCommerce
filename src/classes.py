import json
from abc import ABC, abstractmethod

class CreationInfoMixin:
    def __init__(self, *args, **kwargs):
        class_name = self.__class__.__name__
        print(f"{class_name}{args}")
        super().__init__(*args, **kwargs)


class BaseProduct(ABC):
    @abstractmethod
    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    @abstractmethod
    def __str__(self) -> str:
        """Возвращает строковое представление продукта"""
        pass

    @abstractmethod
    def __add__(self, other):
        """Описывает логику сложения продуктов"""
        pass


class Product(CreationInfoMixin, BaseProduct):
    product_list = []

    def __init__(self, name, description, price, quantity):
        super().__init__(name, description, price, quantity)
        self._price = price
        Product.product_list.append(self)

    def __str__(self):
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other):
        if type(self) != type(other):
            raise TypeError("Нельзя складывать товары разных типов.")
        return self.price * self.quantity + other.price * other.quantity

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, new_price):
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return
        if new_price < self._price:
            confirm = input("Вы уверены, что хотите понизить цену? (y/n): ")
            if confirm.lower() != 'y':
                print("Снижение цены отменено")
                return
        self._price = new_price

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

    def __str__(self):
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def __iter__(self):
        """Делаем объект Category итерируемым."""
        return CategoryIterator(self)  # Возвращаем итератор

class CategoryIterator:
    """Класс-итератор для перебора товаров в категории."""
    def __init__(self, category):
        self._products = category.products  # Получаем список товаров категории
        self._index = 0  # Индекс текущего элемента

    def __iter__(self):
        return self  # Итератор возвращает сам себя

    def __next__(self):
        if self._index >= len(self._products):
            raise StopIteration  # Завершаем итерацию, если товары закончились

        product = self._products[self._index]
        self._index += 1
        return product


class Smartphone(Product):
    def __init__(self, name, description, price, quantity, efficiency, model, memory, color):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color


class LawnGrass(Product):
    def __init__(self, name, description, price, quantity, country, germination_period, color):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color


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
