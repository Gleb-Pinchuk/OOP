import pytest
from src.models import Product, Category, Smartphone, LawnGrass


@pytest.fixture(autouse=True)
def reset_category_counters():
    Category.category_count = 0
    Category.product_count = 0


@pytest.fixture
def sample_products():
    return [
        Product("Телефон", "Смартфон", 100, 10),
        Product("Наушники", "Беспроводные", 200, 2),
        Product("Планшет", "Компактный планшет", 50, 4),
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
    for p in sample_products:
        assert p.name in category.products


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


def test_product_creation_prints_log(capsys):
    product = Product("Мышь", "Игровая мышь", 2499.90, 50)
    captured = capsys.readouterr()
    assert "Product" in captured.out
    assert "Мышь" in captured.out
    assert "2499.9" in captured.out


def test_smartphone_creation_prints_log(capsys):
    phone = Smartphone("iPhone", "Смартфон", 100000, 2, "A16", "14 Pro", 256, "черный")
    captured = capsys.readouterr()
    assert "Smartphone" in captured.out
    assert "iPhone" in captured.out
    assert "100000" in captured.out


def test_lawngrass_creation_prints_log(capsys):
    grass = LawnGrass("Газон", "Семена", 500, 10, "Россия", 30, "зеленый")
    captured = capsys.readouterr()
    assert "LawnGrass" in captured.out
    assert "Газон" in captured.out
    assert "500" in captured.out


def test_add_same_class_products_returns_total_value():
    a = Product("Товар A", "Описание", 100, 10)
    b = Product("Товар B", "Описание", 200, 2)
    result = a + b
    assert result == 1400


def test_add_different_class_products_raises_type_error():
    phone = Smartphone("iPhone", "Смартфон", 100000, 2, "A16", "14 Pro", 256, "черный")
    grass = LawnGrass("Газон", "Семена", 500, 10, "Россия", 30, "зеленый")
    with pytest.raises(TypeError):
        _ = phone + grass


@pytest.mark.parametrize("invalid_obj", ["строка", 123, 45.6, {"name": "test"}, [1, 2, 3]])
def test_add_invalid_object_to_category_raises_type_error(invalid_obj, sample_products):
    category = Category("Электроника", "Гаджеты", sample_products)
    with pytest.raises(TypeError):
        category.add_product(invalid_obj)


def test_add_valid_inherited_products_to_category():
    category = Category("Товары", "Разные", [])
    phone = Smartphone("Samsung", "Galaxy", 50000, 5, "Snapdragon", "S22", 128, "синий")
    grass = LawnGrass("Газон", "Трава", 1000, 20, "Германия", 14, "зеленый")
    category.add_product(phone)
    category.add_product(grass)
    assert "Samsung" in category.products
    assert "Газон" in category.products
