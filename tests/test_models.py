import pytest
from src.models import Product, Category


@pytest.fixture(autouse=True)
def reset_category_counters():
    """
    Фикстура для сброса счетчиков Category перед каждым тестом
    """
    Category.category_count = 0
    Category.product_count = 0


@pytest.fixture
def sample_products():
    return [
        Product("Телефон", "Смартфон", 29999.99, 10),
        Product("Наушники", "Беспроводные", 7999.50, 25),
        Product("Планшет", "Компактный планшет", 19999.00, 15),
    ]


def test_product_initialization():
    product = Product("Ноутбук", "Игровой ноутбук", 59999.90, 5)

    assert product.name == "Ноутбук"
    assert product.description == "Игровой ноутбук"
    assert product.price == 59999.90
    assert product.quantity == 5


def test_category_initialization(sample_products):
    category = Category("Электроника", "Гаджеты", sample_products)

    assert category.name == "Электроника"
    assert category.description == "Гаджеты"
    assert len(category.products) == 3
    assert isinstance(category.products[0], Product)


def test_category_count_increases(sample_products):
    assert Category.category_count == 0

    Category("Электроника", "Гаджеты", sample_products)
    assert Category.category_count == 1

    Category("Бытовая техника", "Техника для дома", [])
    assert Category.category_count == 2


def test_product_count_increases(sample_products):
    assert Category.product_count == 0

    Category("Электроника", "Гаджеты", sample_products)
    assert Category.product_count == 3

    Category("Бытовая техника", "Техника для дома", [
        Product("Холодильник", "Большой холодильник", 49999.90, 3)
    ])
    assert Category.product_count == 4
