import pytest
from src.models import Product, Category, Smartphone, LawnGrass


@pytest.fixture(autouse=True)
def reset_category_counters():
    """Сбрасывает счетчики Category перед каждым тестом"""
    Category.category_count = 0
    Category.product_count = 0


@pytest.fixture
def sample_products():
    return [
        Product("Телефон", "Смартфон", 100.0, 10),
        Product("Наушники", "Беспроводные", 200.0, 2),
        Product("Планшет", "Компактный планшет", 50.0, 4),
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


def test_new_product_from_dict():
    data = {"name": "Мышь", "description": "Игровая мышь", "price": 2499.90, "quantity": 50}
    product = Product.new_product(data)
    assert isinstance(product, Product)
    assert product.name == "Мышь"
    assert product.price == 2499.90
    assert product.quantity == 50


@pytest.mark.parametrize("invalid_price", [0, -1, -1000])
def test_invalid_price_does_not_change_value(capsys, invalid_price):
    product = Product("Клавиатура", "Механическая", 4999.99, 15)
    product.price = invalid_price
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out
    assert product.price == 4999.99


def test_products_string_format(sample_products):
    category = Category("Электроника", "Гаджеты", sample_products)
    products_str = category.products.split("\n")
    for line, p in zip(products_str, sample_products):
        assert line == str(p)


def test_category_str(sample_products):
    category = Category("Электроника", "Гаджеты", sample_products)
    total_quantity = sum(p.quantity for p in sample_products)
    assert str(category) == f"Электроника, количество продуктов: {total_quantity} шт."


def test_product_str():
    product = Product("Телевизор", "4K UHD", 89999.99, 2)
    assert str(product) == "Телевизор, 89999.99 руб. Остаток: 2 шт."


def test_add_same_class_products_returns_total_value():
    a = Product("Товар A", "Описание", 100, 10)  # 1000
    b = Product("Товар B", "Описание", 200, 2)   # 400
    result = a + b
    assert result == 1400


def test_add_different_class_products_raises_type_error():
    phone = Smartphone("iPhone", "Смартфон", 100000, 2, "A16", "14 Pro", 256, "черный")
    grass = LawnGrass("Газон", "Семена", 500, 10, "Россия", 30, "зеленый")
    with pytest.raises(TypeError):
        _ = phone + grass


def test_add_product_with_non_product_raises_type_error():
    a = Product("Товар A", "Описание", 100, 1)
    with pytest.raises(TypeError):
        _ = a + 123


@pytest.mark.parametrize("invalid_obj", ["строка", 123, 45.6, {"name": "test"}, [1, 2, 3]])
def test_add_invalid_object_to_category_raises_type_error(invalid_obj, sample_products):
    category = Category("Электроника", "Гаджеты", sample_products)
    with pytest.raises(TypeError):
        category.add_product(invalid_obj)


def test_add_valid_inherited_products():
    category = Category("Товары", "Разные", [])
    phone = Smartphone("Samsung", "Galaxy", 50000, 5, "Snapdragon", "S22", 128, "синий")
    grass = LawnGrass("Газон", "Трава", 1000, 20, "Германия", 14, "зеленый")
    category.add_product(phone)
    category.add_product(grass)
    assert "Samsung" in category.products
    assert "Газон" in category.products
