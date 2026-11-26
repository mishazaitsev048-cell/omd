from typing import Any, Callable
from functools import partial


def extract_nested_value(obj: dict, keys: list[str]) -> Any:
    """Извлекает значение из вложенных структур данных по цепочке ключей.
    Принимает словарь и список ключей, определяющих путь к значению.
    Возвращает значение по указанному пути или None, если путь не существует.
    """
    current_value = obj
    for key in keys:
        if not isinstance(current_value, dict) or key not in current_value:
            return None
        current_value = current_value[key]
    return current_value


def process_dictionary_with_config(dictionary: dict, config: dict) -> dict:
    """Обрабатывает один словарь согласно словару-конфигу.
    Принимает вложенный словарь и конфигурацию его обработки.
    Возвращает словарь с извлечёнными и преобразованными значениями."""
    processed_dict = {}
    for name, attribute_config in config.items():
        if isinstance(attribute_config, tuple):
            value = extract_nested_value(dictionary, attribute_config[0])
            if value is not None:
                value = attribute_config[1](value)
        else:
            value = extract_nested_value(dictionary, attribute_config)
        processed_dict[name] = value
    return processed_dict


def process_list_of_dicts_with_config(
    list_of_dicts: list[dict], config: dict
) -> list[dict]:
    """Принимает список словарей и конфигурацию обработки.
    Возвращает список словарей, обработанных согласно конфигурации."""
    return [
        process_dictionary_with_config(dictionary, config)
        for dictionary in list_of_dicts
    ]


def create_processor(config: dict, list_processor: bool = False) -> Callable:
    """Принимает конфигурацию обработки и признак обработки списка.
    Возвращает вызываемый объект с зафиксированной конфигурацией."""
    if list_processor:
        return partial(process_list_of_dicts_with_config, config=config)
    return partial(process_dictionary_with_config, config=config)
