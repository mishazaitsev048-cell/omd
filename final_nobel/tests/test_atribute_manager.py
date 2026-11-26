import pytest
from atribute_manager import add_attribute


# Проверка добавления нового атрибута
def test_add_attribute():
    """Добавление и перезапись атрибута."""
    data = [{'a': 10}]
    assert add_attribute(data, 'b', lambda x: 20) == [{'a': 10, 'b': 20}]
    assert add_attribute(data, 'a', lambda x: 20) == [{'a': 20}]
    assert data == [{'a': 10}]
    assert add_attribute([], 'b', lambda x: 20) == []


def test_add_attribute_errors():
    """Неверная функция или ключ."""
    with pytest.raises(TypeError):
        add_attribute([{'a': 10}], 'b', 20)

    with pytest.raises(KeyError):
        add_attribute([{'a': 10}], 'b', lambda x: x['c'])
