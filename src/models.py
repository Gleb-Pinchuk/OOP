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
        """
        self.__products.append(product)
        Category.product_count += 1


    @property
    def products(self) -> str:
        """
        Геттер для отображения списка товаров в заданном формате.
        Возвращает строку с перечислением всех товаров.
        """
        product_strings = []
        for product in self.__products:
            product_strings.append(
                f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт."
            )
        return "\n".join(product_strings)
