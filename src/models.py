from typing import Dict, List


class Product:
    def __init__(self, name: str, description: str, price: float, quantity: int):
        """
        Класс для описания товара.
        """
        self.name: str = name
        self.description: str = description
        self.__price: float = 0.0
        self.price = price
        self.quantity: int = quantity


    @property
    def price(self) -> float:
        """
        Геттер для получения цены товара.
        """
        return self.__price


    @price.setter
    def price(self, value: float) -> None:
        """
        Сеттер для установки цены товара с валидацией.
        """
        if value <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        else:
            self.__price = value


    @classmethod
    def new_product(cls, product_data: Dict[str, any]) -> 'Product':
        """
        Класс-метод для создания нового товара из словаря с параметрами.
        """
        return cls(
            name=product_data['name'],
            description=product_data['description'],
            price=product_data['price'],
            quantity=product_data['quantity']
        )


    def __str__(self) -> str:
        """
        Строковое отображение товара.
        """
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."


    def __add__(self, other: object) -> float:
        """
        Складывает два товара, возвращая суммарную стоимость их остатков.
        """
        if not isinstance(other, Product):
            raise TypeError("Складывать можно только объекты класса Product")

        return self.price * self.quantity + other.price * other.quantity


class Category:
    category_count: int = 0
    product_count: int = 0

    def __init__(self, name: str, description: str, products: List[Product]):
        """
        Класс для описания категории товаров.
        """
        self.name: str = name
        self.description: str = description
        self.__products: List[Product] = products

        Category.category_count += 1
        Category.product_count += len(products)


    def add_product(self, product: Product) -> None:
        """
        Добавляет товар в категорию.
        Принимает только объекты класса Product или его наследников.
        """
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только объекты класса Product или его наследников")

        self.__products.append(product)
        Category.product_count += 1


    @property
    def products(self) -> str:
        """
        Возвращает строку с перечислением всех товаров.
        """
        return "\n".join(str(product) for product in self.__products)


    def __str__(self) -> str:
        """
        Строковое отображение категории.
        """
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."
