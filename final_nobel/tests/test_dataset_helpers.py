import pytest
from dataset_helpers import (
    count_missing_values,
    calculate_missing_ratios,
    filter_data,
    group_by_attributes,
    apply_aggregation
)


# Проверка пропусков
def test_count_missing_values():
    """Подсчет пропусков."""
    data = [{'a': 10}, {'a': None}, {'a': None}]
    assert count_missing_values(data) == {'a': 2}
    assert count_missing_values([]) == {}
    assert count_missing_values([{'a': None}]) == {'a': 1}
    assert count_missing_values([{'a': 0}, {'a': False}]) == {'a': 0}


# Проверка доли пропусков
def test_calculate_missing_ratios():
    """Расчет доли пропусков."""
    data = [{'a': 10}, {'a': 20}, {'a': None}]
    assert calculate_missing_ratios(data) == {'a': 0.3333}
    assert calculate_missing_ratios([]) == {}
    assert calculate_missing_ratios([{'a': None}]) == {'a': 1}
    assert calculate_missing_ratios([{'a': 10}]) == {'a': 0}


# Проверка фильтрации
def test_filter_data():
    """Фильтрация данных."""
    data = [{'a': 10}, {'a': 20}]
    assert filter_data(data, lambda x: x['a'] > 10) == [{'a': 20}]
    assert filter_data(data, lambda x: x['a'] > 30) == []
    assert filter_data([], lambda x: True) == []


def test_filter_data_errors():
    """Неверное условие или ключ."""
    with pytest.raises(TypeError):
        filter_data([{'a': 10}], 10)
    with pytest.raises(KeyError):
        filter_data([{'a': 10}], lambda x: x['b'])


# Проверка группировки
def test_group_by_attributes():
    """Группировка по атрибутам."""
    data = [{'a': 1, 'b': 2}, {'a': 1, 'b': 3}]
    assert group_by_attributes(data, ['a']) == {(1,): data}
    assert group_by_attributes(data, ['a', 'b']) == {
        (1, 2): [data[0]],
        (1, 3): [data[1]]
    }
    assert group_by_attributes([], ['a']) == {}


def test_group_by_attributes_errors():
    """Неверный ключ или тип."""
    with pytest.raises(KeyError):
        group_by_attributes([{'a': 1}], ['b'])
    with pytest.raises(TypeError):
        group_by_attributes([{'a': [1]}], ['a'])


# Проверка агрегации
def test_apply_aggregation():
    """Агрегация по группам."""
    assert apply_aggregation({'a': [1, 2], 'b': [4]}, sum) == {'a': 3, 'b': 4}
    assert apply_aggregation({}, sum) == {}
    with pytest.raises(TypeError):
        apply_aggregation({'a': [1]}, 10)
