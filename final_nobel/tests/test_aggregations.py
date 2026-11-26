import pytest
from aggregations import (
    calculate_mean,
    calculate_median,
    calculate_min,
    calculate_max,
    get_top_n
)


# Проверка среднего
def test_calculate_mean():
    """Расчет среднего."""
    assert calculate_mean([{'a': -10}, {'a': 20}], 'a') == 5
    assert calculate_mean([{'a': 1.5}, {'a': 2.5}], 'a') == 2
    assert calculate_mean([{'a': 10}, {'a': None}], 'a') == 10
    assert calculate_mean([{'a': None}], 'a') is None
    assert calculate_mean([], 'a') is None


def test_calculate_mean_errors():
    """Неверные типы и ключи."""
    for value in ['10', True, [10]]:
        with pytest.raises(TypeError):
            calculate_mean([{'a': value}], 'a')

    with pytest.raises(KeyError):
        calculate_mean([{'a': 10}], 'b')


# Проверка мелианы
def test_calculate_median():
    """Расчет медианы."""
    data = [{'a': 1}, {'a': 2}, {'a': 9}]
    assert calculate_median(data, 'a') == 2


# Проверка минимума и максимума
def test_calculate_min_max():
    """Поиск минимума и максимума."""
    data = [{'a': 2}, {'a': None}, {'a': 1}]
    assert calculate_min(data, 'a') == 1
    assert calculate_max(data, 'a') == 2


# Проверка топ н
def test_get_top_n():
    """Порядок и количество элементов."""
    data = {'a': 1, 'b': 3, 'c': 2}
    assert list(get_top_n(data, 2).items()) == [('b', 3), ('c', 2)]
    assert get_top_n(data, 5) == data
    assert get_top_n(data, 0) == {}
    assert get_top_n({}, 2) == {}


def test_get_top_n_errors():
    """Неверное значение n."""
    with pytest.raises(ValueError):
        get_top_n({'a': 1}, -1)

    with pytest.raises(TypeError):
        get_top_n({'a': 1}, '2')
