import pytest
from src.models import Product, Category


@pytest.fixture(autouse=True)
def reset_category_counters():
    """
    Сбрасывает счетчики Category перед каждым тестом
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

    products_str = category.products
    assert isinstance(products_str, str)

    for p in sample_products:
        assert p.name in products_str
        assert str(p.price) in products_str
        assert str(p.quantity) in products_str


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


def test_add_product_increases_count(sample_products):
    category = Category("Электроника", "Гаджеты", sample_products)
    initial_count = Category.product_count

    new_product = Product("Смарт-часы", "Фитнес-браслет", 9999.99, 20)
    category.add_product(new_product)

    assert Category.product_count == initial_count + 1
    assert "Смарт-часы" in category.products
    assert "9999.99 руб." in category.products
    assert "20 шт." in category.products


def test_add_invalid_product_raises_type_error(sample_products):
    category = Category("Электроника", "Гаджеты", sample_products)
    with pytest.raises(TypeError):
        category.add_product("не продукт")  # строка вместо Product


def test_new_product_from_dict():
    data = {
        "name": "Мышь",
        "description": "Игровая мышь",
        "price": 2499.90,
        "quantity": 50
    }
    product = Product.new_product(data)

    assert isinstance(product, Product)
    assert product.name == "Мышь"
    assert product.price == 2499.90
    assert product.quantity == 50


@pytest.mark.parametrize("invalid_price", [0, -1, -1000])
def test_invalid_price_does_not_change_value(capsys, invalid_price):
    product = Product("Клавиатура", "Механическая", 4999.99, 15)

    product.price = invalid_price  # некорректное значение
    captured = capsys.readouterr()

    assert "Цена не должна быть нулевая или отрицательная" in captured.out
    assert product.price == 4999.99  # цена осталась прежней


def test_products_string_format(sample_products):
    category = Category("Электроника", "Гаджеты", sample_products)
    products_str = category.products.split("\n")

    for line, p in zip(products_str, sample_products):
        assert line == f"{p.name}, {p.price} руб. Остаток: {p.quantity} шт."
