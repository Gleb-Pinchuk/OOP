from typing import Dict, List


class Product:
    def __init__(self, name: str, description: str, price: float, quantity: int):
        """
        Базовый класс для описания товара.
        """
        self.name: str = name
        self.description: str = description
        self.__price: float = 0.0
        self.price = price
        self.quantity: int = quantity

    @property
    def price(self) -> float:
        """Геттер для получения цены товара."""
        return self.__price

    @price.setter
    def price(self, value: float) -> None:
        """Сеттер для установки цены товара с валидацией."""
        if value <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        else:
            self.__price = value

    @classmethod
    def new_product(cls, product_data: Dict[str, any]) -> 'Product':
        """Класс-метод для создания нового товара из словаря с параметрами."""
        return cls(
            name=product_data['name'],
            description=product_data['description'],
            price=product_data['price'],
            quantity=product_data['quantity']
        )

    def __str__(self) -> str:
        """Строковое представление продукта."""
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: object) -> float:
        """
        Магический метод сложения продуктов.
        Складывать можно только товары одного класса (type(self) == type(other)).
        """
        if not isinstance(other, Product):
            raise TypeError("Складывать можно только объекты Product или его наследников")

        if type(self) is not type(other):
            raise TypeError("Складывать можно только товары одного класса продуктов")

        return self.price * self.quantity + other.price * other.quantity


class Smartphone(Product):
    def __init__(self, name: str, description: str, price: float, quantity: int,
                 efficiency: str, model: str, memory: int, color: str):
        """Класс для описания смартфона."""
        super().__init__(name, description, price, quantity)
        self.efficiency: str = efficiency
        self.model: str = model
        self.memory: int = memory
        self.color: str = color

    def __str__(self) -> str:
        return (f"{self.name} ({self.model}, {self.memory} ГБ, {self.color}), "
                f"{self.price} руб. Остаток: {self.quantity} шт.")


class LawnGrass(Product):
    def __init__(self, name: str, description: str, price: float, quantity: int,
                 country: str, germination_period: int, color: str):
        """Класс для описания газонной травы."""
        super().__init__(name, description, price, quantity)
        self.country: str = country
        self.germination_period: int = germination_period
        self.color: str = color

    def __str__(self) -> str:
        return (f"{self.name} ({self.color}, {self.country}, "
                f"срок прорастания {self.germination_period} дней), "
                f"{self.price} руб. Остаток: {self.quantity} шт.")


class Category:
    category_count: int = 0
    product_count: int = 0

    def __init__(self, name: str, description: str, products: List[Product]):
        """Класс для описания категории товаров."""
        self.name: str = name
        self.description: str = description
        self.__products: List[Product] = []

        for p in products:
            self.add_product(p)

        Category.category_count += 1

    def add_product(self, product: Product) -> None:
        """
        Добавляет товар в категорию.
        Разрешены только объекты класса Product или его наследников.
        """
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только объекты класса Product или его наследников")

        if not issubclass(type(product), Product):
            raise TypeError("Объект должен быть наследником класса Product")

        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        """Геттер для отображения списка товаров в заданном формате."""
        return "\n".join(str(product) for product in self.__products)

    def __str__(self) -> str:
        """Строковое представление категории."""
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."
