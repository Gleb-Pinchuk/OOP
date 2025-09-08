from typing import List


class Product:
    def __init__(self, name: str, description: str, price: float, quantity: int):
        """
        Класс для описания товара.
        """
        self.name: str = name
        self.description: str = description
        self.price: float = price
        self.quantity: int = quantity


class Category:
    category_count: int = 0
    product_count: int = 0

    def __init__(self, name: str, description: str, products: List[Product]):
        """
        Класс для описания категории товаров.
        """
        self.name: str = name
        self.description: str = description
        self.products: List[Product] = products

        Category.category_count += 1
        Category.product_count += len(products)
