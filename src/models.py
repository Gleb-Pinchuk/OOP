from abc import ABC, abstractmethod
from typing import Dict, List


class InitLoggerMixin:
    """
    Миксин: при создании объекта печатает в консоль информацию о классе и
    аргументах конструктора, и реализует __repr__.
    """

    def __init__(self, *args, **kwargs):
        parts = [repr(a) for a in args] + [f"{k}={v!r}" for k, v in kwargs.items()]
        try:
            print(f"{self.__class__.__name__}({', '.join(parts)})")
        except Exception:
            print(f"Создан объект {self.__class__.__name__}")
        super().__init__(*args, **kwargs)

    def __repr__(self) -> str:
        parts: List[str] = []
        for a in ("name", "description", "price", "quantity"):
            if hasattr(self, a):
                parts.append(repr(getattr(self, a)))
        extra_parts: List[str] = []
        for k, v in vars(self).items():
            if k.startswith("_") or k in ("name", "description", "price", "quantity"):
                continue
            extra_parts.append(f"{k}={v!r}")
        all_parts = ", ".join(parts + extra_parts)
        return f"{self.__class__.__name__}({all_parts})"


class BaseProduct(ABC):
    """
    Абстрактный базовый класс для всех продуктов.
    Описывает общую функциональность: имя, описание, цену, количество.
    """

    def __init__(self, name: str, description: str, price: float, quantity: int):
        if quantity <= 0:
            raise ValueError("Товар с нулевым количеством не может быть добавлен")
        self.name: str = name
        self.description: str = description
        self._price: float = 0.0
        self.price = price
        self.quantity: int = quantity

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        if value <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        else:
            self._price = value

    @abstractmethod
    def __str__(self) -> str:
        ...

    @abstractmethod
    def __add__(self, other: object) -> float:
        ...


class Product(InitLoggerMixin, BaseProduct):
    """
    Конкретный продукт — наследует mixin и абстрактный класс.
    """

    def __str__(self) -> str:
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: object) -> float:
        if not isinstance(other, BaseProduct):
            raise TypeError("Складывать можно только объекты Product или его наследников")
        if type(self) is not type(other):
            raise TypeError("Складывать можно только товары одного класса продуктов")
        return self.price * self.quantity + other.price * other.quantity

    @classmethod
    def new_product(cls, product_data: Dict[str, any]) -> "Product":
        return cls(
            name=product_data["name"],
            description=product_data["description"],
            price=product_data["price"],
            quantity=product_data["quantity"],
        )


class Smartphone(Product):
    def __init__(self, name: str, description: str, price: float, quantity: int,
                 efficiency: str, model: str, memory: int, color: str):
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
        self.name: str = name
        self.description: str = description
        self.__products: List[Product] = []

        for p in products:
            self.add_product(p)

        Category.category_count += 1

    def add_product(self, product: Product) -> None:
        if not isinstance(product, BaseProduct):
            raise TypeError("Можно добавлять только объекты класса Product или его наследников")
        if not issubclass(type(product), BaseProduct):
            raise TypeError("Объект должен быть наследником класса BaseProduct")
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        return "\n".join(str(product) for product in self.__products)

    def __str__(self) -> str:
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def average_price(self) -> float:
        """
        Возвращает среднюю цену всех товаров в категории.
        Если товаров нет, возвращает 0.
        """
        try:
            total_price = sum(product.price for product in self.__products)
            avg_price = total_price / len(self.__products)
            return avg_price
        except ZeroDivisionError:
            return 0.0
