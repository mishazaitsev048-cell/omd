from json_dict_processing import (
    extract_nested_value,
    process_dictionary_with_config,
    process_list_of_dicts_with_config,
    create_processor
)


# Проверка извлечения значения
def test_extract_nested_value():
    """Извлечение значения по ключам."""
    data = {'a': {'b': 10}}
    assert extract_nested_value(data, ['a', 'b']) == 10
    assert extract_nested_value(data, ['a', 'c']) is None
    assert extract_nested_value(data, ['a', 'b', 'c']) is None
    assert extract_nested_value({}, ['a']) is None


# Проверка обработки словаря
def test_process_dictionary_with_config():
    """Обработка словаря по конфигу."""
    data = {'a': '10'}
    config = {'b': (['a'], int), 'c': ['a']}
    assert process_dictionary_with_config(data, config) == {'b': 10, 'c': '10'}
    assert process_dictionary_with_config({}, config) == {'b': None, 'c': None}
    assert process_dictionary_with_config(data, {}) == {}


# Проверка обработки списка словарей
def test_process_list_of_dicts_with_config():
    """Обработка списка словарей."""
    data = [{'a': 1}, {'a': 2}]
    config = {'b': ['a']}
    assert process_list_of_dicts_with_config(data, config) == [
        {'b': 1},
        {'b': 2}
    ]
    assert process_list_of_dicts_with_config([], config) == []


# Проверка создания препроцессора
def test_create_processor():
    """Создание обработчиков словаря и списка."""
    config = {'b': ['a']}
    processor = create_processor(config)
    assert processor({'a': 10}) == {'b': 10}
    processor = create_processor(config, list_processor=True)
    assert processor([{'a': 10}]) == [{'b': 10}]
