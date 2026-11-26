from typing import Callable


def count_missing_values(data: list[dict]) -> dict:
    """Принимает список словарей.
    Возвращает словарь с количеством пропущенных значений для каждого поля."""
    missing_counts: dict[str, int]
    missing_counts = {}
    for record in data:
        for field in record:
            if record[field] is None:
                missing_counts[field] = missing_counts.get(field, 0) + 1
            else:
                missing_counts[field] = missing_counts.get(field, 0)
    return missing_counts


def calculate_missing_ratios(data: list[dict]) -> dict:
    """Принимает список словарей.
    Возвращает словарь с долями пропущенных значений для каждого поля."""
    missing_counts = count_missing_values(data)
    if not missing_counts:
        return {}
    missing_ratios = {}
    for field in missing_counts:
        missing_ratios[field] = round(missing_counts[field] / len(data), 4)
    return missing_ratios


def filter_data(data: list[dict], condition: Callable) -> list[dict]:
    """Принимает список словарей и условие фильтрации.
    Возвращает список словарей, удовлетворяющих условию."""
    filtered_data = []
    for record in data:
        if condition(record):
            filtered_data.append(record)
    return filtered_data


def group_by_attributes(data: list[dict], attributes: list[str]) -> dict:
    """Принимает список словарей и список атрибутов группировки.
    Возвращает словарь, ключами которого являются кортежи значений
    атрибутов, а значениями — списки соответствующих записей."""
    grouped_data = {}
    for record in data:
        group_key = tuple([record[attribute] for attribute in attributes])
        if group_key not in grouped_data:
            grouped_data[group_key] = [record]
        else:
            grouped_data[group_key].append(record)
    return grouped_data


def apply_aggregation(grouped_data: dict, aggregation: Callable) -> dict:
    """Принимает сгруппированные данные и функцию агрегации.
    Возвращает словарь с результатами агрегации по каждой группе."""
    aggregated_data = {}
    for group_key in grouped_data:
        aggregated_data[group_key] = aggregation(grouped_data[group_key])
    return aggregated_data
